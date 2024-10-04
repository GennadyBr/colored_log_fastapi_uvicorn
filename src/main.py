""" FastAPI Boilerplate Library """
from typing import Callable

import requests
import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging middleware"""

    async def dispatch(
        self, request: Request, call_next: Callable,
    ) -> Response:
        logger.info('Logging middleware')
        logger.info(f'Request: {request.method} {request.url}')
        response = await call_next(request)
        logger.info(f'Response: {response.status_code}')
        return response


app = FastAPI(
    debug=False,
)
app.add_middleware(LoggingMiddleware)


def _hello() -> dict:
    """Hello world"""
    logger.info('Hello World')
    return {'message': 'Hello World'}


def _request() -> str:
    """Request example"""
    response = requests.get('https://google.com')
    result = f'Google Response: {response.status_code}'
    logger.info(result)
    return result


def _raise_error() -> str:
    """Raise Error"""
    try:
        div_zero = 1 / 0
    except ZeroDivisionError as error:
        logger.error(error)
        logger.exception('RRRR - Divide by zero error')
        return str(error)
    return str(div_zero)


@app.get('/hello')
async def hello() -> dict:
    """Hello world"""
    return _hello()


@app.get('/request')
async def request() -> str:
    """Request example"""
    return _request()


@app.get('/raise_error')
async def raise_error() -> str:
    """Raise Error"""
    return _raise_error()


if __name__ == '__main__':

    _hello()
    _request()
    _raise_error()

    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        log_config='core/log_conf.yaml',
    )
