from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class BookBase(BaseModel):
    serial_number : int
    title : str
    author : str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    
    is_borrowed : bool
    borrower_id : Optional[int] = None
    borrowed_at : Optional[datetime] = None


class Book(BookBase):

    id : int

    is_borrowed : bool
    borrower_id : Optional[int] = None
    borrowed_at : Optional[datetime] = None



    class Config:
        orm_mode = True








