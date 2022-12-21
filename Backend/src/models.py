import datetime as _dt

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Order(_database.Base):
    __tablename__ = "orders"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer)  # _sql.ForeignKey("users.id", ondelete="CASCADE"))
    table_id = _sql.Column(_sql.Integer)  # _sql.ForeignKey("tables.id", ondelete="CASCADE"))
    date = _sql.Column(_sql.Date)


class Table(_database.Base):
    __tablename__ = "tables"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    number = _sql.Column(_sql.Integer, index=True, unique=True)
