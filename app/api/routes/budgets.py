from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.crud_helpers import get_owned_or_404
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.budget import Budget
from app.models.expense import Expense
from app.schemas.budget import BudgetCreate, BudgetOut

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("/", response_model=BudgetOut, status_code=status.HTTP_201_CREATED)
def create_budget(budget_in: BudgetCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category_id == budget_in.category_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Budget for this category already exists")

    budget = Budget(user_id=current_user.id, category_id=budget_in.category_id, monthly_limit=budget_in.monthly_limit)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("/", response_model=list[BudgetOut])
def list_budgets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Budget).filter(Budget.user_id == current_user.id).all()


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget = get_owned_or_404(db, Budget, budget_id, current_user.id)
    db.delete(budget)
    db.commit()
    return None


@router.get("/{budget_id}/status")
def get_budget_status(budget_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget = get_owned_or_404(db, Budget, budget_id, current_user.id)

    start_of_month = date.today().replace(day=1)

    spent = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.category_id == budget.category_id,
        Expense.date >= start_of_month,
    ).scalar() or 0

    return {
        "category_id": budget.category_id,
        "monthly_limit": float(budget.monthly_limit),
        "spent": float(spent),
        "remaining": float(budget.monthly_limit) - float(spent),
        "exceeded": spent > budget.monthly_limit,
    }