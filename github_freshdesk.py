import os
import requests
import argparse


def get_github_user_info(username):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Error retrieving GitHub user information: {response.text}"
            )

        return response.json()

    except Exception as e:
        raise Exception(f"Error : {e}")


def create_or_update_freshdesk_contact(subdomain, contact_data):
    url = f"https://{subdomain}.freshdesk.com/api/v2/contacts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('FRESHDESK_TOKEN')}",
    }
    try:
        response = requests.get(url, headers=headers)
        contacts = response.json()

        existing_contact = next(
            (
                contact
                for contact in contacts
                if contact["email"] == contact_data["email"]
            ),
            None,
        )

        if existing_contact:
            url = f"{url}/{existing_contact['id']}"
            response = requests.put(url, json=contact_data, headers=headers)
            if response.status_code == 200:
                print("Contact updated successfully!")

        else:
            response = requests.post(url, json=contact_data, headers=headers)
            if response.status_code == 201:
                print("Contact created successfully!")
            else:
                raise Exception(f"Error creating contact in Freshdesk: {response.text}")

    except Exception as e:
        raise Exception(f"Error : {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve GitHub user information and create/update Freshdesk contact."
    )
    parser.add_argument("github_username", help="GitHub username")
    parser.add_argument("freshdesk_subdomain", help="Freshdesk subdomain")

    args = parser.parse_args()

    github_user_info = get_github_user_info(args.github_username)
    if github_user_info:
        contact_data = {
            "name": github_user_info.get("name", ""),
            "email": github_user_info.get("email", ""),
            "phone": github_user_info.get("phone", ""),
            "description": github_user_info.get("bio", ""),
        }
        create_or_update_freshdesk_contact(args.freshdesk_subdomain, contact_data)


if __name__ == "__main__":
    main()
