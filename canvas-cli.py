#!/usr/bin/python3

import calendar
import datetime
from tabulate import tabulate
import yaml
import json
import requests
import io
import sys
import argparse

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
    STRIKETHROUGH = '\033[9m'

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


# Returns course ID but presents user
# with human readable course numbers
def chooseCourse():
    courses = fetchCourseIDs()
    tableData = []
    HEADERS = ["#", "Course"]
    idDict = {}
    i = 0
    for item in courses.items():
        idDict.update({i:item})
        i = i+1
    for num in idDict.keys():
        tableData.append([num, idDict[num][0]])
    print(tabulate(tableData, headers=HEADERS, tablefmt="fancy_grid"))
    userChoice = int(input("Choose a course: "))
    return(idDict[userChoice][1])


def formatScore(assignment, percentage=False):
    pointsPossible = assignment['points_possible']
    pointsEarned = assignment['submission']['score']
    score = ''
    # Unscored assignment
    if not pointsEarned:
        return("-/"+str(pointsPossible))
    else:
        score = float(pointsEarned/pointsPossible)
        percentage = score*100

    if score >= .90:
        if percentage == True:
            scoreString = f"{bcolors.OKGREEN}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.OKGREEN}"+str(pointsEarned)+f"{bcolors.ENDC} /"+str(pointsPossible)
    elif score >= .80:
        if percentage == True:
            scoreString = f"{bcolors.OKBLUE}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.OKBLUE}"+str(pointsEarned)+f"{bcolors.ENDC} /"+str(pointsPossible)
    elif score >= .70:
        if percentage == True:
            scoreString = f"{bcolors.WARNING}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.WARNING}"+str(pointsEarned)+f"{bcolors.ENDC} /"+str(pointsPossible)
    else:
        if percentage == True:
            scoreString = f"{bcolors.FAIL}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.FAIL}"+str(pointsEarned)+f"{bcolors.ENDC} /"+str(pointsPossible)

    return(scoreString)

def formatDueDate(assignment):
        dueDateRaw = assignment['due_at']
        dueDateObject = datetime.datetime.strptime(dueDateRaw, '%Y-%m-%dT%H:%M:%SZ')
        todayObject = datetime.datetime.now()
        month = calendar.month_abbr[dueDateObject.month]
        day = str(dueDateObject.day)
        hour = str(dueDateObject.hour)
        minute = str(dueDateObject.minute)
        # assigment already submitted
        if assignment['submission']['submitted_at']:
            #  return(month+" "+day+", "+hour+":"+minute)
            return(f"{bcolors.STRIKETHROUGH}"+month+" "+day+", "+hour+":"+minute+f"{bcolors.ENDC} (DONE)")
        # assignment is late
        if assignment['submission']['late']:
            return(f"{bcolors.FAIL}"+month+" "+day+", "+hour+":"+minute+f"{bcolors.ENDC}")
        else:
            daysLeft = abs((dueDateObject - todayObject).days)
            if daysLeft >= 7:
                return(f"{bcolors.OKGREEN}"+month+" "+day+", "+hour+":"+minute+f"{bcolors.ENDC}")
            elif daysLeft >= 3:
                return(f"{bcolors.OKBLUE}"+month+" "+day+", "+hour+":"+minute+f"{bcolors.ENDC}")
            elif daysLeft >= 1:
                return(f"{bcolors.WARNING}"+month+" "+day+", "+hour+":"+minute+f"{bcolors.ENDC}")


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
        scoreString = formatScore(assignment, False)
        dueDate = formatDueDate(assignment)
        tableData.append((ID, fullName, dueDate, scoreString))
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

    args = argparse.ArgumentParser(
        description='A light-weight command-line interface for canvas.')
    args.add_argument('-list', choices=['courses', 'assignments'], help='List either courses or assignments')
    args.add_argument('-courseID', type=int, help='If you know the ID of your course, add it here to speed up the search')
    args.add_argument('-summary', action='store_true', help='print a summary of courses')
    args = args.parse_args()

    if args.list and args.list == 'courses':
        listActiveCoursesTable()

    if args.list and args.list == 'assignments':
        if args.courseID:
            listAssignmentsTable(args.courseID)
        else:
            listAssignmentsTable(chooseCourse())

    if args.summary:
        assignmentSummary()



    #  elif sys.argv[1] == "list":
        #  if len(sys.argv) < 3:
            #  printError("List What?")
        #  elif sys.argv[2] == "courses":
            #  listActiveCoursesTable()
            #  #  listActiveCourses(canvasDomain, canvasToken)
        #  elif sys.argv[2] =="assignments":
            #  if len(sys.argv) < 4:
                #  printError("Please choose a course")
                #  #  listActiveCoursesTable()
                #  #  chooseCourse()
                #  listAssignmentsTable(chooseCourse())
            #  else:
                #  listAssignmentsTable(sys.argv[3])
                #  #  listAssignments(canvasDomain, canvasToken, sys.argv[3])
    #  elif sys.argv[1] == "summary":
        #  assignmentSummary()

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

