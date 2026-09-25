from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.crud_helpers import get_owned_or_404, get_all_owned
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionOut, SubscriptionCreate

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/", response_model=SubscriptionOut, status_code=status.HTTP_201_CREATED)
def create_subscription(subscription_in: SubscriptionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = Subscription(
        user_id=current_user.id,
        name=subscription_in.name,
        amount=subscription_in.amount,
        currency=subscription_in.currency,
        period=subscription_in.period,
        next_billing_date=subscription_in.next_billing_date,
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

@router.get("/", response_model=list[SubscriptionOut])
def get_all_subscriptions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_owned(db, Subscription, current_user.id)

@router.get("/{subscription_id}", response_model=SubscriptionOut)
def get_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = get_owned_or_404(db, Subscription, subscription_id, current_user.id)
    return subscription


@router.put("/{subscription_id}", response_model=SubscriptionOut)
def update_subscription(subscription_id: int, subscription_in: SubscriptionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = get_owned_or_404(db, Subscription, subscription_id, current_user.id)

    subscription.name = subscription_in.name
    subscription.amount = subscription_in.amount
    subscription.currency = subscription_in.currency
    subscription.period = subscription_in.period
    subscription.next_billing_date = subscription_in.next_billing_date
    db.commit()
    db.refresh(subscription)
    return subscription

@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription = get_owned_or_404(db, Subscription, subscription_id, current_user.id)
    db.delete(subscription)
    db.commit()
    return None




