import sqlite3
from inspect import get_annotations
from typing import Any
from datetime import datetime
from bookkeeper.repository.abstract_repository \
    import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Class for repository avaliable to SQL queries
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.cls = cls
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.last_pk = 0
        self.fields.pop('pk')
        names = ', '.join(self.fields.keys())
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            ### Create table if not exists
            query = f'CREATE TABLE IF NOT EXISTS {self.table_name} (pk, {names})'
            cur.execute(query)
        con.close()

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        placeholder = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')

            ### Create table if not exists
            query = f'CREATE TABLE IF NOT EXISTS {self.table_name} (pk, {names})'
            cur.execute(query)

            ### Retrieve PK
            cur.execute(f'SELECT * FROM {self.table_name}')
            res = cur.fetchall()
            self.last_pk = int(res[-1][0])
            pk = self.last_pk + 1

            ### Add data to table
            query = f'INSERT INTO {self.table_name} (pk, {names}) VALUES({pk}, {placeholder})'
            cur.execute(query, values)
            obj.pk = cur.lastrowid
            self.last_pk = obj.pk
        con.close()
        return obj.pk

    def build_object(self, fields: dict[str, type], values: list[Any]) -> T:
        '''
        Returns an object with specified qualities from the DB
        '''
        class_arguments = {}

        for field_name, field_value in zip(fields.keys(), values[1:]):
            field_type = fields[field_name]

            if field_type == datetime:
                field_value = datetime.strptime(field_value, "%Y-%m-%d %H:%M:%S.%f")

            class_arguments[field_name] = field_value

        obj = self.cls(**class_arguments)
        obj.pk = values[0]
        return obj

    def get(self, pk: int) -> T | None:
        """
        Получить объект по id
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'SELECT * FROM {self.table_name} WHERE pk = (?)', [pk])
            res = cur.fetchall()
        con.close()
        if res == []:
            return None
        obj = self.build_object(self.fields, res[0])
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if where is None:
                cur.execute(f'SELECT * FROM {self.table_name}')
            else:
                fields, vals = list(where.keys()), list(where.values())
                condition = ' AND '.join(f'{f} = ?' for f in fields)
                query = f'SELECT * FROM {self.table_name} WHERE ' + condition
                cur.execute(query, vals)
            res = cur.fetchall()
        con.close()
        objs = [self.get(row[0]) for row in res]
        return objs
        
    def get_all_like(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if where is None:
                cur.execute(f'SELECT * FROM {self.table_name}')
            else:
                fields, vals = list(where.keys()), list(where.values())
                condition = ' AND '.join(f'{f} LIKE ?' for f in fields)
                query = f'SELECT * FROM {self.table_name} WHERE ' + condition
                cur.execute(query, vals)
            res = cur.fetchall()
        con.close()
        objs = [self.get(row[0]) for row in res]
        return objs

    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """
        if not obj.pk:
            raise ValueError(f'Object {obj} does not have pk.')

        pk = obj.pk
        names = ', '.join(f'{f} = ?' for f in self.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        values.append(pk)

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            query = f'UPDATE {self.table_name} SET ' + names + ' WHERE pk = ?'
            cur.execute(query, values)
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить запись """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = ?', [pk])
        con.close()
        self.last_pk -= 1
