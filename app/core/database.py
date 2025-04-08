from contextvars import ContextVar
from functools import wraps
from typing import Any, AsyncGenerator, Callable, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# ContextVar 정의
db_session_ctx: ContextVar[AsyncSession] = ContextVar("db_session_ctx")

async_engine = create_async_engine(
    settings.DATABASE_URL, echo=True, future=True
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        token = db_session_ctx.set(session)
        try:
            yield session
        finally:
            db_session_ctx.reset(token)


def get_current_session() -> AsyncSession:
    session = db_session_ctx.get(None)
    if session is None:
        raise RuntimeError("No session found in context")
    return session


def transactional(
    func: Callable[..., Coroutine[Any, Any, Any]]
) -> Callable[..., Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:  # type: ignore
        session = get_current_session()
        try:
            result = await func(*args, **kwargs)
            await session.commit()
            return result
        except Exception:
            await session.rollback()
            raise

    return wrapper
