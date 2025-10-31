from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from property.presentation.routes import router
from property.settings import create_container
from property.application.exceptions import ExceptionResponse
from property.domain.exceptions import BaseException


app = FastAPI(title="Property Management API")
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def handle_exception(request, error: BaseException):
    return JSONResponse(
        status_code=error.status_code,
        content=ExceptionResponse(
            status_code=error.status_code,
            message=error.message,
        ).model_dump(),
    )


app.add_exception_handler(BaseException, handle_exception)

container = create_container()
app.container = container
