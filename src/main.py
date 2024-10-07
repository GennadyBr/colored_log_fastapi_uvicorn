""" FastAPI Boilerplate Library """
import os
import sys

import uvicorn
from fastapi import FastAPI

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.logger import logger
from src.middleware import LoggingMiddleware
from src.api.routers import router

app = FastAPI(
    debug=False,
)
app.add_middleware(LoggingMiddleware)

app.include_router(router)

if __name__ == '__main__':
    logger.info('Information')
    logger.debug('Debug')
    logger.warning('Warning')
    logger.error('Error')
    logger.critical('Critical')

    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        log_config='core/log_conf.yaml',
    )
