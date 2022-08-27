from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from logger import logger
from routers import estimation_router


def app_factory() -> FastAPI:
    # Init fast api
    app: FastAPI = FastAPI(title="xung anstattt pfung")

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Add router
    app.include_router(estimation_router.router, prefix='/api/v1/estimation')

    # Logging
    logger.info('Starting app with profile: {}'.format(config.settings.ENV))

    return app
