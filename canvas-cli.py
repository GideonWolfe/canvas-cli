import yaml
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


def fetchAssignments(canvasDomain, courseId):
    url = canvasDomain+"api/v1/courses/"+str(courseId)+"/assignments"
    assignments = requests.get(url)
    print(assignments.text)

def main():

    # Load config file & save config file
    global conf
    with open("config.yaml", 'r') as stream:
        conf = yaml.safe_load(stream)

    canvasDomain = str(conf['default']['canvasdomain'])
    print("Domain: "+canvasDomain)

    courses = []
    for course in conf['courses']:
        courses.append(course)

    fetchAssignments(canvasDomain, courses[0])

main()
