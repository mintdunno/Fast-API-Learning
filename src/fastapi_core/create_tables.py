import asyncio

from fastapi_core.db import engine
from fastapi_core.db_base import Base
from fastapi_core.features.notes.model import Note  # noqa: F401
from fastapi_core.features.users.model import User  # noqa: F401


async def main() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
