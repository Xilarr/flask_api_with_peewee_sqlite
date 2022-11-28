from src.models import DriverInfo, db
from src.config import FOLDER_PATH
from src.report import build_report

with db:
    db.create_tables([DriverInfo])

    drivers_info = []
    for note in build_report(FOLDER_PATH):
        drivers_info.append({'place': note[0], 'full_name': note[1], 'car': note[2], 'time': note[3], 'driver_id': note[4]})

    DriverInfo.insert_many(drivers_info).execute()
