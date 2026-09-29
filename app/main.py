from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView

from app.api.routes import auth, categories, subscriptions, expenses, budgets

from app.db.session import engine
from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense
from app.models.subscription import Subscription
from app.models.budget import Budget

from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(title="FinTrack API")

admin = Admin(app, engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(subscriptions.router)
app.include_router(expenses.router)
app.include_router(budgets.router)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username, User.created_at]
    column_searchable_list = [User.email, User.username]
    name = "Пользователь"
    name_plural = "Пользователи"


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.user_id]
    name = "Категория"
    name_plural = "Категории"


class ExpenseAdmin(ModelView, model=Expense):
    column_list = [Expense.id, Expense.user_id, Expense.category_id, Expense.amount, Expense.currency, Expense.date]
    column_searchable_list = [Expense.description]
    column_sortable_list = [Expense.date, Expense.amount]
    name = "Расход"
    name_plural = "Расходы"


class SubscriptionAdmin(ModelView, model=Subscription):
    column_list = [Subscription.id, Subscription.user_id, Subscription.name, Subscription.amount, Subscription.next_billing_date]
    name = "Подписка"
    name_plural = "Подписки"


class BudgetAdmin(ModelView, model=Budget):
    column_list = [Budget.id, Budget.user_id, Budget.category_id, Budget.monthly_limit]
    name = "Бюджет"
    name_plural = "Бюджеты"


admin.add_view(UserAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ExpenseAdmin)
admin.add_view(SubscriptionAdmin)
admin.add_view(BudgetAdmin)

@app.get("/health")
def health_check():
    return {"status": "ok"}