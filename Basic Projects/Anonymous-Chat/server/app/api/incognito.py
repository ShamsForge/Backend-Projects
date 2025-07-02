from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Secret, Incognito 
from typing import Dict, List

router = APIRouter(
    prefix="/incognito",
    tags=["incognito"]
)


# In-memory store for incognito messages
incognito_sessions: Dict[str, List[str]] = {}

@router.post("/{secret}",)
def incognito_message(secret: str, message: str, db: Session = Depends(get_db)):
    # Check if secret exists
    db_secret = db.query(Secret).filter(Secret.secret == secret).first()
    if not db_secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    # Store message in memory (append, don't overwrite)
    if secret not in incognito_sessions:
        incognito_sessions[secret] = []
    incognito_sessions[secret].append(message)
    # Return the full message history for this secret
    return {"messages": incognito_sessions[secret]}


@router.post("/{secret}/disable")
def disable_incognito(secret: str, db: Session = Depends(get_db)):
    # Check if secret exists
    db_secret = db.query(Secret).filter(Secret.secret == secret).first()
    if not db_secret:
        raise HTTPException(status_code=404, detail="Secret not found")
    # Remove messages for this secret
    incognito_sessions.pop(secret, None)
    return {"status": f"Incognito chat disabled for {secret}. Messages deleted."}