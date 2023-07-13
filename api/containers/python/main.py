from aiofauna import AioFauna

app = AioFauna()

@app.get("/")
async def index():
    return {"message": "Hello World"}


