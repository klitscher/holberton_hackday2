#!/usr/bin/env python3


import requests
import sys
import time
import getpass


def LOTC(hbtn_email, password, api_key):
    # if len(sys.argv) != 4:
    #     print("Usage: ./python.py '<email>'"
    #           "'<api_key>' '<project_number>")
    # password = getpass.getpass('Password: ')
    my_dict = {'email': hbtn_email, 'password': password,
               'api_key': api_key, 'scope': 'checker'}

    try:
        auth_token = requests.post(
            'https://intranet.hbtn.io/users/auth_token.json',
            data=my_dict).json()['auth_token']
    except KeyError:
        print('Please enter the correct credentials')
        exit()
    project = requests.get(
        'https://intranet.hbtn.io/projects/{}.json?auth_token={}'.format(
            sys.argv[3], auth_token))
    task_id_list = []
    task_title_list = []
    for task in project.json()['tasks']:
        task_id_list.append(task['id'])
        task_title_list.append(task['title'])

    for count, task_id in enumerate(task_id_list):
        print('\x1b[1m' + 'Task: {} Title: {}'.format(
            count, task_title_list[count]) + '\x1b[0m')
        correction_request_url = 'https://intranet.hbtn.io/tasks/{}/' \
                                 'start_correction.json?auth_token={}'.format(
                                     task_id, auth_token)
        correction_id = requests.post(correction_request_url).json()['id']
        correction_result_url = 'https://intranet.hbtn.io/' \
                                'correction_requests/' \
                                '{}.json?auth_token={}'.format(
                                    correction_id, auth_token)
        correction_result = requests.get(correction_result_url).json()
        delay = 0
        while len(correction_result['result_display']['checks']) == 0:
            delay += 5
            time.sleep(delay)
            correction_result = requests.get(correction_result_url).json()
        for check_info in correction_result['result_display']['checks']:
            print('{}, {} check'.format(
                check_info.get('title'), check_info.get('check_label')))
            if check_info.get('passed') is True:
                print('\x1b[;37;42m' + 'You pass!' + '\x1b[0m')
            else:
                print('\x1b[5;37;41m' +
                      'Fail: You must be from San Francisco or Bogota' +
                      '\x1b[0m')
        print()
