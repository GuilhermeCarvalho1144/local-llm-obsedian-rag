from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/echo")
async def echo(message: str):
    return {"reply": f"You said {message}"}
