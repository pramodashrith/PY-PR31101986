#!/usr/bin/env python3
'''
Script to backup and restore Jenkins Jobs
'''
from argparse import ArgumentParser
from os import environ as env, listdir, makedirs as mkdir, path
import sys

import requests
from py_dotenv import read_dotenv


def argument_parser():
    '''
    Creating argument parser
    '''
    parser = ArgumentParser(description="Backup and restore Jenkins jobs")
    mutually_exclusive = parser.add_mutually_exclusive_group(required=True)
    mutually_exclusive.add_argument('-b', '--backup', action='store_true',
                                    help="backup jobs")
    mutually_exclusive.add_argument('-r', '--restore', metavar='job',
                                    help="restore a backed up job")
    mutually_exclusive.add_argument('-R', '--restore-all', action='store_true',
                                    help="restore all backed up jobs")
    return parser


def load_env_var(var_name):
    '''
    tries to load one env var
    returns the content if found
    '''
    try:
        return env[var_name]
    except KeyError as k:
        err_str = 'Unable to read variable {} from environment'
        err_str += '\nPlease add {} variable to your .env file to run this '
        err_str += 'program'
        print(err_str.format(k, k))
        sys.exit(1)


def load_env_vars():
    '''
    tries to load required env vars for the program to run
    returns them if found
    '''
    dotenv_path = path.join(path.dirname(__file__), '.env')
    try:
        read_dotenv(dotenv_path)
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(2)
    json_api_path = load_env_var('JSON_API_PATH')
    jenkins_url = load_env_var('JENKINS_URL')
    user = load_env_var('USERNAME')
    api_token = load_env_var('API_TOKEN')
    return (jenkins_url, json_api_path, user, api_token)


def get_jobs(jenkins_main_url):
    '''
    gets and returns a json with the jobs from jenkins
    '''
    jobs = {}
    answer = requests.get(jenkins_main_url, verify=False).json()['jobs']
    for ans in answer:
        jobs[ans['name']] = ans['url']
    return jobs


def get_config(url, user, api_token):
    '''
    Load configuration variables
    '''
    rns = requests.get(url, auth=(user, api_token), verify=False)
    return rns.text


def backup_jobs(jenkins_url, json_api_path, user, api_token):
    '''
    jobs backup
    '''
    jobs = get_jobs(jenkins_url + json_api_path)
    mkdir('jobs', exist_ok=True)
    for name in jobs:
        print('Backing up {}'.format(name))
        mkdir('jobs/{}'.format(name), exist_ok=True)
        config_xml = get_config('{}/config.xml'.format(jobs[name]),
                                user, api_token)
        print(config_xml, file=open('jobs/{}/config.xml'.format(name), "w"))
        print('Job {} successfully backed up'.format(name))


def restore_job(name, jenkins_url, user, api_token):
    '''
    job restoration
    '''
    print('Restoring job {}'.format(name))
    with open('jobs/{}/config.xml'.format(name), 'r') as myfile:
        xml_data = myfile.read()
    headers = {'Content-Type': 'application/xml'}
    url = '{}/createItem?name={}'.format(jenkins_url, name)
    result = requests.post(url, auth=(user, api_token), verify=False,
                           data=xml_data, headers=headers)
    if result.status_code != 200:
        url = '{}/job/{}/config.xml'.format(jenkins_url, name)
        result = requests.post(url, auth=(user, api_token), verify=False,
                               data=xml_data, headers=headers)
        if result.status_code != 200:
            print('Something went wrong, status code: {}'
                  .format(result.status_code))
    print('Job {} successfully restored'.format(name))


def restore_all(jenkins_url, user, api_token):
    '''
    Restore all jobs
    '''
    for job in listdir('jobs'):
        restore_job(job, jenkins_url, user, api_token)


def main():
    '''
    main function
    '''
    requests.packages.urllib3.disable_warnings()
    parser = argument_parser().parse_args()
    jenkins_url, json_api_path, user, api_token = load_env_vars()
    if parser.backup:
        backup_jobs(jenkins_url, json_api_path, user, api_token)
    elif parser.restore_all:
        restore_all(jenkins_url, user, api_token)
    else:
        restore_job(parser.restore, jenkins_url, user, api_token)


if __name__ == "__main__":
    main()