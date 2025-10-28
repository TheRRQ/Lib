from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional



class BookBase(BaseModel):
    serial_number : int = Field(... , ge=100000, le=999999, description="6 digit book SN")
    title : str
    author : str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    is_borrowed : Optional[bool] = None
    borrowed_by : Optional[int] = None
    borrowed_at : Optional[datetime] = None


class Book(BookBase):

    id : int

    is_borrowed : bool
    borrowed_by : Optional[int] = None
    borrowed_at : Optional[datetime] = None



    class Config:
        from_attributes = True
