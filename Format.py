import calendar
import datetime

# ANSI escape sequences to format output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    FADED = '\033[2m'
    UNDERLINE = '\033[4m'
    STRIKETHROUGH = '\033[9m'

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


