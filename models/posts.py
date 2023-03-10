from database_manager import BASE
from sqlalchemy import Column, String, TIMESTAMP, text, Integer, ForeignKey, BLOB, Text
from sqlalchemy.orm import relationship
import sqlalchemy.types as types


# class ChoiceType(types.TypeDecorator):
#
#     impl = types.String
#
#     def __init__(self, choices, **kw):
#         self.choices = dict(choices)
#         super(ChoiceType, self).__init__(**kw)
#
#     def process_bind_param(self, value, dialect):
#         return [k for k, v in self.choices.iteritems() if v == value][0]
#
#     def process_result_value(self, value, dialect):
#         return self.choices[value]
#


class Post(BASE):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publish_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    status = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    owner = relationship('User')
    # post_comment = relationship("Comment", back_populates="post_related")


class Comment(BASE):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    publish_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

    parent_comment_id = Column(Integer, ForeignKey("comments.comment_id", ondelete="CASCADE"))

    post_related = relationship("Post")
    user_related = relationship("User")
