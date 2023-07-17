<div class="text-center">
  <Icon icon="mdi-post" class="text-4xl mb-4 m-auto" />
  <h1>Tutorial</h1>
</div>

Visual Studio Code is arguably one of the best tools on the market for writing code. It's fast, it's free, and it's open source. It's also highly customizable, and has a huge library of extensions that can be installed to add further functionality. Also is now powered by AI with several code autocompletion extensions such as `Github Copilot`, `Tabnine`, `Kite`, `IntelliCode` among others, gaining popularity among new developers.

Code-server is a fork of Monaco Editor, the same editor that powers VS Code, with features like IntelliSense, debugging, and Git integration. The project is open source under the MIT license, and will be our default IDE, indeed you can run an instance of Code-Server instantly on the cloud by clicking on the button below:

<GithubButton/>

Now you should be in a plain VSCode like IDE. Your password is the same as your ref id number.

<img src="/screen1.png">

Now is you opportunity to customize the environment, here some of the extensions I've used on code-server:

- Color Theme: SynthWave '84 (Cool theme for oldies like me)
- Icon Theme: Material Icon Theme (Elegant and simple)
- Ms-Python (Python Language Server)
- Autoclose Tag (HTML)
- Isort (Python Imports)
- Tailwindcss Intellisense (Autocompletion for Tailwind)
- Tab 9 Autocomplete (AI, asistant)
- Pyright (Static type checker)
- `Thunder Client` a REST API client for testing purposes. (Similar to postman but inside VSCode)

The last extension is mandatory since we couldn't manage to proper configure the proxy to forward ports from the container to the internet or to our local machine yet, we will be testing our API through this extension.

Now you should look an environment that meets your needs, you can install any extension you want, and customize the settings as you wish.

Let's install the missing packages on the system:

```bash
sudo apt install -y python3-pip python3-venv
```

Now we will create a virtual environment for our project:

```bash
virtualenv .venv
```

Now we will activate the virtual environment:

```bash
source .venv/bin/activate
```

Now we will install the dependencies:

```bash
pip install aiofauna
```

Now you should have a nice view of your custom dev environment, you can start coding right away.
You can even download the Progressive Web App (PWA) version of code-server to your phone and start coding on the go.

Let's start coding our first `aiofauna` app.

### Creating our first app

Let's create a new file called `main.py` and add the following code:

```python
# main.py
from aiofauna import Api

app = Api()

@app.get("/")
async def hello():
    return "Hello World!"
```

Then we can test with Thunder Client:

<img src='/screen2.png'/>

Now let's add our environment variables to the `.env` file:

```bash
FAUNA_SECRET=your_fauna_secret
```

With this now we can create our model and our CRUD endpoints:

```python

from aiofauna import FaunaModel, Field, Optional, render_template

class Todo(FaunaModel):
    title: str = Field(..., unique=True)
    completed: bool = Field(default=False, index=True)
    description: Optional[str] = Field(None)

@app.get("/api/todos")
async def get_todos():
    """Get all todos"""
    return await Todo.all()

@app.post("/api/todos")
async def create_todo(todo: Todo):
    """Create a new todo"""
    return await todo.save()

@app.put("/api/todos")
async def update_todo(ref: str):
    """Update a todo"""
    return await Todo.update(ref, completed=True)

@app.delete("/api/todos")
async def delete_todo(ref: str):
    """Delete a todo"""
    return await Todo.delete(ref)

@app.on_event("startup")
async def startup(_):
    """Startup event hook"""
    await Todo.provision()
```

Our collection will be created automatically on the first request, now let's download the PWA and run the server on local, enabling the automatically generated swagger UI on the `/docs` endpoint:

<img src="/screen3.png"/>

Now we can test each endpoint to see if it works as expected:

<img src="/post.png"/>

<img src="/get.png"/>

<img src="/put.png"/>

<img src="/delete.png" />

Now let's create a beautiful frontend for our app.

