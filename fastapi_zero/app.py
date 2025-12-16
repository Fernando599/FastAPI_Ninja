from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI(
    title='API To-do List',
    description='API projeto To-do List para aprendizado.',
)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá FastAPI'}


templates = Jinja2Templates(directory='templates')


@app.get(
    '/exercicio/',
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def exercicio(request: Request):
    return templates.TemplateResponse(
        'exercicio/index.html', {'request': request}
    )


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session: SessionDep,
):

    db_user = session.scalar(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exists',
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists',
                status_code=HTTPStatus.CONFLICT,
            )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(session: SessionDep, limit: int = 10, offset: int = 0):
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session: SessionDep):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    conflict = session.scalar(
        select(User).where(
            User.id != user_id,
            or_(
                (User.username == user.username),
                (User.email == user.email),
            ),
        )
    )

    if conflict:
        if conflict.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists'
        )

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password

    session.commit()
    session.refresh(user_db)

    return user_db


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: SessionDep):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted'}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_user(user_id: int, session: SessionDep):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!',
        )

    return user_db
