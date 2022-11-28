from simplexml import dumps
from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from src import api
from src.models import DriverInfo, db


def output_xml(data, code, headers=None):
    resp = make_response(dumps({'response': data}), code)
    resp.headers['Accept'] = 'application/xml'
    return resp


api.representations['application/xml'] = output_xml

parser = reqparse.RequestParser()


class CommonStatistics(Resource):
    def get(self):
        with db:
            args = parser.parse_args()
            resp_format = args.get('resp_format')
            drivers_stats = DriverInfo.select()
            if resp_format == 'json':
                output = []
                for driver in drivers_stats:
                    driver_data = {'place': driver.place, 'name': driver.full_name,
                                   'car': driver.car, 'time': driver.time}
                    output.append(driver_data)
                return jsonify(output)
            elif resp_format == 'xml':
                output = []
                driver_tag = {}
                for driver in drivers_stats:
                    driver_data = {'place': driver.place, 'name': driver.full_name,
                                   'car': driver.car, 'time': driver.time}
                    driver_tag['driver'] = driver_data
                    output.append(driver_tag)
                return output


api.add_resource(CommonStatistics, '/api/v1/report/')


parser.add_argument('driver_id', type=str, location='args')
parser.add_argument('order', type=str, location='args')
parser.add_argument('resp_format', type=str, location='args')


class DriversStatistics(Resource):
    def get(self):

        args = parser.parse_args()
        order = args.get('order')
        driver_id = args.get('driver_id')
        resp_format = args.get('resp_format')
        output = []

        with db:
            if driver_id:
                driver_id = driver_id.upper()

            if not order and not args.driver_id:
                drivers_stats = DriverInfo.select()
                if resp_format == 'json':
                    for driver in drivers_stats:
                        driver_statistics = {'driver_id': driver.driver_id, 'name': driver.full_name, 'car': driver.car}
                        output.append(driver_statistics)
                elif resp_format == 'xml':
                    drivers_stats = DriverInfo.select()
                    driver_tag = {}
                    for driver in drivers_stats:
                        driver_statistics = {'driver_id': driver.driver_id, 'name': driver.full_name, 'car': driver.car}
                        driver_tag['driver'] = driver_statistics
                        output.append(driver_tag)

            elif order == 'asc':
                drivers_stats = DriverInfo.select()
                if resp_format == 'json':
                    for driver in drivers_stats:
                        driver_data = {'place': driver.place, 'name': driver.full_name, 'car': driver.car,
                                       'time': driver.time}
                        output.append(driver_data)

                elif resp_format == 'xml':
                    for driver in drivers_stats:
                        driver_data = {'place': driver.place, 'name': driver.full_name,
                                       'car': driver.car, 'time': driver.time}
                        output.append(driver_data)

            elif order == 'desc':
                drivers_stats = DriverInfo.select()
                if resp_format == 'json':
                    for driver in drivers_stats:
                        driver_data = {'place': driver.place, 'name': driver.full_name,
                                       'car': driver.car, 'time': driver.time}
                        output.append(driver_data)
                    output = output[::-1]
                elif resp_format == 'xml':
                    driver_tag = {}
                    drivers_stats = drivers_stats[::-1]
                    for driver in drivers_stats:
                        driver_data = {'place': driver.place, 'name': driver.full_name,
                                       'car': driver.car, 'time': driver.time}
                        driver_tag['driver'] = driver_data
                        output.append(driver_tag)

            elif driver_id:  # if driver_id == None,driver_id.upper() raise an err.
                driver_stats = DriverInfo.select().where(DriverInfo.driver_id == driver_id)
                for driver in driver_stats:
                    output = {'place': driver.place, 'name': driver.full_name,
                              'car': driver.car, 'time': driver.time}

            else:
                output = 'Bad request'

            if resp_format == 'json':
                return jsonify(output)
            else:
                return output


api.add_resource(DriversStatistics, '/api/v1/report/drivers/')
