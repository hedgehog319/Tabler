from database.models import *


class GroupSerializer:
    @staticmethod
    def get_groups():
        res = [group for group in Group.select()]
        return res

    @staticmethod
    def get_group(name) -> Group:
        return Group.get_or_none(name=name)

    @staticmethod
    def get_or_create(name):
        return Group.get_or_create(name=name)[0]

    @staticmethod
    def insert(name):
        return Group.create(name=name)


class ScheduleSerializer:
    @staticmethod
    def get_schedule_by_id(id) -> Schedule:
        return Schedule.get_by_id(id)

    @staticmethod
    def create(**kwargs):
        week_parity = kwargs['week_parity']
        week_day = WeekDaySerializer.get_id(kwargs['week_day'])
        pair_number = kwargs['pair_number']
        discipline_name = kwargs['discipline_name']
        classes = kwargs['classes']
        teacher = kwargs['teacher']

        return Schedule.create(week_parity=week_parity, week_day=week_day, pair_number=pair_number,
                               discipline_name=discipline_name, classes=classes, teacher=teacher)


class GroupScheduleSerializer:
    @staticmethod
    def get_schedule(group_id, week_parity, week_day) -> []:
        schedule = Schedule.select().join(GroupSchedule).where(GroupSchedule.group == group_id,
                                                               Schedule.week_parity == week_parity,
                                                               Schedule.week_day == week_day).execute()
        day_schedule = []
        for pair in schedule:
            day_schedule.append({
                "pair_number": pair.pair_number,
                "discipline": pair.discipline_name,
                "classes": pair.classes,
                "teacher": pair.teacher
            })
        return day_schedule

    @staticmethod
    def create(**kwargs) -> GroupSchedule:
        group = kwargs['group_id']
        schedule = kwargs['schedule_id']
        return GroupSchedule.create(group=group, schedule=schedule)

    @staticmethod
    def clear_schedule(group_id) -> int:
        schedules = Schedule.select(Schedule.id).join(GroupSchedule).where(GroupSchedule.group == group_id)
        for schedule in schedules:
            schedule.delete_instance()

        return len(schedules)

    # Don't use
    @staticmethod
    def create_or_update(group_id, **kwargs):
        week_parity = kwargs['week_parity']
        week_day = WeekDaySerializer.get_id(kwargs['week_day'])
        pair_number = kwargs['pair_number']
        discipline_name = kwargs['discipline_name']
        classes = kwargs['classes']
        teacher = kwargs['teacher']

        schedule = Schedule.select().join(GroupSchedule).where(GroupSchedule.group == group_id,
                                                               Schedule.week_parity == week_parity,
                                                               Schedule.week_day == week_day,
                                                               Schedule.pair_number == pair_number).first()
        if schedule is not None:
            schedule.pair_number = pair_number
            schedule.discipline_name = discipline_name
            schedule.classes = classes
            schedule.teacher = teacher

            schedule.save()
        else:
            schedule = ScheduleSerializer.create(**kwargs)
            GroupScheduleSerializer.create(group=group_id, schedule=schedule.id)

    @staticmethod
    def delete(group_id, week_parity, week_day, pair_number) -> bool:
        week_day = WeekDaySerializer.get_id(week_day)
        schedule = Schedule.select(Schedule.id).join(GroupSchedule).where(GroupSchedule.group == group_id,
                                                                          Schedule.week_parity == week_parity,
                                                                          Schedule.pair_number == pair_number,
                                                                          Schedule.week_day == week_day).first()
        if schedule is None:
            return False

        schedule.delete_instance()
        return True


class UserSerializer:
    @staticmethod
    def get_group(user_id):
        return User.select().where(User.user == user_id).first().group

    @staticmethod
    def create_or_update_group(user_id, group_id):
        user = User.get_or_none(user=user_id)
        if user is None:
            user = User.create(user=user_id, group=group_id)
        else:
            user.group = group_id
            user.save()

        return user

    @staticmethod
    def is_user(user_id):
        user = User.select().where(User.user == user_id).first()
        return user is not None

    @staticmethod
    def is_admin(user_id):
        user = User.select().where(User.user == user_id).first()

        if user is None:
            return False
        return user.is_admin


class WeekDaySerializer:
    @staticmethod
    def get_id(day):
        day = WeekDay.get_or_none(WeekDay.day == day)
        if day is None:
            return -1
        else:
            return day.id

    @staticmethod
    def get_name(id):
        day = WeekDay.get_or_none(WeekDay.id == id)
        if day is None:
            return None
        else:
            return day.day

    @staticmethod
    def create(name):
        return WeekDay.create(id=1, day=name)
