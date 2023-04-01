from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category

from datetime import datetime
import sqlite3
import os

import pytest

cwd = os.getcwd()
db_file = os.path.join(cwd, 'tests', 'test_repository', 'test_db_file.db')
FIELD_INT  = 58008
FIELD_STR  = "\"I am string\""
FIELD_DATE = datetime.now()

@pytest.fixture
def custom_class():
    class Custom():
        field_int  : int       = FIELD_INT
        field_str  : str       = FIELD_STR
        field_date : datetime  = FIELD_DATE
        pk         : int       = 0

        def __init__(self, field_int: int = FIELD_INT, field_str: str = FIELD_STR, field_date: datetime = FIELD_DATE, pk: int = 0):
            self.field_int = field_int
            self.field_str = field_str
            self.field_date = field_date
            self.pk = pk

        def __eq__(self, other):
            s = False
            if (self.field_int == other.field_int and
            self.field_str == other.field_str and
            self.field_date == other.field_date):
                s = True
            return s
        
    return Custom


@pytest.fixture
def repo(custom_class):
    cls = custom_class
    return SQLiteRepository(db_file, cls)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None

def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    repo.add(custom_class())
    while repo.last_pk != 0:
        repo.delete(repo.last_pk)
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects
    for i in range(5):
        repo.delete(repo.last_pk)

def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.field_int = i
        o.field_str = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'field_str': 'test'}) == objects
    assert repo.get_all({'field_int': 3}) == [objects[3]]
    for i in range(5):
        repo.delete(repo.last_pk)
    

def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)

def test_get_all_like(repo, custom_class):
    objects = []
    for i in range(15):
        o = custom_class()
        o.field_int = i
        o.field_str = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all_like() == objects
    assert repo.get_all_like({'field_str': 't%'}) == objects
    got_all_like = repo.get_all_like({'field_int': '1%'})
    check_list = [objects[1]]
    for i in range(10, 15):
        check_list.append(objects[i])
    assert got_all_like == check_list
    for i in range(15):
        repo.delete(repo.last_pk)

"""
def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)

"""