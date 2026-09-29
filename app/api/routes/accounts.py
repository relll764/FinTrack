from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.api.crud_helpers import get_owned_or_404, get_all_owned
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountOut

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(account_in: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_account = db.query(Account).filter(
        Account.user_id == current_user.id,
        Account.name == account_in.name
    ).first()
    if check_account:
        raise HTTPException(status_code=400, detail="Account already exists")

    account = Account(
        user_id=current_user.id,
        name=account_in.name,
        balance=account_in.balance,
        currency=account_in.currency,
        description=account_in.description,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.get("/", response_model=list[AccountOut])
def get_all_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_owned(db, Account, current_user.id)

@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = get_owned_or_404(db, Account, account_id, current_user.id)
    return account

@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, account_in: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = get_owned_or_404(db, Account, account_id, current_user.id)

    account.name = account_in.name
    account.balance = account_in.balance
    account.currency = account_in.currency
    account.description = account_in.description
    db.commit()
    db.refresh(account)
    return account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = get_owned_or_404(db, Account, account_id, current_user.id)
    db.delete(account)
    db.commit()
    return None

