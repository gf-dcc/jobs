import requests
import synapseclient
import pandas as pd
syn=synapseclient.login()

def get_team_members(team_id):
    url = f"https://repo-prod.prod.sagebase.org/repo/v1/team/{team_id}"
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        team = response.json()
        team_name = team["name"]
    # API endpoint URL
    url = f"https://repo-prod.prod.sagebase.org/repo/v1/teamMembers/{team_id}"
    # Send GET request to the API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        team_members = response.json()["results"]
        # Create a list of dictionaries with the desired columns
        members_data = [
            {
                "teamId": team_id,
                "firstName": member["member"]["firstName"],
                "lastName": member["member"]["lastName"],
                "isAdmin": member["isAdmin"]
            }
            for member in team_members
        ]
        # Print each team member’s data as a row
        for member in members_data:
            membership_level = "Member"
            if member["isAdmin"]:
                membership_level = "Manager"
            print("{:<10} {:<15} {:<15} {:<10}".format(
                team_name,
                member["firstName"],
                member["lastName"],
                membership_level
            ))
    else:
        print(f"Error: {response.status_code} - {response.text}")
def print_table_header():
    # Print the table header
    print("{:<10} {:<15} {:<15} {:<10}".format("Team ID", "First Name", "Last Name", "Permission Level"))
    print("-" * 75)
print_table_header()

# Get the team members DataFrame
get_team_members(3423657)
get_team_members(3427329)
get_team_members(3442703)
get_team_members(3444502)
get_team_members(3444501)
get_team_members(3444504)
get_team_members(3466987)
get_team_members(3466748)
get_team_members(3443961)
get_team_members(3444503)
