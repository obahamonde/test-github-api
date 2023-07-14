import aiohttp_cors
from .schemas import *
from .services import *
from .tools import *
from .agent import *

def bootstrap():
    """Bootstraps the API server."""
    
    app = AioFauna()
    auth0 = AuthClient()
    cloudflare = CloudFlare()
    aws = AmazonWebServices()

    @app.get("/api")
    async def indexo(q:str,namespace:str):
        return await chat_handler(q,namespace)

    @app.post("/api/auth")
    async def user_info(request: Request):
        try:
            token = request.headers.get("Authorization")
            assert isinstance(token, str)
            token = token.split(" ")[-1]
            user = await auth0.user_info(token)
            assert isinstance(user, User)
            app.logger.info("User logged in: %s", user)
            return Response(
                text=user.json(), content_type="application/json", status=200
            )
        except AssertionError:
            return HTTPException(
                text=dumps({"status": "error", "message": "Invalid token"})
            )
        except Exception as exc:
            app.logger.info(exc)
            return HTTPException(text=dumps({"status": "error", "message": str(exc)}))

    @app.post("/api/chatbot/chat")
    async def main(doc:DocumentModel,audio:bool=False):
        gpt = ChatGPT(namespace=doc.namespace)
        response = await gpt.question(doc.text,ChatBotModel())
        app.logger.info(response)
        if audio is False:
            return response
        else:
            polly = Polly.from_text(response)
            return Response(body=await polly.get_audio(), content_type="application/octet-stream")

    @app.websocket("/api/chatbot/ingest")
    async def ingest_organization_website(
        namespace: str, ref: str, websocket: WebSocketResponse
    ):
        """
        Ingests a website and creates a new organization.
        """
        user = await User.get(ref)
        assert isinstance(user, User)
        tool = SiteMapTool(logger=app.logger, websocket=websocket, namespace=namespace)
        await tool.run(namespace)
        await tool.cleanup()
    @app.post("/api/audio")
    async def text_to_speech(text: str):
        polly = Polly.from_text(text)
        return Response(body=polly.get_audio(), content_type="application/octet-stream")
    
    @app.websocket("/api/chatbot/infer")
    async def lead_generator_bot(websocket: WebSocketResponse, req: Request):
        try:
            namespace = req.query.get("user")
            if namespace:
                user = await User.get(namespace)
                assert isinstance(user, User)
                app.logger.info(user.json())
                assert isinstance(user, User)
                await websocket.send_str(
                    "Welcome back, " + user.name + "!, How can I help you?"
                )
                while True:
                
                    question = await websocket.receive_str()
                    app.logger.info(question)
                    answer = await main(DocumentModel(text=question, namespace=namespace))
                    app.logger.info(answer)
                    assert isinstance(answer, str)
                    await websocket.send_str(answer)
            else:
                namespace = websocket.cookies.get("namespace")
                if not namespace:
                    lead = await Lead.from_request(req).run_until_complete(websocket)
                else:
                    lead = await Lead.get(namespace.__str__())
                assert isinstance(lead, Lead)
                lead = await lead.save()
                assert isinstance(lead, Lead)
                app.logger.info(lead.json())
                assert isinstance(lead.ref, str)
                namespace = lead.ref
                websocket.cookies["namespace"] = namespace
                app.logger.info("Namespace: %s", namespace)
                while True:
                    question = await websocket.receive_str()
                    app.logger.info(question)
                    answer = await main(DocumentModel(text=question, namespace=namespace))
                    app.logger.info(answer)
                    assert isinstance(answer, str)
                    await websocket.send_str(answer)
        except AssertionError:
            await websocket.send_json({"status": "error", "message": "Invalid lead"})
            await websocket.close()
        except Exception as exc:
            app.logger.info(exc)
            await websocket.send_json({"status": "error", "message": str(exc)})
            await websocket.close()

    @app.get("/api/user")
    async def users():
        return await User.all()

    @app.post("/api/github")
    async def callback(code: CodeRequest):
        try:
            github = GitHubService()
            github.base_url = "https://github.com"
            payload = {
                "client_id": env.GH_CLIENT_ID,
                "client_secret": env.GH_CLIENT_SECRET,
                "redirect_uri": "http://localhost:3000/tutorial",
                "code": code.code,
                "state": "1234",
            }
            response = await github.fetch(
                "/login/oauth/access_token", "POST", json=payload
            )
            assert isinstance(response, dict)
            access_token = response["access_token"]
            github_api = GitHubService(access_token)
            gh_user = await github_api.fetch("/user")
            assert isinstance(gh_user, dict)
            user = await User(
                **{
                    "sub": gh_user["id"],
                    "name": gh_user["login"],
                    "email": gh_user["email"],
                    "picture": gh_user["avatar_url"],
                    "emailverified": gh_user["email"] is not None,
                }
            ).save()

            assert isinstance(user, User)
            return {"user": user.dict(), "token": access_token}
        except Exception as e:
            raise Exception from e

    @app.put("/api/user/{ref}")
    async def suscribe_user(ref: str):
        try:
            user = await User.get(ref)
            assert isinstance(user, User)
            if isinstance(user.email, str):
                return await aws.suscribe(user.email)
            else:
                raise Exception("User email not found")
        except Exception as e:
            raise Exception from e
    
    @app.get("/api/github/repos")
    async def search_own_repos(token: str, query: str, login: str):
        gh = GitHubService(token)
        app.logger.info("Searching repos for %s", login)
        response = await gh.search_repos(query, login)
        app.logger.info(response)
        return response

    @app.post("/api/github/workspace")
    async def ci_pipeline(body: ContainerCreate):
        try:
            # Retrieve github token
            token = body.token
            # Instantiate github client
            github = GitHubService(body.token)
            # Instantiate Docker client
            docker = DockerService()
            # Create Docker volume
            volume = await docker.create_volume(tag=body.login + "-" + body.repo)
            # Create App container
            _app = await docker.create_container(body, volume)
            # Provision App Container [ERROR]
            dns_app = await cloudflare.provision(body.login + "-" + body.repo, _app.host_port)

            # instantiate IDE container
            ide = ContainerCreate(
                login=body.login,
                repo=body.repo,
                token=token,
                email=body.email,
                image="codeserver",
            )
            # Create IDE container
            codeserver = await docker.create_code_server(ide, volume)
            # Provision IDE container
            dns_codeserver = await cloudflare.provision(
                body.login + "-" + body.image, codeserver.host_port
            )
            # Create Repo from template
            repo_response = await github.create_repo_from_template(
                RepoTemplateCreate(
                    name=body.repo,
                    template_owner="obahamonde",
                    template_repo=body.image,
                    login=body.login,
                    token=token,
                    email=body.email,
                )
            )
            assert isinstance(repo_response, dict)

            # Construct response payload
            preview = {
                "url": dns_app["url"],
                "ip": f"{env.IP_ADDR}:{_app.host_port}",
                "container": _app.container_id,
                "repo": 1,  # repo_response["html_url"],
            }
            workspace = {
                "url": dns_codeserver["url"],
                "ip": f"{env.IP_ADDR}:{codeserver.host_port}",
                "container": codeserver.container_id,
            }
            return {"workspace": workspace, "preview": preview}
        except Exception as e:
            raise e

    @app.get("/api/provision")
    async def provision(name: str, port: int):
        return await cloudflare.provision(name, port)
    
    
    #@app.post("/api/email/verify")
    async def verify_email(email: str):
        try:
            return await aws.verify_email(Email(email=email))
        except Exception as e:
            raise e
        
    #@app.post("/api/email/send")
    async def send_email(email: Email):
        try:
            return await aws.send_email(email)
        except Exception as e:
            raise e
        
        
    @app.get("/api/db/{ref}")
    async def get_database_key(ref:str):
        """Get the database key"""
        try:
            instance = await DatabaseKey.find_unique("user", ref)
            if isinstance(instance, DatabaseKey):
                return instance
            fql = FaunaClient(secret=env.FAUNA_SECRET)
            # Create a new database
            database = await fql.query(q.create_database({"name": ref}))
            assert isinstance(database, dict)
            global_id = database["global_id"]
            db_ref = database["ref"]["@ref"]["id"]
            # Create a new key
            key = await fql.query(q.create_key({"database": q.database(db_ref), "role": "admin"}))
            assert isinstance(key, dict)
            key_ref = key["ref"]["@ref"]["id"]
            secret = key["secret"]
            hashed_secret = key["hashed_secret"]
            role = key["role"]
            
            response = await DatabaseKey(
                user=ref,
                database=db_ref,
                global_id=global_id,
                key=key_ref,
                secret=secret,
                hashed_secret=hashed_secret,
                role=role
            ).save()
            assert isinstance(response, DatabaseKey)
            app.logger.info(response.json())
            return response
        except Exception as e:
            return {"message": str(e), "status": "error"}

    @app.post("/api/db/ingest")
    async def ingest_data(doc:DocumentModel):
        try:
            gpt = ChatGPT(namespace=doc.namespace)
            return await gpt.insert(doc.text)
        except Exception as e:
            raise e

    @app.post("/api/db/query")
    async def query_data(doc:DocumentModel):
        try:
            gpt = ChatGPT(namespace=doc.namespace)
            return await gpt.predict(doc.text)
        except Exception as e:
            raise e

    @app.get("/api/db/ingest/{namespace}")
    async def ingest_data_(namespace:str):
        try:
            tool = SiteMapTool(namespace=namespace,logger=app.logger)
            await tool.run(namespace)
            return {"status": "success"}
        except HTTPException as e:
            return {"status": "error", "message": dumps(e)}
        
    
    @app.on_event("startup")
    async def startup(_):
        await FaunaModel.create_all()

    @app.get("/")
    async def index():
        return Response(text=open("static/index.html").read(), content_type="text/html")

    app.static()

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            )
        },
    )

    for route in list(app.router.routes()):
        cors.add(route)

    return app
