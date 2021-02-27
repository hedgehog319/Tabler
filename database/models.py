from peewee import \
    AutoField, CharField, BooleanField, IntegerField, ForeignKeyField

from database.db import BaseModel


class Group(BaseModel):
    id = AutoField()
    name = CharField(20)

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        table_name = 'groups'


class User(BaseModel):
    user = IntegerField()
    group = ForeignKeyField(Group, related_name='groups')
    is_admin = BooleanField(default=False)

    def __str__(self):
        return f'Id: {self.user}, Group Id:{self.group}'

    class Meta:
        table_name = 'users'


class Schedule(BaseModel):
    id = AutoField()
    week_parity = BooleanField()
    week_day = IntegerField()
    pair_number = IntegerField()
    discipline_name = CharField()
    classes = CharField()
    teacher = CharField()

    def __str__(self):
        return f'{self.id} {self.week_parity} {self.week_day}' \
               f' {self.pair_number} {self.discipline_name} {self.classes} {self.teacher}'

    class Meta:
        table_name = 'schedules'


class GroupSchedule(BaseModel):
    group = ForeignKeyField(Group, related_name='groups', on_delete='CASCADE')
    schedule = ForeignKeyField(Schedule, related_name='schedules', on_delete='CASCADE')

    def __str__(self):
        return f'{self.group} {self.schedule}'


class WeekDay(BaseModel):
    id = IntegerField()
    day = CharField(20)

    def __str__(self):
        return f'Id {self.id}: {self.day}'

    class Meta:
        table_name = 'week_days'


__all__ = ['User', 'Group', 'Schedule', 'GroupSchedule', 'WeekDay']
