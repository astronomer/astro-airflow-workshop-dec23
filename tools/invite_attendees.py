#!/usr/bin/env python3
import argparse

import requests

_ORGANIZATION_MEMBER="ORGANIZATION_MEMBER"


_INVITE_ENDPOINT = "https://api.astronomer.io/iam/v1beta1/organizations/%s/invites"

def main():
    # Parse arguments for email txt file and organization id
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--emails-file",
        help="Path to txt file containing emails to invite, one per line",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--organizationId",
        help="Astro organization id",
        required=True,
        type=str,
    )

    parser.add_argument(
        "--api-token",
        help="Astro API token",
        required=True,
        type=str,
    )
    args = parser.parse_args()
    
    # Read csv file
    with open(args.emails_file) as f:
        emails = f.readlines()
    
    # Send invite to each email
    for email in emails:
        email = email.strip()
        invite = {
            "inviteeEmail": email,
            "role": _ORGANIZATION_MEMBER
        }

        response = requests.post(
            _INVITE_ENDPOINT % args.organizationId,
            json=invite,
            headers={
                "Authorization": "Bearer %s" % args.api_token,
            }
        )
        if response.status_code == 200:
            print("Successfully invited %s" % email)

        else:
            print("Failed to invite %s" % email)
            print(response.text)

if __name__ == "__main__":
    main()