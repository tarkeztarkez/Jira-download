from jira import JIRA
import requests
import re
option = {
    "server":"https://jira.upaid.pl"

}

jira = JIRA(options=option,auth=("upaid", "Y9U378v4azofRscPVfB"),)
print(jira.issue("FENIGE-3065"))