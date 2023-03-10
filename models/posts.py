from database_manager import BASE
from sqlalchemy import Column, String, TIMESTAMP, text, Integer, ForeignKey, BLOB, Text


class Post(BASE):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publish_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    status_id = Column(Integer, ForeignKey("status.status_id", ondelete="RESTRICT"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    # image = Column(BLOB)


class Comment(BASE):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.status_id", ondelete="NO ACTION"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    publish_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    parent_comment_id = Column(Integer, ForeignKey("comments.comment_id", ondelete="CASCADE"))


class Status(BASE):
    __tablename__ = "status"

    status_id = Column(Integer, primary_key=True)
    status_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
