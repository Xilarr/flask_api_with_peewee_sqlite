from peewee import *

db = SqliteDatabase('../src/db/database.db')


class DriverInfo(Model):
    id = AutoField(unique=True)
    place = IntegerField()
    full_name = CharField()
    car = CharField()
    time = DateTimeField()
    driver_id = CharField()

    class Meta:
        table_name = 'DriversInfo'
        database = db
        order_by = 'place'

