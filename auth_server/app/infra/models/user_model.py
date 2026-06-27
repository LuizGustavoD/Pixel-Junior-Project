from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import String

import uuid
from datetime import datetime

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36),
                                     primary_key=True, 
                                     default=lambda: 
                                     str(uuid.uuid4()))
    
    email: Mapped[str] = mapped_column(String(255), 
                                       unique=True, 
                                       nullable=False)
    
    username: Mapped[str] = mapped_column(String(255), 
                                          unique=True, 
                                          nullable=False)
    
    password: Mapped[str] = mapped_column(String(255),
                                           nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, 
                                                 onupdate=datetime.utcnow)