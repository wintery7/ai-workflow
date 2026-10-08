from fastapi import APIRouter, Depends, File, UploadFile
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.contract import Contract

router = APIRouter()


@router.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    pdf_reader = PdfReader(file.file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    contract = Contract(
        filename=file.filename,
        content=text,
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)

    return {
        "id": contract.id,
        "filename": contract.filename,
        "text_length": len(text),
    }