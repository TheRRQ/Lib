from fastapi import APIRouter, Depends, HTTPException


from sqlalchemy.orm import Session


from app.database import get_db


from app.schemas import BookCreate, Book, BookUpdate
from app.models import Book as BookModel


router = APIRouter(
    prefix="/books",
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
    db.refresh(db_book)

    return db_book


@router.get("/", response_model = list[Book])
def get_books(db : Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books


@router.get("/{serial_number}", response_model=Book)
def get_book_by_sn(serial_number : int, db : Session = Depends(get_db)):

    book = db.query(BookModel).filter(BookModel.serial_number == serial_number).first()
    
    if not book: 
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book



@router.put("/{serial_number}", response_model = Book)
def update_book_by_sn(serial_number : int, updated: BookUpdate,  db : Session = Depends(get_db)):

    book = db.query(BookModel).filter(BookModel.serial_number == serial_number).first()

    if not book: 
        raise HTTPException(status_code=404, detail="Book not found")

    book.update_from_schema(updated.model_dump(exclude_unset=True))
    
    db.commit()
    db.refresh(book)

    return book


@router.delete("/{serial_number}")
def delete_book_by_sn(serial_number : int, db : Session = Depends(get_db)):
    
    book = db.query(BookModel).filter(BookModel.serial_number == serial_number).first()

    if not book: 
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"msg" : f"Book {serial_number} deleted"}