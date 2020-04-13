#!/usr/bin/python3

import calendar
import datetime
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

# Global Variables
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
def fetchActiveCourses():
    url = canvasDomain+"api/v1/courses"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    PARAMS = {'enrollment_state':'active',
              'include': 'course_progress',
              'exclude_blueprint_courses':'true'}
    coursesRAW = requests.get(url, params=PARAMS, headers=HEADERS)
    courses = coursesRAW.json()
    return(courses)

# Returns dictionary of courseID and courseName
def fetchCourseIDs():
    courses = fetchActiveCourses()
    courseIds = {}
    for course in courses:
        # Remove stray ended courses
        if not course['end_at']:
            courseIds.update({course['name']:course['id']})
    return(courseIds)

# Returns a JSON array of assignments for a given course
def fetchAssignments(courseId):
    url = canvasDomain+"api/v1/courses/"+str(courseId)+"/assignments"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    PARAMS = {'all_dates': 1, 'include': 'submission'}
    assignmentsRAW = requests.get(url, headers=HEADERS, params=PARAMS)
    assignments = assignmentsRAW.json()
    return(assignments)

# Prints list of assignments for a given course
def listAssignments(courseId, summary=False):
    assignments = fetchAssignments(courseId)
    for assignment in assignments:
        if summary:
            print(" • "+assignment['name'])
        else:
            print(assignment['name'])

# Prints list of assignments for a given course
def listAssignmentsTable(courseId):
    assignments = fetchAssignments(courseId)
    tableData = []
    HEADERS=["ID", "Name", "Due Date", "Score"]
    for assignment in assignments:
        fullName = assignment['name']
        ID = assignment['id']
        pointsPossible = assignment['points_possible']
        pointsEarned = assignment['submission']['score']
        if not pointsEarned:
            pointsEarned = '-'
        dueDateRaw = assignment['due_at']
        dateTimeObject = datetime.datetime.strptime(dueDateRaw, '%Y-%m-%dT%H:%M:%SZ')
        dueDate = calendar.month_abbr[dateTimeObject.month]+" "+str(dateTimeObject.day)+", "+str(dateTimeObject.hour)+":"+str(dateTimeObject.minute)
        tableData.append((ID, fullName, dueDate, str(pointsEarned)+"/"+str(pointsPossible)))
    print(tabulate(tableData, headers=HEADERS, tablefmt="fancy_grid"))

# Prints a list of active courses
def listActiveCourses():
    courses = fetchActiveCourses()
    for course in courses:
        fullName = course['name']
        courseId = course['id']
        endDate = course['end_at']
        if not endDate:
            print("[ID: "+str(courseId)+"] "+fullName)

# Prints a list of active courses in a table
def listActiveCoursesTable():
    courses = fetchActiveCourses()
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
def assignmentSummary():
    courses = fetchCourseIDs()
    #  print(courses.keys())
    for course in courses:
        print("\u0332".join(course))
        listAssignments(courses[course], True)

def parseArgs():

    #  canvasDomain = str(conf['default']['canvasdomain'])
    #  canvasToken = str(conf['default']['canvastoken'])
    courses = fetchCourseIDs().keys

    if len(sys.argv) <= 1:
        print("No arguments supplied")
    elif sys.argv[1] == "list":
        if len(sys.argv) < 3:
            printError("List What?")
        elif sys.argv[2] == "courses":
            listActiveCoursesTable()
            #  listActiveCourses(canvasDomain, canvasToken)
        elif sys.argv[2] =="assignments":
            if len(sys.argv) < 4:
                printError("Please supply a course ID")
                listActiveCoursesTable()
            else:
                listAssignmentsTable(sys.argv[3])
                #  listAssignments(canvasDomain, canvasToken, sys.argv[3])
    elif sys.argv[1] == "summary":
        assignmentSummary()

def main():

    # Declare global variables
    global conf
    global canvasToken
    global canvasDomain

    # Load config file & save config file
    with open("config.yaml", 'r') as stream:
        conf = yaml.safe_load(stream)

    canvasDomain = str(conf['default']['canvasdomain'])
    canvasToken = str(conf['default']['canvastoken'])


    parseArgs()


if __name__ == "__main__":
    main()

