from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logfire

from app.api.v1.metrics_api import metrics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    yield
    print("Application is shutting down...")


def run_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.include_router(metrics_router)

    logfire.configure()
    logfire.instrument_fastapi(app)

    return app


app = run_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
