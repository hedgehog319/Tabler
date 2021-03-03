import sys


def parse_command(command):
    if 'help' in command:
        print('help')
    elif 'migrate' in command:
        import database.models
        from database.db import db

        tables = [database.models.User, database.models.Group, database.models.WeekDay, database.models.Schedule,
                  database.models.GroupSchedule]
        db.create_tables(tables)
    elif 'start' in command:
        from bot.TablerBot import start
        start()
    elif 'createadmin' in command:
        from database.serializers import UserSerializer

        id = sys.argv[2]
        user = UserSerializer.create_or_update_group(id, '0')

        user.is_admin = True
        user.save()
    elif 'createnone' in command:
        from database.serializers import GroupSerializer
        GroupSerializer.create(id=0, name='None')
    elif 'addweekday' in command:
        from database.serializers import WeekDaySerializer

        day = sys.argv[2]
        WeekDaySerializer.create(day)
    else:
        print('unknown command')


try:
    subcommand = sys.argv[1]
except IndexError:
    subcommand = 'help'  # Display help if no arguments were given.

parse_command(subcommand)

from database.serializers import GroupSerializer
GroupSerializer.insert('None')
