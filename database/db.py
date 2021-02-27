from peewee import Model

from settings import DATABASE

db = None

if DATABASE['ENGINE'] == 'postgres':
    from peewee import PostgresqlDatabase

    db = PostgresqlDatabase(database=DATABASE['NAME'], user=DATABASE['USER'], password=DATABASE['PASSWORD'])
elif DATABASE['ENGINE'] == 'sqlite3':
    from peewee import SqliteDatabase

    db = SqliteDatabase(DATABASE['NAME'])
else:
    print('Unknown engine')
    raise Exception


class BaseModel(Model):
    class Meta:
        database = db
