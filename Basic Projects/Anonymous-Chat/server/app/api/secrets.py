from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.models import Secret
from app.database import get_db

router = APIRouter(
    prefix="/secret",
    tags=["secret"]
)

@router.post("/")
def create_secret(secret: str, db: Session = Depends(get_db)):
    # Check if the secret already exists
    db_secret = db.query(Secret).filter(Secret.secret == secret).first()
    if db_secret:
        raise HTTPException(status_code=400, detail="Secret already exists")
    # Create a new secret
    new_secret = Secret(secret=secret)
    db.add(new_secret)
    db.commit()
    db.refresh(new_secret)
    return {"message": f"New secret is created as: {new_secret.secret}", "id": new_secret.id}

@router.delete("/delete/{secret_id}")
def delete_secret(secret: str, db: Session = Depends(get_db)):
    db_secret = db.query(Secret).filter(Secret.secret == secret).first()
    if not db_secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    db.delete(db_secret)
    db.commit()
    return {"Message": f"Secret deleted, Good Business", "id": db_secret.id}