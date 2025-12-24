from __future__ import annotations

from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar import Controller, delete, get, post

from app.db import models as m
from app.domain.test_jsonb.services import TestJsonbService
from app.lib import dto
from app.lib.deps import create_service_dependencies

from . import urls

if TYPE_CHECKING:
    from litestar.dto import DTOData
    from litestar.params import Parameter


class TestJsonbDTO(SQLAlchemyDTO[m.TestJsonbModel]):
    config = dto.config(max_nested_depth=0, exclude={"created_at", "updated_at"})


class TestJsonbCreateDTO(SQLAlchemyDTO[m.TestJsonbModel]):
    config = dto.config(max_nested_depth=0, exclude={"id", "created_at", "updated_at"})


class TestJsonbController(Controller):
    """Public API for testing JSONB double-encoding bug."""

    guards = []  # No authentication required for testing
    dependencies = create_service_dependencies(
        TestJsonbService,
        key="test_jsonb_service",
    )
    tags = ["Test JSONB"]
    return_dto = TestJsonbDTO

    @get(operation_id="GetTestJsonb", path=urls.TEST_JSONB_DETAILS)
    async def get_item(
        self,
        test_jsonb_service: TestJsonbService,
        item_id: Annotated[UUID, Parameter(title="Item ID", description="The item to retrieve.")],
    ) -> dict:
        """Get a specific test JSONB item."""
        db_obj = await test_jsonb_service.get(item_id)
        return db_obj.to_dict()

    @post(operation_id="CreateTestJsonb", path=urls.TEST_JSONB_CREATE, dto=TestJsonbCreateDTO)
    async def create_item(
        self,
        test_jsonb_service: TestJsonbService,
        data: DTOData[m.TestJsonbModel],
    ) -> dict:
        """Create a new test JSONB item."""
        db_obj = await test_jsonb_service.create(data, auto_commit=True)
        return db_obj.to_dict()

    @delete(operation_id="ClearTestJsonb", path=urls.TEST_JSONB_CLEAR, status_code=200, return_dto=None)
    async def clear_all(
        self,
        test_jsonb_service: TestJsonbService,
    ) -> dict[str, str]:
        """Clear all test JSONB items."""
        await test_jsonb_service.repository.session.execute(
            test_jsonb_service.repository.statement.delete(m.TestJsonbModel)
        )
        await test_jsonb_service.repository.session.commit()
        return {"message": "All test items cleared"}
