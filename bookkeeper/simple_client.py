"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.utils import read_tree
from bookkeeper.repository.sqlite_repository import SQLiteRepository
import os

cwd = os.getcwd()

db_file = os.path.join(cwd, 'bookkeeper', 'repository', 'test_db.db')
cat_repo = SQLiteRepository(db_file=db_file, cls=Category)
exp_repo = SQLiteRepository(db_file=db_file, cls=Expense)

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

print('ADD')
#Category.create_from_tree(read_tree(cats), cat_repo)

print('GET')
print(cat_repo.get(5))

print('GET ALL')
print(*cat_repo.get_all(), sep='\n')
print('GET ALL WHERE')
print(*cat_repo.get_all({'parent': 1}), sep='\n')

print('UPDATE')
obj = Category(name='одежда', parent=1, pk=7)
cat_repo.update(obj)
print(*cat_repo.get_all(), sep='\n')
obj = Category(name='одежда', parent=None, pk=7)
print(*cat_repo.get_all(), sep='\n')

print('DELETE')
obj = Category(name='обувь', parent=None)
cat_repo.add(obj)
print(*cat_repo.get_all(), sep='\n')
cat_repo.delete(pk=8)
print(*cat_repo.get_all(), sep='\n')

"""
while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
"""
