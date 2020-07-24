options = {
    "cookies":{
        "JSESSIONID": "F54263E662CD279F253567CF57F782B6"
    }
}


from jira import JIRA
import re
import dateutil.parser
from openpyxl import Workbook
import pandas as pd

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

        print("GET: "+str(issues))
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

def getTeamName(issue):
    if str(issue.fields.project) == "OTPSRB":
        return "Merchant"
    elif str(issue.fields.project) == "FENIGE":
        return "Administracja"
    else:
        teamName = re.sub("^\d+\s|\s\d+\s|\s\d+$", "", getSprintName(issue))
        teamName = teamName.lstrip(" Sprint")
        if teamName == "":
            teamName = "No team"
        return teamName

jira = JIRA("https://jira.upaid.pl",basic_auth=("upaid","Y9U378v4azofRscPVfB"),options=options)
nameMap = {field['name']:field['id'] for field in jira.fields()}

print("Getting issues...")
issues = searchIssues(
    "status = Done AND 'Story Points' is not EMPTY AND project != 'Zakupy Fenige' AND project != Urlopy AND resolved > startOfMonth(-6) ORDER BY resolved DESC",
    "Story Points,project,resolutiondate,customfield_10004"
)
print("Getting issues... DONE")

data = {
    "Key": [],
    "Project": [],
    "Story Points": [],
    "Team Name": [],
    "Resolve Date": []
}

for issue in issues:
    teamName = getTeamName(issue)
    if teamName == "":
        continue
    data.get("Team Name").append(getTeamName(issue))

    data.get("Key").append(str(issue.key))
    data.get("Project").append(str(issue.fields.project.name+ " ("+str(issue.fields.project)+")"))
    data.get("Story Points").append(float(getattr(issue.fields,nameMap["Story Points"])))

    date = dateutil.parser.parse(issue.fields.resolutiondate)
    date = date.strftime("%m.%Y")
    data.get("Resolve Date").append(date)

    print("SAVE: "+issue.key)

#TODO: Dynamic report name
print("Creating DataFrame...")
data = pd.DataFrame(data,columns=["Key","Project","Story Points","Team Name","Resolve Date"])

print("Creating PivotTable...")
table = pd.pivot_table(data,values="Story Points",index=["Project","Team Name"],columns="Resolve Date",aggfunc="sum")
table2 = pd.pivot_table(data,values="Story Points",index=["Team Name","Project"],columns="Resolve Date",aggfunc="sum")

print("Writing to Excel...")
writer = pd.ExcelWriter("xd.xlsx",engine='xlsxwriter')
table.to_excel(writer,sheet_name="Sheet1")
table2.to_excel(writer,sheet_name="Sheet2")
writer.save()
print("ALL DONE!!!")