"""
Модель категории расходов
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator
from datetime import datetime

from ..repository.abstract_repository import AbstractRepository

@dataclass
class Budget():
    end_date: datetime
    sum: float

    def __init__(self, end_date: datetime, sum: float):
        self.end_date = end_date
        self.sum = sum