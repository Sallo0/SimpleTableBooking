import datetime as _dt

import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import passlib.hash as _hash
import sqlalchemy.orm as _orm

import database as _database
import models as _models
import schemas as _schemas

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = ""


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------- users

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
        db: _orm.Session = _fastapi.Depends(get_db),
        token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)


# ------------------- tables

async def get_tables(db: _orm.Session):
    tables = db.query(_models.Table)
    return list(map(_schemas.Table.from_orm, tables))


async def create_table(table: _schemas.Table, db: _orm.Session):
    table = _models.Table(id=table.id, number=table.number)
    db.add(table)
    db.commit()
    db.refresh(table)
    return _schemas.Table.from_orm(table)


# ------------------- orders

async def get_user_orders(user: _schemas.User, db: _orm.Session):
    orders = db.query(_models.Order).filter_by(owner_id=user.id)
    return list(map(_schemas.Order.from_orm, orders))


async def get_all_orders(db: _orm.Session):
    orders = db.query(_models.Order)
    return list(map(_schemas.Order.from_orm, orders))


async def create_order(user: _schemas.User, table: _schemas.Table, db: _orm.Session):
    order = _models.Order(owner_id=user.id, table_id=table.id, date=_dt.date.today())
    db.add(order)
    db.commit()
    db.refresh(order)
    return _schemas.Order.from_orm(order)


async def delete_order(user: _schemas.User, table: _schemas.Table, db: _orm.Session):
    order = db.query(_models.Order).filter_by(owner_id=user.id, table_id=table.id).first()
    db.delete(order)
    db.commit()
