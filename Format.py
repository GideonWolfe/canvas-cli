import calendar
import datetime

# ANSI escape sequences to format output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BLUE = "\033[0;34m"
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = '\033[1m'
    FADED = '\033[2m'
    UNDERLINE = '\033[4m'
    STRIKETHROUGH = '\033[9m'
    BLINK = "\033[5m"
    ITALIC = "\033[3m"
    NEGATIVE = "\033[7m"
    ENDC = '\033[0m'

def formatStatus(assignment):
    if assignment['submission']['late'] == True:
        return(f"{bcolors.FAIL}✗"+f"{bcolors.ENDC}")
    elif assignment['submission']['workflow_state'] == 'graded':
        return(f"{bcolors.OKGREEN}✓"+f"{bcolors.ENDC}")
    elif assignment['submission']['workflow_state'] == 'submitted':
        return(f"{bcolors.OKBLUE}✓"+f"{bcolors.ENDC}")
    elif assignment['submission']['workflow_state'] == 'pending_review':
        return(f"{bcolors.OKBLUE}🔎"+f"{bcolors.ENDC}")
    elif assignment['submission']['workflow_state'] == 'unsubmitted':
        return(f"{bcolors.WARNING}✗"+f"{bcolors.ENDC}")


def formatCourseScore(score, letter=False):
    if not score:
        return(" -- ")
    elif score >= 90:
        return(f"{(bcolors.OKGREEN)}"+str(score)+f"{bcolors.ENDC}")
    elif score >= 80:
        return(f"{(bcolors.OKBLUE)}"+str(score)+f"{bcolors.ENDC}")
    elif score >= 70:
        return(f"{(bcolors.YELLOW)}"+str(score)+f"{bcolors.ENDC}")
    elif score >= 60:
        return(f"{(bcolors.PURPLE)}"+str(score)+f"{bcolors.ENDC}")
    elif score >= 50:
        return(f"{(bcolors.RED)}"+str(score)+f"{bcolors.ENDC}")
    else:
        return(f"{bcolors.RED}{bcolors.BLINK}"+str(score)+f"{bcolors.ENDC}")





def formatScore(assignment, percentage=False):
    pointsPossible = assignment['points_possible']
    if 'score' not in assignment['submission'].keys():
        return("-/"+str(pointsPossible))
    pointsEarned = assignment['submission']['score']
    score = ''
    # Unscored assignment
    if not pointsEarned:
        return("-/"+str(pointsPossible))
    elif pointsPossible == 0:
            return(f"{bcolors.FADED}"+str(pointsEarned)+f"{bcolors.ENDC}/"+str(pointsPossible))
    else:
        score = float(pointsEarned/pointsPossible)
        percentage = score*100

    if score >= .90:
        if percentage == True:
            scoreString = f"{bcolors.OKGREEN}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.OKGREEN}"+str(pointsEarned)+f"{bcolors.ENDC}/"+str(pointsPossible)
    elif score >= .80:
        if percentage == True:
            scoreString = f"{bcolors.OKBLUE}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.OKBLUE}"+str(pointsEarned)+f"{bcolors.ENDC}/"+str(pointsPossible)
    elif score >= .70:
        if percentage == True:
            scoreString = f"{bcolors.WARNING}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.WARNING}"+str(pointsEarned)+f"{bcolors.ENDC}/"+str(pointsPossible)
    else:
        if percentage == True:
            scoreString = f"{bcolors.FAIL}"+str(percentage)+f"%{bcolors.ENDC}"
        else:
            scoreString = f"{bcolors.FAIL}"+str(pointsEarned)+f"{bcolors.ENDC}/"+str(pointsPossible)

    return(scoreString)

def formatDueDate(assignment):
    try:
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
            return(f"{bcolors.FADED}"+month+" "+day+", "+hour+":"+minute+f"{bcolors.ENDC}")
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
    except:
        return("--")


