from jira import JIRA
import re
import dateutil.parser
import datetime

options = {
    "cookies":{
        "JSESSIONID": "32297DEEB683F6D90F44C19B57D2C84B"
    }
}

jira = JIRA("https://jira.upaid.pl",basic_auth=("upaid","Y9U378v4azofRscPVfB"),options=options)
nameMap = {field['name']:field['id'] for field in jira.fields()}

file = open("xd.csv","w")

block_size = 100
block_num = 0
while True:
    start_idx = block_num*block_size
    issues = jira.search_issues\
        ("status = Done AND 'Story Points' is not EMPTY AND project != 'Zakupy Fenige' AND project != Urlopy AND resolved > startOfMonth(-6)",
         start_idx,
         block_size,
         fields="Story Points,project,resolutiondate,customfield_10004")
    if len(issues) == 0:
        # Retrieve issues until there are no more to come
        break
    block_num += 1
    for issue in issues:
        toWrite = []

        toWrite.append(str(issue.key))
        toWrite.append(str(issue.fields.project))
        toWrite.append(str(getattr(issue.fields,nameMap["Story Points"])).replace(".",","))

        sname = ""
        try:
            for sprint in issue.fields.customfield_10004:
                sprint_name = str(re.findall(r"name=[^,]*", str(issue.fields.customfield_10004[0])))
                sname = sprint_name.lstrip("['name=").rstrip("']")
        except:pass
        toWrite.append(sname)

        date = dateutil.parser.parse(issue.fields.resolutiondate)
        date = date.strftime("%b %Y")
        toWrite.append(date)

        print(";".join(toWrite))
        file.write(";".join(toWrite)+"\n")

file.close()
