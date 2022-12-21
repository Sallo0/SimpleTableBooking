import datetime as _dt

import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class Table(_pydantic.BaseModel):
    id: int
    number: int

    class Config:
        orm_mode = True


class Order(_pydantic.BaseModel):
    id: int
    owner_id: int
    table_id: int
    date: _dt.date

    class Config:
        orm_mode = True
