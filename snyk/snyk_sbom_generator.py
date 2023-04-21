#!/usr/bin/python3
# Author: Robert Marion
# Date: 2023
# License: MIT
# PoC to create SBOM from Snyk
# an org can contain one or more projects
# a project is dependencies:'projects', excluding those beginning with '@' and everything preceding ':'
# a report is a list of name-version components (and properties: licenses, copyrights) per project
#
import requests
import json
from pprint import pprint

SNYK_BASE_URL = "https://snyk.io/api/v1/org/"
CONFIG_FILE = "./sbom_generator.json"


def main():
    config = get_config()
    HEADER = {'content-type':'application/json; charset=utf-8','Authorization':'token ' + config['snyk_api_token']}
    get_dependencies_url = SNYK_BASE_URL + config['organization_token'] + '/' + 'dependencies' + '?page=1&perPage=500'

    result = requests.post(get_dependencies_url, headers=HEADER)
    if result.status_code != 200:
        exit(f"Unable to make Snyk request. Error code {result.status_code}")

    deps = json.loads(result.text)   
    reports = get_json_report(deps, config['report_name'])
    pprint(reports)
    

def get_json_report(deps, project_name):
    report = {
    "report":"",
    "name":"",
    "version":"",
    "copyright":"",
    "license":""
    }
    reports = []
    print(project_name)
    for row in deps['results']:
        for proj in row['projects']:
            if  proj['name'].find(project_name) != -1: 
                report['report'] = project_name
                report['name'] = row['name']
                report['version'] = row['version']
                report['copyright'] = [c for c in row['copyright']]
                for license in row['licenses']:
                    report['license'] = license['license']
                reports.append(dict(report))
    return reports
            

#Not used but can return a list of Snyk monitored repos in an Org
def get_project_list(deps):
    projects = set()
    for row in deps['results']:
        for proj in row['projects']:
            if '@' not in proj['name']:
                #remove anything after a colon
                projects.add(proj['name'][0:proj['name'].find(':')])
    return list(projects)


def get_config():
    try:
        with open(CONFIG_FILE) as config:
            config = json.load(config)
    except:
        print("Unable to open config file. Quitting")
        exit()
    return(config)

if __name__ == "__main__":
    main()