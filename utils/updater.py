import io
import xlrd

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
from settings import CREDENTIALS_FILE, FILE_ID, SCHEDULE_NAME

from database.serializers import GroupSerializer, GroupScheduleSerializer


def download_schedules():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/drive.readonly'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=httpAuth)

    request = service.files().export_media(fileId=FILE_ID,
                                           mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fh = io.FileIO(SCHEDULE_NAME, 'wb')
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.close()


def update_schedules():
    rb = xlrd.open_workbook(SCHEDULE_NAME)
    for sheet in rb.sheets():
        update_group_schedule(sheet)


def update_group_schedule(sheet):
    group_id = GroupSerializer.get_or_create(sheet.name).id
    GroupScheduleSerializer.clear_schedule(group_id)

    days = [sheet.col_values(i) for i in range(sheet.ncols)]
    days.pop(0)

    for day in days:
        update_day_schedule(group_id, day)


def update_day_schedule(group_id, day):
    week_day = day[0]
    week_parity = day[1] == 'Числитель'

    for i in range(2, len(day)):
        pair_number = i - 1
        if day[i] != '':
            discipline_name, teacher, classes = day[i].replace('\n', '').split(';')
            GroupScheduleSerializer.create_or_update(group_id, week_parity=week_parity, week_day=week_day,
                                                     pair_number=pair_number, discipline_name=discipline_name,
                                                     classes=classes, teacher=teacher)
        else:
            GroupScheduleSerializer.delete(group_id, week_parity, week_day, pair_number)
