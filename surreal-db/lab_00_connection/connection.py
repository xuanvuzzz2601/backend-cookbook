"""SurrealDB Connection Manager — Sync & Async"""

from __future__ import annotations

import logging
import asyncio
from typing import Any, Optional

from surrealdb import AsyncSurreal, Surreal

logger = logging.getLogger(__name__)


class SurrealDB:
    def __init__(   self, 
                    url: str,
                    user_name: str = None,
                    password: str = None
                ) -> None:
        self.url = url
        self.user_name = user_name
        self.password = password
        self._db: Optional[Surreal] = None

    def connect(self) -> None:
        self._db = Surreal(self.url)

        # sign in / use namespace if needed
        if self.user_name and self.password:
            self._db.signin({
                "username": self.user_name,
                "password": self.password,
            })

        self._db.use("test", "test")

        print(f"Connected: {self.url}")
        logger.info("Connected: %s", self.url)

    def close(self) -> None:
        if self._db:
            self._db.close()
            self._db = None
            logger.info("Disconnected: %s", self.url)

    def __enter__(self) -> "SurrealDB":
        self.connect()
        return self

    def __exit__(self, *_) -> None:
        self.close()

    @property
    def db(self) -> Surreal:
        if not self._db:
            raise RuntimeError("Not connected. Call connect() first.")
        return self._db


class AsyncSurrealDB:
    def __init__( self,
                  url: str,
                  user_name: str = None,
                  password: str = None ) -> None:
        self.url = url
        self.user_name = user_name
        self.password = password
        self._db: Optional[AsyncSurreal] = None

    async def connect(self) -> None:
        self._db = AsyncSurreal(self.url)
        await self._db.connect()

        if self.user_name and self.password:
            await self._db.signin({
                "username": self.user_name,
                "password": self.password,
            })

        await self._db.use("test", "test")

        print(f"Async Connected to {self.url}")

    async def close(self) -> None:
        if self._db:
            await self._db.close()
            self._db = None
            logger.info("Disconnected: %s", self.url)

    async def __aenter__(self) -> "AsyncSurrealDB":
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    @property
    def db(self) -> AsyncSurreal:
        if not self._db:
            raise RuntimeError("Not connected. Call await connect() first.")
        return self._db
    
if __name__ == "__main__": 
    url = "ws://localhost:8080"
    username = "vuhx"
    password = "123456"
    db = AsyncSurrealDB(url, username, password)
    asyncio.run(db.connect())