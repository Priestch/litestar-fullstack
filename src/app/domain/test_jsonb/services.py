from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db import models as m

__all__ = ("TestJsonbService",)


class TestJsonbService(SQLAlchemyAsyncRepositoryService[m.TestJsonbModel]):
    """Handles basic lookup operations for TestJsonbModel."""

    class Repository(SQLAlchemyAsyncRepository[m.TestJsonbModel]):
        """TestJsonbModel Repository."""

        model_type = m.TestJsonbModel

    repository_type = Repository
    match_fields = ["name"]
