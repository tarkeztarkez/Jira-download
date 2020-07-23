from jira import JIRA

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
        ("status = Done AND 'Story Points' is not EMPTY AND project != 'Zakupy Fenige' AND project != Urlopy ",
         start_idx,
         block_size,
         fields="Story Points,project,resolutiondate")
    if len(issues) == 0:
        # Retrieve issues until there are no more to come
        break
    block_num += 1
    for issue in issues:
        toWrite = []

        toWrite.append(str(issue.key))
        toWrite.append(str(issue.fields.project))
        toWrite.append(str(getattr(issue.fields,nameMap["Story Points"])).replace(".",","))




        print(";".join(toWrite))
        file.write(";".join(toWrite)+"\n")

file.close()
