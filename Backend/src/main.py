from typing import List

import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

import schemas as _schemas
import services as _services

app = _fastapi.FastAPI()


# ------------------- users

@app.post("/api/users")
async def create_user(
        user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
        form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
        db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


# ------------------- tables

@app.get("/api/tables", response_model=list[_schemas.Table])
async def get_tables(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_tables(db)


@app.post("/api/tables", response_model=_schemas.Table)
async def create_table(
        table: _schemas.Table,
        db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_table(table, db)


# ------------------- orders

@app.get("/api/orders/all", response_model=list[_schemas.Order])
async def get_all_orders(
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_all_orders(db)


@app.get("/api/orders", response_model=list[_schemas.Order])
async def get_orders(
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_user_orders(user, db)


@app.post("/api/orders", response_model=_schemas.Order)
async def create_order(
        table: _schemas.Table,
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.create_order(user=user, table=table, db=db)


@app.delete("/api/orders", status_code=204)
async def delete_order(
        table: _schemas.Table,
        user: _schemas.User = _fastapi.Depends(_services.get_current_user),
        db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    await _services.delete_order(user=user, table=table, db=db)
    return {"message", "Successfully Deleted"}


# ------------------- app

@app.get("/api")
async def root():
    return {"message": "Бронирование столиков онлайн (с регистрацией)"}
