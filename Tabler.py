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
        print('start')
    else:
        print('unknown command')


try:
    subcommand = sys.argv[1]
except IndexError:
    subcommand = 'help'  # Display help if no arguments were given.

parse_command(subcommand)
