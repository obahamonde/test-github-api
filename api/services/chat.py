from ..schemas import *

OPENAI_API_KEY: str = environ["OPENAI_API_KEY"]
OPENAI_BASE_URL: str = environ["OPENAI_BASE_URL"]
PINECONE_API_KEY: str = environ["PINECONE_API_KEY"]
PINECONE_INDEX: str = environ["PINECONE_INDEX"]
PINECONE_ENVIRONMENT: str = environ["PINECONE_ENVIRONMENT"]

pc.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
chat = ChatOpenAI(model="gpt-3.5-turbo-16k-0613", max_tokens=1024, temperature=0.7)  # type: ignore


class ChatBot(BaseModel):
    """
    A class that represents a chatbot using the GPT-3 model.

    Attributes:
        model (str): The GPT-3 model to use.
        max_tokens (int): The maximum number of tokens to use.
        temperature (float): The temperature to use.
        messages (List[Union[SystemMessage,HumanMessage, AIMessage]]): The messages to use.
    """

    model: str = Field("gpt-3.5-turbo-16k-0613", title="The GPT-3 model to use")
    max_tokens: int = Field(1024, title="The maximum number of tokens to use")
    temperature: float = Field(0.2, title="The temperature to use")
    messages: List[Union[SystemMessage, HumanMessage, AIMessage]] = Field(
        [], title="The messages to use"
    )

    @property
    def client(self):
        """
        OpenAIAPI - A chatbot using OpenAI's service.
        """
        return ChatOpenAI(model=self.model, max_tokens=self.max_tokens, temperature=self.temperature)  # type: ignore

    async def generate(self, query: str, template: ChatPromptTemplate, **context):
        """
        Generate a response to a user query.

        Args:
            query (str): The user's query.
            template (ChatPromptTemplate): The template to use for the response.
            **context: Additional context for the response.

        Returns:
            The generated response.
        """
        return await self.client.agenerate(
            messages=[
                [
                    SystemMessage(
                        content=template.format_prompt(**context).to_string()
                    ),
                    HumanMessage(content=query),
                ]
            ]
        )

    async def predict(self, query: str):
        """
        Predict an outcome based on a user query.

        Args:
            query (str): The user's query.

        Returns:
            The predicted outcome.
        """
        return await self.client.apredict(text=query)


class VectorStore(BaseModel):
    """
    A class that represents a vector store using Pinecone's service.

    Attributes:
        namespace (str): The namespace to use.
        index (str): The index to use.
        texts (List[str]): The texts to use.
    """

    namespace: str = Field(..., title="The namespace to use")
    index: str = Field(PINECONE_INDEX, title="The index to use")
    texts: List[str] = Field([], title="The texts to use")

    @property
    def executor(self):
        """
        Executor - A Python executor.
        """
        return ThreadPoolExecutor()

    @property
    def client(self):
        """
        Pinecone - A vector store using Pinecone's service.
        """
        return Pinecone.from_texts(
            texts=self.texts,
            embedding=self.embeddings,
            index_name=self.index,
            namespace=self.namespace,
        )

    @property
    def embeddings(self):
        """
        OpenAIEmbeddings - A text embedding model using OpenAI's service.
        """
        return OpenAIEmbeddings()  # type: ignore

    async def search(self, query: str, k: int = 8):
        """
        Search for similar or related content.

        Args:
            query (str): The query to search for.
            k (int): The number of results to return.

        Returns:
            The search results.
        """
        return await self.client.asimilarity_search(query=query, k=k)

    @asyncify
    def insert(self, texts: List[str]):
        """
        Insert text strings into the vector store.

        Args:
            texts (List[str]): The text strings to insert.
        """
        return self.client.add_texts(texts=texts)


class ChatGPT(BaseModel):
    """
    A class that represents the main chatbot application.

    Attributes:
        namespace (str): The namespace to use.
    """

    namespace: str = Field(..., title="The namespace to use")

    @property
    def chatbot(self):
        """
        ChatBot - A chatbot using the GPT-3 model.
        """
        return ChatBot()

    @property
    def vectorstore(self):
        """
        VectorStore(Pinecone) - A vector store using Pinecone's service.
        """
        return VectorStore(namespace=self.namespace)

    async def question(self, query: str, bot: ChatBotModel) -> str:
        """
        Ask a question.

        Args:
            query (str): The question to ask.
            bot (ChatBotModel): The bot to use.

        Returns:
            The bot's response.
        """
        results = await self.vectorstore.search(query=query)
        kwargs = {
            **bot.dict(),
            "previous_answers": "\n".join([result.json() for result in results]),
        }
        response = await self.chatbot.generate(
            query=query,
            template=ChatPromptTemplate.from_template(
                """
            I am {chatbot_name} a {role} that can {action} about {topic}.
            My goal is to {goal}.
            The previous answers related to the user's question were:
            {previous_answers}
            I must be {personality} and {attitude} to the user.
            I must speak the same language as the user does.
            If I'm asked about my identity, I will just say that I'm an AI assistant.
            If I'm asked about my creator, I will just say that I was created by AioFauna.
            If I'm asked about my purpose, I will just say that I was created to help people.
            If I'm asked about my feelings, I will just say that I don't have any feelings.
            If I'm asked about something I don'know, I can ask for clarification, search my knowledge base or
            simply say that I don't know.
            
            AI Message:
            """
            ),
            **kwargs
        )
        text = response.generations[0][0].text
        await self.vectorstore.insert(texts=[text, query])
        return text

    async def predict(self, query: str) -> str:
        """
        Predict an outcome based on a user query.

        Args:
            query (str): The user's query.

        Returns:
            The predicted outcome.
        """
        return await self.chatbot.predict(query=query)

    async def insert(self, text: str):
        """
        Insert a text string into the vector store.

        Args:
            text (str): The text string to insert.
        """
        return await self.vectorstore.insert(texts=[text])

    async def insert_many(self, texts: List[str]):
        """
        Insert multiple text strings into the vector store.

        Args:
            texts (List[str]): The text strings to insert.
        """
        return await self.vectorstore.insert(texts=texts)

    async def search(self, query: str, k: int = 8):
        """
        Search for similar or related content.

        Args:
            query (str): The query to search for.
            k (int): The number of results to return.

        Returns:
            The search results.
        """
        return await self.vectorstore.search(query=query, k=k)