```html
<!--templates/index.html-->
<head>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@unocss/reset/tailwind.min.css"
  />
  <script src="https://cdn.jsdelivr.net/npm/@unocss/runtime/mini.global.js"></script>
  <title>AioFauna Todos</title>
</head>
<body>
  <div id="app">
    <div flex flex-col items-center shadow-lg shadow-black w-96 p-8 m-8 mx-auto>
      <h1 text-4xl font-extrabold text-center text-blue-500 font-sans>
        + Task
      </h1>
      <form flex flex-col items-center>
        <input
          type="text"
          v-model="todo.title"
          outline
          m-4
          p-1
          rounded-lg
          placeholder="Title"
        />
        <textarea
          v-model="todo.description"
          outline
          m-4
          p-1
          rounded-lg
          w-64
          h-32
          placeholder="Description"
        ></textarea>
        <button @click="post(todo)" px-4 py-2 bg-blue-500 text-white rounded-lg>
          Add
        </button>
      </form>
    </div>
    <div
      v-if="todos.length"
      m-4
      p-4
      bg-gray-100
      rounded-lg
      grid
      grid-cols-1
      sm:grid-cols-2
      md:grid-cols-3
      lg:grid-cols-4
      gap-4
    >
      <div
        v-for="t in todos"
        m-4
        p-4
        flex
        flex-col
        items-center
        bg-white
        rounded-lg
        shadow-lg
        w-64
        gap-2
      >
        <label font-extrabold>Title:</label>
        <h2>[[ t.title ]]</h2>
        <label font-extrabold>Description:</label>
        <p>[[ t.description ]]</p>
        <div class="flex items-center mb-4">
          <input
            :id="t.ref"
            type="checkbox"
            :value="t.completed"
            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
            @change="put(t.ref)"
            checked="t.completed"
          />
          <label
            :for="t.ref"
            class="ml-2 text-sm font-medium text-gray-400 dark:text-gray-500"
            >[[ t.completed ? 'Done' : 'Pending' ]]</label
          >
        </div>
        <label>Created:</label>
        <p>[[ new Date(Math.abs(t.ts)).toLocaleString() ]]</p>
        <button @click="del(t.ref)" px-4 py-2 bg-red-500 text-white rounded-lg>
          Delete
        </button>
      </div>
    </div>
  </div>
  <script type="module">
    import * as Vue from "https://cdnjs.cloudflare.com/ajax/libs/vue/3.2.47/vue.esm-browser.prod.min.js";
    const { ref, createApp, onMounted } = Vue;
    const app = createApp({
      delimiters: ["[[", "]]"],
      setup() {
        const todos = ref([]);
        const todo = ref({
          title: "",
          completed: false,
          description: "",
        });
        const get = async () => {
          const res = await fetch("/api/todos");
          const data = await res.json();
          todos.value = data;
        };
        const post = async (todo) => {
          const res = await fetch("/api/todos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(todo),
          });
          await res.json();
          await get();
        };
        const put = async (ref_) => {
          const res = await fetch(`/api/todos?ref=${ref_}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
          });
          await res.json();
          await get();
        };
        const del = async (ref_) => {
          const res = await fetch(`/api/todos?ref=${ref_}`, {
            method: "DELETE",
          });
          await res.text();
          await get();
        };
        onMounted(get);
        return { todo, todos, get, post, put, del };
      },
    });
    app.mount("#app");
  </script>
</body>
```

> Let's take in account that we changed the delimiters of the Vue app to `[[` `]]` so they don't get overlapped by Jinja2 syntax.

Now let's modify our root endpoint to serve the frontend:

```python

from aiofauna import render_template


@app.get("/")
async def index():
  """Front End"""
  return render_template("index.html")
```

With this we have our Todo App ready to be deployed, let's create a `Dockerfile` to build our image:

```dockerfile
# Dockerfile
FROM python:3.9.7-slim-buster

ARG LOCAL_PATH

WORKDIR /app

COPY ${LOCAL_PATH} /app

RUN pip install -r requirements.txt

CMD ["python","main.py"]
```

We will also need a `requirements.txt` file:

```txt
aiofauna
```

## Why the `LOCAL_PATH` variable?

By default the tarball downloaded from github is prepended by the `[owner][repo][sha]` named directory which is our `LOCAL_PATH` variable, soon a better workaround will be found. Now it's time to push the project to GitHub. Be sure to properly config your `.gitconfig` file in the root directory, It should look something like this:

```gitconfig
@yourusername
    name = Your Name
    email = <your@email.here>
```

Once your repo is published on Github, let's jump into the deployment section, input your Github username and repo name on the form below, and click on the `Deploy` button.

<DeployRepo/>

It will take no more than 30 seconds to deploy your app.

Then click on the `Visit your brand new App!` button and see it live:

<img src="/app.png"/>

And that's how you build a serverless full-stack app with AioFauna framework!

<br/>
<br/>
<br/>
