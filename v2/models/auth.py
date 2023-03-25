from database_manager import BASE
from sqlalchemy import Column, String, TIMESTAMP, text, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class User(BASE):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    is_authenticated = Column(Boolean, default=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    image = Column(String)

    role = Column(String, nullable=False)


class UserRequest(BASE):
    __tablename__ = "user_request"
    user_request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    request_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    __table_args__ = (UniqueConstraint('user_id', 'request_name', 'status', name='unique_request'),)
    owner = relationship('User')


class ContactUs(BASE):
    __tablename__ = "contact_us"
    contact_us_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))