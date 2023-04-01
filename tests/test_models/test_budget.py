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
    bd = Budget(lim = 1000, period = 'day', spent = 100, pk = 1)
    assert bd.lim == 1000
    assert bd.period == 'day'
    assert bd.spent == 100
    assert bd.pk == 1

    bw = Budget(lim = 2000, period = 'week', spent = 200, pk = 2)
    assert bw.lim == 2000
    assert bw.period == 'week'
    assert bw.spent == 200
    assert bw.pk == 2

    bm = Budget(lim = 3000, period = 'month', spent = 300, pk = 3)
    assert bm.lim == 3000
    assert bm.period == 'month'
    assert bm.spent == 300
    assert bm.pk == 3

    by = Budget(lim = 4000, period = 'year', spent = 400, pk = 4)
    assert by.lim == 4000
    assert by.period == 'year'
    assert by.spent == 400
    assert by.pk == 4


def test_update(repo):
    bd = Budget(lim = 1000, period = 'day', spent = 100, pk = 1)
    bw = Budget(lim = 2000, period = 'week', spent = 200, pk = 2)
    bm = Budget(lim = 3000, period = 'month', spent = 300, pk = 3)
    by = Budget(lim = 4000, period = 'year', spent = 400, pk = 4)

    exp = Expense(category = 1, amount = 10)
    repo.add(exp)
    bd.update(repo)
    bw.update(repo)
    bm.update(repo)
    by.update(repo)

    assert bd.spent == 10
    assert bw.spent == 10
    assert bm.spent == 10
    assert by.spent == 10

    repo.delete(repo.last_pk)

def test_create_unexistent_period():
    with pytest.raises(ValueError):
        b = Budget(lim = 1000, period = 'decade', spent = 100, pk = 1)

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
