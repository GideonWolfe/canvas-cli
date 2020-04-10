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
        courseIds.update({course['name']:course['id']})
        #  courseIds['name'] = course['name']
        #  courseIds['id'] = course['id']
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

# Prints a list of active courses
def listActiveCourses(canvasDomain, canvasToken):
    courses = fetchActiveCourses(canvasDomain, canvasToken)
    for course in courses:
        fullName = course['name']
        courseId = course['id']
        endDate = course['end_at']
        if not endDate:
            print("[ID: "+str(courseId)+"] "+fullName)

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
            #  print("\033[4mList what?\033[0m")
            print("\u0332".join("List What?"))
            print("courses")
            print("assignments <course id>")
        elif sys.argv[2] == "courses":
            print("Listing courses")
            listActiveCourses(canvasDomain, canvasToken)
        elif sys.argv[2] =="assignments":
            if len(sys.argv) < 4:
                print("Please supply a course ID")
                listActiveCourses(canvasDomain, canvasToken)
            else:
                listAssignments(canvasDomain, canvasToken, sys.argv[3])
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

