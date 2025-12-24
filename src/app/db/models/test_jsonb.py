from __future__ import annotations

from typing import Any

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class TestJsonbModel(UUIDAuditBase):
    """Test model to demonstrate JSONB double-encoding bug."""

    __tablename__ = "test_jsonb_model"
    __table_args__ = {"comment": "Test model for JSONB bug reproduction"}

    name: Mapped[str] = mapped_column(nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    settings: Mapped[list[dict[str, Any]] | None] = mapped_column(JSONB, nullable=True, default=None)
