import requests

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
def fetchAssignments(courseId, canvasDomain, canvasToken):
    url = canvasDomain+"api/v1/courses/"+str(courseId)+"/assignments"
    HEADERS = {'Authorization': "Bearer "+canvasToken}
    PARAMS = {'all_dates': 1, 'include': 'submission'}
    assignmentsRAW = requests.get(url, headers=HEADERS, params=PARAMS)
    assignments = assignmentsRAW.json()
    return(assignments)


