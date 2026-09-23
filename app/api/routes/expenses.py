from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models import Category
from app.models.user import User
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseOut
from app.services.categorization import categorize
import logging
logging.basicConfig(
    level=logging.INFO,  # Минимальный уровень логов для вывода
    format="%(asctime)s [%(levelname)s] %(message)s",  # Формат: Время [Уровень] Сообщение
    datefmt="%Y-%m-%d %H:%M:%S"
)
router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category_id = expense_in.category_id

    if category_id is None and expense_in.description:
        user_categories = db.query(Category).filter(Category.user_id == current_user.id).all()
        category_names = [c.name for c in user_categories]

        predicted_name = categorize(expense_in.description, category_names)

        if predicted_name is not None:
            category = db.query(Category).filter(
                Category.name == predicted_name,
                Category.user_id == current_user.id
            ).first()
            if category:
                category_id = category.id

    # теперь один-единственный блок создания, неважно откуда взялся category_id
    expense = Expense(
        user_id=current_user.id,
        category_id=category_id,
        amount=expense_in.amount,
        currency=expense_in.currency,
        description=expense_in.description,
        date=expense_in.date,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/", response_model=list[ExpenseOut])
def get_all_expenses(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Expense).filter(Expense.user_id ==current_user.id).all()


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.user_id == current_user.id, Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense_in: ExpenseCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense.amount = expense_in.amount
    expense.currency = expense_in.currency
    expense.description = expense_in.description
    expense.date = expense_in.date
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return None