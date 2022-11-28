import argparse
import datetime
import operator
from datetime import datetime, timedelta


def build_report(folders_path):

    start_dict = make_dict(folders_path + '/start.log')
    end_dict = make_dict(folders_path + '/end.log')
    abb_dict = make_dict(folders_path + '/abbreviations.txt')

    time_dict = calculate_time(start_dict, end_dict)

    report_list = make_result_list(time_dict, abb_dict)
    return report_list


def make_dict(file_path):
    with open(file_path) as file:
        str_list = file.read().split('\n')
    full_dict = {}
    for string in str_list:
        str_dict = ({string[:3]: string[3:]})
        full_dict.update(str_dict)
    return full_dict


def calculate_time(start_dict, end_dict):
    keys = start_dict.keys()
    time_dict = {}
    for key in keys:
        try:
            start_datetime = datetime.strptime(start_dict.get(key), "%Y-%m-%d_%H:%M:%S.%f")
            end_datetime = datetime.strptime(end_dict.get(key), "%Y-%m-%d_%H:%M:%S.%f")
            difference_dict = {key: (abs((end_datetime - start_datetime).total_seconds()))}
            time_dict.update(difference_dict)
        except ValueError:
            pass
    sorted_time_dict = dict(sorted(time_dict.items(), key=operator.itemgetter(1)))

    return sorted_time_dict


def make_result_list(time_dict, abb_dict):
    keys = time_dict.keys()
    digit = 0
    report_list = []

    for key in keys:
        driver_list = []
        digit += 1
        name_and_car = abb_dict.get(key).split('_')
        final_time = str(timedelta(seconds=time_dict.get(key)))[:-3]
        driver_list.append(str(digit))
        driver_list.append(name_and_car[1])
        driver_list.append(name_and_car[2])
        driver_list.append(final_time)
        driver_list.append(key)
        # report_list.append(f'{digit}. {name_and_car[1] + gap1} | {name_and_car[2] + gap2} | {final_time}')
        report_list.append(driver_list)

    return report_list


def print_report(report_list):

    if args.asc:
        for driver in report_list:
            try:
                print(driver)
            except ValueError:
                pass
    elif args.desc:
        for driver in reversed(report_list):
            try:
                print(driver)
            except ValueError:
                pass
    elif args.driver:
        for driver in report_list:
            if args.driver in driver:
                print(driver)
            else:
                pass


def report():
    folder = args.file

    report_list = build_report(folder)
    print_report(report_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str)
    parser.add_argument("--asc", action='store_true')
    parser.add_argument("--desc", action='store_true')
    parser.add_argument("--driver", type=str)
    args = parser.parse_args()
    report()
