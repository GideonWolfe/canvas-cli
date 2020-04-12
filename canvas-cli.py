#!/usr/bin/python3

from tabulate import tabulate
import yaml
import json
import requests
import io
import sys

# ANSI escape sequences to format output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


conf = {}
# Load config file
def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def printError(errorMessage):
    print(f"{bcolors.WARNING}ERROR:{bcolors.ENDC} " + errorMessage)



# Returns a JSON array with the users active courses
def fetchActiveCourses(canvasDomain, canvasToken):
    url = canvasDomain+"api/v1/courses"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    PARAMS = {'enrollment_state':'active',
              'include': 'course_progress',
              'exclude_blueprint_courses':'true'}
    coursesRAW = requests.get(url, params=PARAMS, headers=HEADERS)
    courses = coursesRAW.json()
    return(courses)

# Returns dictionary of courseID and courseName
def fetchCourseIDs(canvasDomain, canvasToken):
    courses = fetchActiveCourses(canvasDomain, canvasToken)
    courseIds = {}
    for course in courses:
        # Remove stray ended courses
        if not course['end_at']:
            courseIds.update({course['name']:course['id']})
    return(courseIds)

# Returns a JSON array of assignments for a given course
def fetchAssignments(canvasDomain, canvasToken, courseId):
    url = canvasDomain+"api/v1/courses/"+str(courseId)+"/assignments"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    assignmentsRAW = requests.get(url, headers=HEADERS)
    assignments = assignmentsRAW.json()
    return(assignments)

# Prints list of assignments for a given course
def listAssignments(canvasDomain, canvasToken, courseId, summary=False):
    assignments = fetchAssignments(canvasDomain, canvasToken, courseId)
    for assignment in assignments:
        if summary:
            print(" • "+assignment['name'])
        else:
            print(assignment['name'])

# Prints list of assignments for a given course
def listAssignmentsTable(canvasDomain, canvasToken, courseId):
    assignments = fetchAssignments(canvasDomain, canvasToken, courseId)
    tableData = []
    HEADERS=["ID", "Name"]
    for assignment in assignments:
        fullName = assignment['name']
        ID = assignment['id']
        tableData.append((ID, fullName))
    print(tabulate(tableData, headers=HEADERS, tablefmt="fancy_grid"))

# Prints a list of active courses
def listActiveCourses(canvasDomain, canvasToken):
    courses = fetchActiveCourses(canvasDomain, canvasToken)
    for course in courses:
        fullName = course['name']
        courseId = course['id']
        endDate = course['end_at']
        if not endDate:
            print("[ID: "+str(courseId)+"] "+fullName)

# Prints a list of active courses in a table
def listActiveCoursesTable(canvasDomain, canvasToken):
    courses = fetchActiveCourses(canvasDomain, canvasToken)
    tableData = []
    HEADERS=["ID", "Name"]
    for course in courses:
        fullName = course['name']
        courseId = course['id']
        endDate = course['end_at']
        if not endDate:
            tableData.append((courseId, fullName))
    print(tabulate(tableData, headers=HEADERS, tablefmt="fancy_grid"))


# Prints a list of active courses and their outstanding assignments
def assignmentSummary(canvasDomain, canvasToken):
    courses = fetchCourseIDs(canvasDomain, canvasToken)
    #  print(courses.keys())
    for course in courses:
        print("\u0332".join(course))
        listAssignments(canvasDomain, canvasToken, courses[course], True)

def parseArgs():

    canvasDomain = str(conf['default']['canvasdomain'])
    canvasToken = str(conf['default']['canvastoken'])
    courses = fetchCourseIDs(canvasDomain, canvasToken).keys

    if len(sys.argv) <= 1:
        print("No arguments supplied")
    elif sys.argv[1] == "list":
        if len(sys.argv) < 3:
            printError("List What?")
        elif sys.argv[2] == "courses":
            print("Listing courses")
            listActiveCoursesTable(canvasDomain, canvasToken)
            #  listActiveCourses(canvasDomain, canvasToken)
        elif sys.argv[2] =="assignments":
            if len(sys.argv) < 4:
                printError("Please supply a course ID")
                listActiveCoursesTable(canvasDomain, canvasToken)
            else:
                listAssignmentsTable(canvasDomain, canvasToken, sys.argv[3])
                #  listAssignments(canvasDomain, canvasToken, sys.argv[3])
    elif sys.argv[1] == "summary":
        assignmentSummary(canvasDomain, canvasToken)

def main():
    # Load config file & save config file
    global conf
    with open("config.yaml", 'r') as stream:
        conf = yaml.safe_load(stream)

    parseArgs()


if __name__ == "__main__":
    main()

