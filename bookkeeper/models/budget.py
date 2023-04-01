from dataclasses import dataclass
from datetime import datetime, timedelta

from bookkeeper.models.expense import Expense
from ..repository.abstract_repository import AbstractRepository


@dataclass
class Budget():
    """
    Модель категории бюджета
    """
    period: str
    lim: int
    spent: int = 0
    pk: int = 0

    def __init__(self, period: str, lim: int, spent: int = 0, pk: int = 0):
        if period in ('day', 'week', 'month', 'year'):
            self.period = period
        else:
            raise ValueError(f"Unknown period \"{period}\" for budget:\n"
                             + "should be \"day\", \"week\", \"month\" or \"year\".")
        self.lim = lim
        self.spent = spent
        self.pk = pk

    def update(self, expense_repo: AbstractRepository[Expense]):
        """
        This method updates budget data with the accordance
        to the newly added expenses
        """
        date = datetime.now().isoformat()[:10]

        expenses = []
        if self.period == 'day':
            expenses += expense_repo.get_all_like(where={'expense_date': date+'%'})
        elif self.period == 'week':
            date_weekday = datetime.now().weekday()
            for wday in range(date_weekday+1):
                day = datetime.now() - timedelta(days=wday)
                day = day.isoformat()[:10] + '%'
                expenses += expense_repo.get_all_like(where={'expense_date': day})
        elif self.period == 'month':
            date_month = date[:7] + '%'
            expenses += expense_repo.get_all_like(where={'expense_date': date_month})
        elif self.period == 'year':
            date_year = date[:5] + '%'
            expenses += expense_repo.get_all_like(where={'expense_date': date_year})
        self.spent = sum(int(record.amount) for record in expenses)
