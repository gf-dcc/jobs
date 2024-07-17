import requests
import pandas as pd
import json

def get_team_name(team_id):
    url = f"https://repo-prod.prod.sagebase.org/repo/v1/team/{team_id}"
    response = requests.get(url)
    if response.status_code == 200:
        team = response.json()
        team_name = team.get("name", "")
        return team_name
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_team_members(team_id):
    team_name = get_team_name(team_id)
    if not team_name:
        return None

    url = f"https://repo-prod.prod.sagebase.org/repo/v1/teamMembers/{team_id}&limit=50"
    response = requests.get(url)
    if response.status_code == 200:
        team_members = response.json()["results"]
        members_data = []
        for member in team_members:
            first_name = member["member"].get("firstName", "")
            last_name = member["member"].get("lastName", "")
            if not first_name and last_name:
                first_name = last_name
            elif not last_name and first_name:
                last_name = first_name

            user_name = member["member"].get("userName", "")
            owner_id = member["member"].get("ownerId", "")

            members_data.append({
                "teamId": team_id,
                "teamName": team_name,
                "firstName": first_name,
                "lastName": last_name,
                "userName": user_name,
                "ownerId": owner_id,
                "isAdmin": member["isAdmin"]
            })

        return members_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def print_table_header():
    print("{:<10} {:<20} {:<15} {:<15} {:<15} {:<15} {:<15}".format("Team ID", "Team Name", "First Name", "Last Name", "User Name", "Owner ID", "Permission Level"))
    print("-" * 110)

print_table_header()

team_ids = [3423657, 3427329, 3442703, 3444502, 3444501, 3444504, 3466987, 3466748, 3443961, 3444503]

all_teams_data = []
for team_id in team_ids:
    team_members_data = get_team_members(team_id)
    if team_members_data:
        all_teams_data.extend(team_members_data)

# Convert all data to DataFrame
df = pd.DataFrame(all_teams_data)

# Print DataFrame
print(df)

# Export to CSV
df.to_csv("team_members.csv", index=False)
