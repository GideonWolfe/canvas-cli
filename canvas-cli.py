import yaml
import json
import requests
import io
import sys

conf = {}
# Load config file
def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

# Returns a JSON array with the users active courses
def fetchActiveCourses(canvasDomain, canvasToken):
    url = canvasDomain+"api/v1/courses"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    PARAMS = {'enrollment_state':'active', 'exclude_blueprint_courses':'true'}
    coursesRAW = requests.get(url, params=PARAMS, headers=HEADERS)
    courses = coursesRAW.json()
    return(courses)

# Returns a JSON array of assignments for a given course
def fetchAssignments(canvasDomain, canvasToken, courseId):
    url = canvasDomain+"api/v1/courses/"+str(courseId)+"/assignments"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    assignmentsRAW = requests.get(url, headers=HEADERS)
    assignments = assignmentsRAW.json()
    return(assignments)

def listAssignments(canvasDomain, canvasToken, courseId):
    assignments = fetchAssignments(canvasDomain, canvasToken, courseId)
    for assignment in assignments:
        print(assignment['name'])

def listActiveCourses(canvasDomain, canvasToken):
    courses = fetchActiveCourses(canvasDomain, canvasToken)
    for course in courses:
        print(course['name'])

def parseArgs():

    canvasDomain = str(conf['default']['canvasdomain'])
    canvasToken = str(conf['default']['canvastoken'])
    courses = []
    for course in conf['courses']:
        courses.append(course)


    if len(sys.argv) <= 1:
        print("No arguments supplied")
    elif sys.argv[1] == "list":
        if len(sys.argv) < 3:
            print("List what?")
        elif sys.argv[2] == "courses":
            print("Listing courses")
            listActiveCourses(canvasDomain, canvasToken)
        elif sys.argv[2] =="assignments":
            if len(sys.argv) < 4:
                print("Please supply a course ID")
            else:
                listAssignments(canvasDomain, canvasToken, courses[0])

def main():
    # Load config file & save config file
    global conf
    with open("config.yaml", 'r') as stream:
        conf = yaml.safe_load(stream)

    parseArgs()




main()
