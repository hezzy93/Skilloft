from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID


from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=True)
    first_name = Column(String, index=True, nullable=True)
    hashed_password = Column(String)

