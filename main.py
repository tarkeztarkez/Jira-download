from jira import JIRA

jira = JIRA(server="https://jira.upaid.pl",basic_auth=("upaid","Y9U378v4azofRscPVfB"),)
print(jira.issue("FENIGE-3065"))