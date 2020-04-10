import yaml
import json
import requests
import io

conf = {}
# Load config file
def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def fetchActiveCourses(canvasDomain, canvasToken):
    url = canvasDomain+"api/v1/courses"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    PARAMS = {'enrollment_state':'active'}
    coursesRAW = requests.get(url, params=PARAMS, headers=HEADERS)
    courses = coursesRAW.json()
    print(len(courses))

    for course in courses:
        print(course['name'])

    #  for attr in courses[0].values():
        #  print(attr)


def fetchAssignments(canvasDomain, canvasToken, courseId):
    url = canvasDomain+"api/v1/courses/"+str(courseId)+"/assignments"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    assignmentsRAW = requests.get(url, headers=HEADERS)
    assignments = assignmentsRAW.json()
    for assignment in assignments:
        print(assignment['name'])
    return(assignments)

def main():

    # Load config file & save config file
    global conf
    with open("config.yaml", 'r') as stream:
        conf = yaml.safe_load(stream)

    canvasDomain = str(conf['default']['canvasdomain'])
    canvasToken = str(conf['default']['canvastoken'])

    courses = []
    for course in conf['courses']:
        courses.append(course)

    #  fetchAssignments(canvasDomain, canvasToken, courses[0])
    fetchActiveCourses(canvasDomain, canvasToken)

main()
