from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_image_url: Mapped[str] = mapped_column(String(250), nullable=True)

    # Relationships
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="user")
    followers: Mapped[list["Follower"]] = relationship(
        "Follower", foreign_keys="Follower.followed_id", back_populates="followed"
    )
    following: Mapped[list["Follower"]] = relationship(
        "Follower", foreign_keys="Follower.follower_id", back_populates="follower"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "bio": self.bio,
            "profile_image_url": self.profile_image_url
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relationships
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id
        }
