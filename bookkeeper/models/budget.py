"""
Модель категории бюджета
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator
from datetime import datetime, timedelta

from ..repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense

@dataclass
class Budget():
    period: str
    limit: int
    spent: int = 0
    pk: int = 0

    def __init__(self, period: str, limit: int, spent: int = 0, pk: int = 0):

        if period == "day" or period == "week" or period == "month" or period == "year":
            self.period = period
        else:
            raise ValueError(f"Unknown period \"{period}\" for budget:\n"
                             + "should be \"day\", \"week\", \"month\" or \"year\".")
        self.limit = limit
        self.spent = spent
        self.pk = pk

    def update(self, expense_repo: AbstractRepository[Expense]):
        date = datetime.now().isoformat()[:10]

        expenses = []
        if self.period == 'day':
            expenses += expense_repo.get_all(where = {'expense_date': date + '%'})
        elif self.period == 'week':
            date_weekday = datetime.now().weekday()
            for wd in range(date_weekday + 1):
                day = datetime.now() - timedelta(days = wd)
                day = day.isoformat()[:10] + '%'
                expenses += expense_repo.get_all(where = {'expense_date': day})
        elif self.period == 'month':
            date_month = date[:7] + '%'
            expenses += expense_repo.get_all(where = {'expense_date': date_month})
        elif self.period == 'year':
            date_year = date[:5] + '%'
            expenses += expense_repo.get_all(where = {'expense_date': date_year})
        print('exps:', expenses)
        #self.spent = sum(record for record in expenses)