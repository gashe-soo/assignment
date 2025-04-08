from fastapi import FastAPI

from app.api.company import router as company_router
from app.api.exception_handlers import exception_handlers

app = FastAPI()

app.include_router(router=company_router, tags=["company"])
for exception, handler in exception_handlers:
    app.add_exception_handler(exception, handler)
