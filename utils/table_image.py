import pandas as pd
from database.serializers import GroupScheduleSerializer


def pd_test() -> str:
    df = pd.DataFrame(columns=['Пара', 'Аудитория', 'Преподаватель'], index=[i for i in range(1, 6)])

    df['Пара'][1] = 'c++'
    df['Аудитория'][1] = '75D'
    df['Преподаватель'][1] = 'Иванов И.И.'

    # return df.dropna()
    df = df.dropna()
    return df.to_html(escape=False)


def test1():
    _schedule = GroupScheduleSerializer.get_schedule(2, True, 2)

    for pair in _schedule:
        print(pair)
