from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db, create_session_db
from src.schema.schemas import Product
from src.infra.sqlalchemy.repository.product import ProcessProduct

create_session_db()

app = FastAPI()


@app.post('/produtos')
def add_product(product: Product, db: Session = Depends(get_db)):
    prd_db = ProcessProduct(db).create(product)
    return prd_db


@app.get('/produtos')
def to_list(db: Session = Depends(get_db)):
    list_prd = ProcessProduct(db).to_list()
    return list_prd