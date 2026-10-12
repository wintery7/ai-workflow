from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.documents import router as documents_router
from app.db.database import Base, engine
from app.db.session import get_db
from app.models.contract import Contract

app = FastAPI()

app.include_router(documents_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "AI Workflow API"}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"result": result.scalar()}


@app.post("/db-test/contract")
def create_test_contract(db: Session = Depends(get_db)):
    contract = Contract(
        filename="test_contract.pdf",
        content="ABC 회사와의 서비스 공급 계약입니다.",
        contract_type="서비스 계약",
        party="ABC회사",
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)

    return {
        "id": contract.id,
        "filename": contract.filename,
        "contract_type": contract.contract_type,
        "party": contract.party,
    }