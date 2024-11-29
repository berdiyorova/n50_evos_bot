import sqlalchemy
from sqlalchemy import DateTime, func, UniqueConstraint

from main.constants import UserStatus
from main.database import metadata

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("full_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("language", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger, unique=True, nullable=False),
    sqlalchemy.Column("phone_number", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String, default=UserStatus.active, nullable=False),
    sqlalchemy.Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), onupdate=func.now(), nullable=False)
)

address = sqlalchemy.Table(
    'address',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("longitude", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("latitude", sqlalchemy.String, nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), onupdate=func.now(), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('user.id'), nullable=True),
    UniqueConstraint('longitude', 'latitude', name='uix_longitude_latitude')
)

category = sqlalchemy.Table(
    "category",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True)
)

product = sqlalchemy.Table(
    "product",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.DECIMAL),
    sqlalchemy.Column("category_id", sqlalchemy.ForeignKey('category.id'))
)

cart = sqlalchemy.Table(
    "cart",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey('product.id')),
    sqlalchemy.Column("quantity", sqlalchemy.Integer, default=1),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('user.id'))
)

order = sqlalchemy.Table(
    "order",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product_name", sqlalchemy.String),
    sqlalchemy.Column("product_price", sqlalchemy.DECIMAL),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
    sqlalchemy.Column("total_price", sqlalchemy.DECIMAL),
    sqlalchemy.Column("status", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('user.id'))
)

feedback = sqlalchemy.Table(
    "feedback",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('user.id', ondelete='CASCADE'))
)
