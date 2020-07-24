options = {
    "cookies":{
        "JSESSIONID": "F54263E662CD279F253567CF57F782B6"
    }
}


from jira import JIRA
import re
import dateutil.parser
from openpyxl import Workbook

def searchIssues(jql,fields,block_size=1000):
    all_issues = []

    block_num = 0
    while True:
        start_idx = block_num * block_size
        issues = jira.search_issues(
            jql,
            start_idx,
            block_size,
            fields=fields)

        if len(issues) == 0:
            # Retrieve issues until there are no more to come
            break

        block_num += 1
        all_issues = all_issues + issues
    return all_issues

def getSprintName(issue):
    try:
        sname = ""
        for sprint in issue.fields.customfield_10004:
            sprint_name = str(re.findall(r"name=[^,]*", str(issue.fields.customfield_10004[0])))
            sname = sprint_name.lstrip("['name=").rstrip("']")
        return sname
    except:
        return ""

jira = JIRA("https://jira.upaid.pl",basic_auth=("upaid","Y9U378v4azofRscPVfB"),options=options)
nameMap = {field['name']:field['id'] for field in jira.fields()}

wb = Workbook()
sheet = wb.active

issues = searchIssues(
    "status = Done AND 'Story Points' is not EMPTY AND project != 'Zakupy Fenige' AND project != Urlopy AND resolved > startOfMonth(-6) ORDER BY resolved DESC",
    "Story Points,project,resolutiondate,customfield_10004"
)

for issue in issues:
    toWrite = []

    toWrite.append(str(issue.key))
    toWrite.append(str(issue.fields.project))
    toWrite.append(str(getattr(issue.fields,nameMap["Story Points"])).replace(".",","))

    toWrite.append(getSprintName(issue))

    date = dateutil.parser.parse(issue.fields.resolutiondate)
    date = date.strftime("%b %Y")
    toWrite.append(date)

    sheet.append(toWrite)

wb.save("xd.xlsx")
