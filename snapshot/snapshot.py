import json, os, synapseclient, requests, traceback, sys
from datetime import datetime

# Secrets
secrets = json.loads(os.getenv("SCHEDULED_JOB_SECRETS"))
auth_token = secrets["SYNAPSE_AUTH_TOKEN"]

# Login
syn = synapseclient.Synapse()
syn.login(authToken=auth_token)

# Snapshot is used to version tables, so targets should be ids of tables
# Instead of hard-coding the list of ids here, ids are stored/updated in `syn51729134` and queried during run

# Query for list of entities to version:
targets_set_list = ['syn28142805']
reference = "syn51729134"
ids = syn.tableQuery(f"SELECT id FROM {reference}").asDataFrame()
targets = targets_set_list + ids['id'].tolist()

target_comment = os.getenv("COMMENT")
target_label = datetime.now()
job_schedule = os.getenv("SCHEDULE")
job_label = os.getenv("LABEL")
slack = os.getenv("SLACK") # Slack webhook to send notifications, if given to the job container

print(f"Targets: {targets}")

def slack_report(slack, success:bool, job_schedule, job_label, target, version = ''):
    if success:
        txt = ":white_check_mark: " + job_schedule + " - " + job_label + " succeeded, updated to *" + target + "." + str(
                version) + "* just now."
    else:
        txt = ":x: " + job_schedule + " - " + job_label + " failed just now for *" + target + "* :worried:"
    
    msg = json.dumps({"text": txt})
    r = requests.post(slack, data=msg, headers={'Content-type': 'application/json'})
    print(r.status_code)

# Iterate   
for target in targets:
    try:
        version = syn.create_snapshot_version(table=target, comment=target_comment, label=target_label)
        if slack is not None:
            slack_report(slack, success=True, job_schedule=job_schedule, job_label=job_label, target=target, version=version)
    except:
        traceback.print_exc()
        if slack is not None:
            slack_report(slack, success=False, job_schedule=job_schedule, job_label=job_label, target=target)
