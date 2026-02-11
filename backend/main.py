from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO, filemode="a")

logger = logging.getLogger(__name__)
handeler = logging.FileHandler("backend.log")
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handeler.setFormatter(formatter)
logger.addHandler(handeler)


app = FastAPI()


@app.get("/health")
async def health():
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}


@app.get("/echo")
async def echo(message: str):
    logger.info("Echo endpoint was called with message: %s", message)
    return {"reply": f"You said {message}"}
