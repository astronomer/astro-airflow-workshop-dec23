from pathlib import Path
from dataclasses import dataclass
import requests
from typing import Literal, Optional
import inspect

_ORGANIZATION_MEMBER = "ORGANIZATION_MEMBER"


@dataclass
class AstroTeam:
    id: str
    name: str
    organizationId: str
    organizationRole: Literal[
        "ORGANIZATION_OWNER", "ORGANIZATION_BILLING_ADMIN", "ORGANIZATION_MEMBER"
    ]
    description: Optional[str] = None
    deploymentRoles: Optional[list[dict]] = None
    workspaceRoles: Optional[list[dict]] = None

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )


@dataclass
class AstroUser:
    fullName: str
    id: str
    status: Literal["ACTIVE", "INACTIVE", "PENDING", "BANNED"]
    username: str
    organizationRole: Literal[
        "ORGANIZATION_OWNER", "ORGANIZATION_BILLING_ADMIN", "ORGANIZATION_MEMBER"
    ]
    deploymentRoles: Optional[list[dict]] = None
    workspaceRoles: Optional[list[dict]] = None

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )


@dataclass
class AstroOrg:
    id: str
    name: str
    product: Literal["HOSTED", "HYBRID"] = "HOSTED"
    supportPlan: Literal[
        "TRIAL", "BASIC", "STANDARD", "PREMIUM", "BUSINESS_CRITICAL", "INTERNAL"
    ] = "INTERNAL"
    status: Literal["ACTIVE", "INACTIVE", "SUSPENDED"] = "ACTIVE"
    usesCustomMetronomePlan: bool = False
    isEgressChargebackEnabled: bool = False

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class AstroAPI:
    _INVITE_ENDPOINT = "https://api.astronomer.io/iam/v1beta1/organizations/%s/invites"
    _ORG_ENDPOINT = "https://api.astronomer.io/admin/v1alpha1/organizations"
    _USERS_ENDPOINT = "https://api.astronomer.io/iam/v1beta1/organizations/%s/users"
    _TEAM_ENDPOINT = "https://api.astronomer.io/iam/v1beta1/organizations/%s/teams"

    def __init__(
        self,
        astro_api_token: str,
    ):
        if not astro_api_token:
            raise ValueError("Must supply Astro API token")
        s = requests.session()
        s.auth = BearerAuth(token=astro_api_token)
        self._s = s

    def users_list(self, org_id) -> list[AstroUser]:
        resp = self._s.get(self._USERS_ENDPOINT % org_id)
        if resp.status_code == 200:
            resp_json = resp.json()
            users = resp_json.get("users", None)
            if users is None:
                raise ValueError(f"No user data returned\n{resp_json}")
            return [AstroUser.from_dict(u) for u in users]

        else:
            print("Failed to get users for org %s" % org_id)
            raise resp.raise_for_status()

    def team_list(
        self,
        org_id: str,
    ) -> list[AstroTeam]:
        resp = self._s.get(self._TEAM_ENDPOINT % org_id)
        if resp.status_code == 200:
            resp_json = resp.json()
            teams = resp_json.get("teams", None)
            if teams is None:
                raise ValueError(f"No team data returned\n{resp_json}")
            return [AstroTeam.from_dict(t) for t in teams]

        else:
            print("Failed to get teams for org %s" % org_id)
            raise resp.raise_for_status()

    def team_create(
        self,
        org_id: str,
        team_name: str,
        description: Optional[str] = None,
        member_ids: Optional[list[str]] = None,
        org_role: Optional[str] = "ORGANIZATION_MEMBER",
    ) -> AstroTeam:
        data = {"name": team_name, "organizationRole": org_role}
        if description:
            data["description"] = description
        if member_ids:
            data["memberIds"] = member_ids

        resp = self._s.post(self._TEAM_ENDPOINT % org_id, json=data)
        if resp.status_code == 200:
            print("Successfully create team %s" % team_name)
            resp_json = resp.json()
            return AstroTeam.from_dict(resp_json)

        else:
            print('Failed to create team "%s" for org %s' % (team_name, org_id))
            raise resp.raise_for_status()

    def team_update(
        self,
        org_id: str,
        team_id: str,
        team_name: str,
        description: Optional[str] = None,
        member_ids: Optional[list[str]] = None,
        org_role: Optional[str] = "ORGANIZATION_MEMBER",
    ):
        raise NotImplementedError
        # data = {"name": team_name, "organizationRole": org_role}
        # if description:
        #     data["description"] = description
        # if member_ids:
        #     data["memberIds"] = member_ids

        # resp = self._s.get(self._TEAM_ENDPOINT % org_id)
        # if resp.status_code == 200:
        #     print("Successfully create team %s" % team_name)
        #     return AstroTeam.from_dict(resp.json())

        # else:
        #     print("Failed to get users for org %s" % org_id)
        #     raise resp.raise_for_status()

    def team_upsert(
        self,
        org_id: str,
        team_name: str,
        description: Optional[str] = None,
        member_ids: Optional[list[str]] = None,
        org_role: Optional[str] = "ORGANIZATION_MEMBER",
    ):
        raise NotImplementedError
        # existing_teams = self.team_list(org_id=org_id)
        # matching_teams = [team for team in existing_teams if team.name == team_name]
        # if len(matching_teams) == 0:
        #     self.team_create(
        #         org_id=org_id,
        #         team_name=team_name,
        #         description=description,
        #         member_ids=member_ids,
        #         org_role=org_role,
        #     )

        # if len(matching_teams) == 1:
        #     matching_team = matching_teams[0]
        #     print(f"Existing team found (id={matching_team.id})")

        # if len(matching_teams) == 1:
        #     matching_team = matching_teams[0]
        #     print(f"Existing team found (id={matching_team.id})")

    def team_add_members(
        self,
        org_id: str,
        team_id: str,
        member_ids: list[str],
    ):
        data = {"memberIds": member_ids}
        resp = self._s.post(
            self._TEAM_ENDPOINT % org_id + f"/{team_id}/members",
            json=data,
        )
        if resp.status_code == 204:
            print("Successfully added members to team")

        else:
            print("Failed to add members to team")
            raise resp.raise_for_status()
