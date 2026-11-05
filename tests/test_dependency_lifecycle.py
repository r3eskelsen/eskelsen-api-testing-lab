"""Verify the original FastAPI database dependency lifecycle."""

import pytest
from sqlalchemy.orm import Session

from app.main import get_db


def test_get_db_yields_and_closes_session():
    dependency = get_db()
    session = next(dependency)

    try:
        assert isinstance(session, Session)
    finally:
        with pytest.raises(StopIteration):
            next(dependency)

    assert dependency.gi_frame is None

