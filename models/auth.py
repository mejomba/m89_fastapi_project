from database_manager import BASE
from sqlalchemy import Column, String, TIMESTAMP, text, Integer, ForeignKey


class User(BASE):

    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    username = Column (String, nullable=False )
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_update = Column (TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

    role_id = Column(Integer, ForeignKey('role.id',ondelete='RESTRICT'), nullable=False)



