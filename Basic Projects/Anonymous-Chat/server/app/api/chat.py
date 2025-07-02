from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.models import Secret, Chat
from app.schemas.schemas import ChatSchema
from app.database import get_db

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/{secret}", response_model=list[ChatSchema])
def chat_message(secret: str, message: str, db: Session = Depends(get_db)):
    # Find or create secret
    db_secret = db.query(Secret).filter(Secret.secret == secret).first()
    if not db_secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    # Create a new chat entry
    new_chat = Chat(stored_chats=message, secret_id=db_secret.id,)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    # Return the chat history for the secret
    chats = db.query(Chat).filter(Chat.secret_id == db_secret.id).all()
    return chats