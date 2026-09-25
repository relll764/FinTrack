from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.crud_helpers import get_owned_or_404, get_all_owned
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_category = db.query(Category).filter(Category.user_id == current_user.id, Category.name == category_in.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория '{category_in.name}' уже существует."
        )
    category = Category(name=category_in.name, user_id=current_user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_owned(db, Category, current_user.id)



@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = get_owned_or_404(db, Category, category_id, current_user.id)
    db.delete(category)
    db.commit()
    return None