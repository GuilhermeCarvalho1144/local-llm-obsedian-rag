from fastapi import FastAPI
import logging
import inngest
import inngest.fast_api

logging.basicConfig(level=logging.INFO, filemode="a")

logger = logging.getLogger(__name__)
handeler = logging.FileHandler("backend.log")
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handeler.setFormatter(formatter)
logger.addHandler(handeler)

inngest_client = inngest.Inngest(
    app_id="local-llm-obsedian-rag",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer(),
)


@inngest_client.create_function(
    fn_id="echo_function", trigger=inngest.TriggerEvent(event="/echo")
)
async def echo_function(ctx: inngest.Context) -> dict:
    return {"reply": "Hello from the echo function!"}


app = FastAPI()

inngest.fast_api.serve(
    app,
    inngest_client,
    [
        echo_function,
    ],
)


@app.get("/health")
async def health():
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}


@app.get("/echo")
async def echo(message: str):
    logger.info("Echo endpoint was called with message: %s", message)
    return {"reply": f"You said {message}"}
