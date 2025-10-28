from fastapi import APIRouter, Depends, HTTPException


from sqlalchemy.orm import Session


from app.database import get_db


from app.schemas import BookCreate
from app.models import Book as BookModel


router = APIRouter(
    "/books",
    tags=["books"]
)



@router.post("/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    

    existing = db.query(BookModel).filter(BookModel.serial_number == book.serial_number).first()
    
    if existing :
        raise HTTPException(status_code=400, detail="This serial number already exists.")



    db_book = BookModel(
        serial_number = book.serial_number,
        title = book.title,
        author = book.author
    )


    db.add(db_book)
    db.commit()
    db.refresh()

    return db_book
