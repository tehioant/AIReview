# to use in local environment
# for pipeline deploy, pipeline create block
# azure + prefect

import os

import requests
import toml
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from requests.exceptions import RequestException

CLIENT_ID = os.getenv("CLIENT_ID", "af7f4c73-bf79-4e97-b078-01ddd481836a")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", None)
AZURE_TOKEN_URL = os.getenv(
    "AZURE_TOKEN_URL",
    "https://login.microsoftonline.com/36074882-37f3-4ca9-b7c0-bc58077cece0/oauth2/v2.0/token",
)
SCOPE = os.getenv("SCOPE", "api://af7f4c73-bf79-4e97-b078-01ddd481836a/.default")
WAKAM_PREFECT_API_URL = os.getenv(
    "WAKAM_PREFECT_API_URL", "https://prefect.wakam.com/api"
)
PREFECT_PROFILE_FILE = os.path.join(os.path.expanduser("~"), ".prefect/profiles.toml")

if CLIENT_SECRET is None:
    print("CLIENT_SECRET is not set, reading from Azure Key Vault")
    # read from azure key vault
    client = SecretClient(
        vault_url=os.getenv("AZURE_KEY_VAULT_URL", "https://kvdataprd.vault.azure.net"),
        credential=DefaultAzureCredential(),
    )
    CLIENT_SECRET = client.get_secret("prefect-server-app-prd").value
    print("CLIENT_SECRET read from Azure Key Vault Successfully")


def create_auth_data():
    return {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
    }


def fetch_azure_token():
    data = create_auth_data()
    try:
        response = requests.post(AZURE_TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except RequestException as e:
        raise Exception(f"Error retrieving token: {e}") from e


def local_login():
    # Read the toml file
    token = fetch_azure_token()
    import pathlib

    profile_file_path = pathlib.Path(PREFECT_PROFILE_FILE)
    if not profile_file_path.exists():
        profile_file_path.parent.mkdir(parents=True, exist_ok=True)
        profile_file_path.touch()

    with open(profile_file_path) as file:
        data = toml.load(file)

    if "profiles" not in data:
        data["profiles"] = {}

    # Add a section called wkm.k8s
    data["profiles"]["wkm.k8s"] = {
        "PREFECT_API_KEY": token,
        "PREFECT_API_URL": WAKAM_PREFECT_API_URL,
    }

    data["active"] = "wkm.k8s"

    # Write the data back to the file
    with open(PREFECT_PROFILE_FILE, "w") as file:
        toml.dump(data, file)

    # Set the prefect environment variable
    os.environ["PREFECT_API_KEY"] = token
    print("Prefect environment variable set successfully")

    os.environ["PREFECT_API_URL"] = WAKAM_PREFECT_API_URL
    print("Prefect API URL environment variable set successfully")


if __name__ == "__main__":
    local_login()
