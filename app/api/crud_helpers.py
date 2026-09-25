from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def get_owned_or_404(db: Session, model, obj_id: int, user_id: int):
    obj = db.query(model).filter(model.id == obj_id, model.user_id == user_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found",
        )
    return obj

def get_all_owned(db: Session, model, user_id: int):
    return db.query(model).filter(model.user_id == user_id).all()