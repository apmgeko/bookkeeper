from datetime import datetime

import pytest

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense

import os

cwd = os.getcwd()
db_file = os.path.join(cwd, 'tests', 'test_models', 'test_db_file.db')

@pytest.fixture
def repo():
    return SQLiteRepository(db_file, Expense)


def test_create_with_full_args_list():
    bd = Budget(limit = 1000, period = 'day', spent = 100, pk = 1)
    assert bd.limit == 1000
    assert bd.period == 'day'
    assert bd.spent == 100
    assert bd.pk == 1

    bw = Budget(limit = 2000, period = 'week', spent = 200, pk = 2)
    assert bw.limit == 2000
    assert bw.period == 'week'
    assert bw.spent == 200
    assert bw.pk == 2

    bm = Budget(limit = 3000, period = 'month', spent = 300, pk = 3)
    assert bm.limit == 3000
    assert bm.period == 'month'
    assert bm.spent == 300
    assert bm.pk == 3

    by = Budget(limit = 4000, period = 'year', spent = 400, pk = 4)
    assert by.limit == 4000
    assert by.period == 'year'
    assert by.spent == 400
    assert by.pk == 4


def test_update(repo):
    bd = Budget(limit = 1000, period = 'day', spent = 100, pk = 1)
    bw = Budget(limit = 2000, period = 'week', spent = 200, pk = 2)
    bm = Budget(limit = 3000, period = 'month', spent = 300, pk = 3)
    by = Budget(limit = 4000, period = 'year', spent = 400, pk = 4)

    exp = Expense(category = 1, amount = 10)
    repo.add(exp)
    bd.update(repo)
    bw.update(repo)
    bm.update(repo)
    by.update(repo)

    assert bd.spent == 110
    assert bw.spent == 210
    assert bm.spent == 310
    assert by.spent == 410

'''
def test_create_brief():
    e = Expense(100, 1)
    assert e.amount == 100
    assert e.category == 1


def test_can_add_to_repo(repo):
    e = Expense(100, 1)
    pk = repo.add(e)
    assert e.pk == pk
'''
