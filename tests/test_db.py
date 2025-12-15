from datetime import datetime

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    new_user = User(username='test', email='test@test.com', password='secret')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.id == 1
    assert user.username == 'test'
    assert user.email == 'test@test.com'
    assert user.password == 'secret'
    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)
