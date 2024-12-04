import argparse
import asyncio
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from prefect import get_client, exceptions
from prefect.blocks.system import Secret
from prefect_snowflake import SnowflakeCredentials

cli = SecretClient(
    "https://kvdataprd.vault.azure.net/", credential=DefaultAzureCredential()
)


async def clean_block(block_type: str, block_name: str) -> None:
    """
    Remove a block by its type and name
    e.g. snowflake-credentials:block-snowflake-cred-dpf-dev
    """
    cli = get_client()
    try:
        id_block = await cli.read_block_document_by_name(block_name, block_type)
        await cli.delete_block_document(id_block.id)
    except exceptions.ObjectNotFound:
        print(f"Already deleted {block_name} block")


def deploy_secret(secret_name: str, block_name: str):
    """Deploy a Key Vault secret to a Prefect Secret block"""
    sn = secret_name.lower()
    bn = block_name.lower()

    secret = cli.get_secret(sn)
    Secret(value=secret.value).save(bn, overwrite=True)
    print(f"💥 Deployed secret {sn} to block {bn}")


def deploy_snowflake_secret(
    secret_name: str,
    block_name: str,
    user: str,
    role: str,
    account: str = "TM88069-WAKAM",
):
    """Deploy Snowflake credentials as a block"""
    print(f"Creating snowflake credentials {block_name}")

    private_key = cli.get_secret(secret_name).value

    cred = SnowflakeCredentials(
        user=user,
        account=account,
        role=role,
        private_key=bytes(private_key, "utf-8"),
    )

    cred.save(block_name, overwrite=True)
    print(f"💥 Deployed Snowflake credentials to block {block_name}")


def main():
    parser = argparse.ArgumentParser(description="Manage Prefect blocks")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a block")
    deploy_subparsers = deploy_parser.add_subparsers(
        dest="block_type", help="Type of block to deploy"
    )

    # Secret deploy
    secret_parser = deploy_subparsers.add_parser("secret", help="Deploy a secret block")
    secret_parser.add_argument("--secret-name", required=True, help="Key vault secret name")
    secret_parser.add_argument("--block-name", required=True, help="Block name")

    # Snowflake deploy
    snowflake_parser = deploy_subparsers.add_parser(
        "snowflake-credentials", help="Deploy Snowflake credentials"
    )
    snowflake_parser.add_argument(
        "--secret-name", required=True, help="Key vault secret name"
    )
    snowflake_parser.add_argument("--block-name", required=True, help="Block name")
    snowflake_parser.add_argument("--user", required=True, help="Snowflake user")
    snowflake_parser.add_argument("--role", required=True, help="Snowflake role")
    snowflake_parser.add_argument(
        "--account", default="TM88069-WAKAM", help="Snowflake account"
    )

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean a block")
    clean_parser.add_argument(
        "block_type",
        choices=["secret", "snowflake-credentials"],
        help="Type of block to clean",
    )
    clean_parser.add_argument("block_name", help="Name of block to clean")

    args = parser.parse_args()

    if args.action == "deploy":
        if args.block_type == "secret":
            deploy_secret(args.secret_name, args.block_name)
        elif args.block_type == "snowflake-credentials":
            deploy_snowflake_secret(
                args.secret_name, args.block_name, args.user, args.role, args.account
            )
    elif args.action == "clean":
        asyncio.run(clean_block(args.block_type, args.block_name))


if __name__ == "__main__":
    main()
