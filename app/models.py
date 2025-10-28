from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Book(Base):

    __tablename__ = "books"


    id = Column(Integer, primary_key= True, index=True)
    serial_number = Column(Integer, unique=True, nullable=False)

    title = Column(String(100), nullable = False)
    author = Column(String(100), nullable=False)

    is_borrowed = Column(Boolean, default=False)
    borrowed_by = Column(Integer, nullable= True)
    borrowed_at = Column(DateTime, nullable= True)


    # for updates
    def update_from_schema(self, data):
        for key, val in data:
            setattr(self, key, val)
