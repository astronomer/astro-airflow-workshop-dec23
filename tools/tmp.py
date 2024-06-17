import os

import requests
from astro.api import AstroAPI

TEAM_NAME = "Workshop Attendees"
TEAM_DESCRIPTION = "Team for Astro workshop attendees"
ORG_ID = "clxj4mnmy00vr01o1f1kvaagv"


token = os.environ.get("TOKEN")
client = AstroAPI(astro_api_token=token)


users = client.users_list(org_id=ORG_ID)
user_ids = [user.id for user in users]
print(user_ids)

try:
    team = client.team_create(
        org_id=ORG_ID,
        team_name=TEAM_NAME,
        description=TEAM_DESCRIPTION,
        member_ids=user_ids,
    )

    team_id = team.id
except requests.exceptions.HTTPError as e:
    resp = e.response
    resp_json = resp.json()
    print(resp_json)
    if "already exists" in resp_json.get("message", ""):
        existing_teams = client.team_list(
            org_id=ORG_ID,
        )
        matching_teams = [team for team in existing_teams if team.name == TEAM_NAME]
        if len(matching_teams) == 1:
            matching_team = matching_teams[0]
            print(f"Existing team found (id={matching_team.id})")
            team_id = matching_team.id


client.team_add_members(
    org_id=ORG_ID,
    team_id=team_id,
    member_ids=user_ids,
)
