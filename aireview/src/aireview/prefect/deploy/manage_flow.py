import asyncio
import importlib
import sys
import argparse
from prefect import Flow
from prefect.types.entrypoint import EntrypointType
from prefect import exceptions, get_client  # noqa
from prefect.client.orchestration import PrefectClient  # noqa
from prefect.client.schemas.filters import (
    DeploymentFilter,
    DeploymentFilterTags,
    FlowRunFilter,
)  # noqa


def env_to_workpool(env: str):
    """
    Return the workpool name based on the environment
    """
    low_cased_env = env.lower()
    if low_cased_env == "prd":
        return "workpool-k8s-prd"
    elif low_cased_env == "dev":
        return "workpool-k8s-dev"
    else:
        return "workpool-k8s-rap"


async def deploy(
    flow: Flow,
    product: str,
    env: str,
    parameters: dict = {},
    additional_job_variables: dict = {},
    concurrency_limit: int = 3,
    cron: str | None = None,
    work_queue_name: str = "default",
    image_tag: str = "test-local",
    name_override: str | None = None,
):
    """
    This is the function that will deploy the flows to the Prefect server
    Add your flow deployment here.

    flow: The flow function
    product: The product name (pdx, dpf, kamai)
    env: The environment (prd, dev, prxxxxx)
    parameters: The parameters for the flow
    additional_job_variables: Additional job variables to be passed to the flow
    concurrency_limit: The concurrency limit for the flow
    cron: The cron schedule for the flow
    work_queue_name: The work queue name for the flow
    image_tag: The image tag for the flow
    name_override: The name override for the flow
    """
    result = await flow.with_options(name=f"{flow.name}-{env}").deploy(
        name=f"{product}-{env}" if name_override is None else name_override,
        image=f"crdataprd.azurecr.io/prefect-flow-{product}:{image_tag}".lower(),
        work_pool_name=env_to_workpool(env),
        work_queue_name=work_queue_name,
        cron=cron,
        tags=[env.lower(), product.lower()],
        job_variables={
            "env": {
                f"{product.upper()}_ENV": env,
            },
            **additional_job_variables,
        },
        parameters=parameters,
        concurrency_limit=concurrency_limit,
        entrypoint_type=EntrypointType.MODULE_PATH,
        build=False,
    )
    print(f"Deployment ID: {result}")
    return result


async def remove_all_resource_for_pr(env: str):
    """
    Remove all resources for a PR:
    1. snowflake credentials block
    2. deployments and its runs
    """
    client = get_client()
    # remove the snowflake credentials block

    print("💥 Deleting the deployments and its runs")
    deployment_filter = DeploymentFilter(tags=DeploymentFilterTags(all_=[env.lower()]))

    print(
        "Fetching deployments with filter: {}".format(
            deployment_filter.__dict__["tags"].__dict__["all_"]
        )
    )
    deployments = await client.read_deployments(deployment_filter=deployment_filter)

    for d in deployments:
        flow = await client.read_flow(d.flow_id)
        print(f"💥 Deleting flow {flow.name}")
        # remove all the flow runs

        flow_runs = await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(flow_id=flow.id)
        )
        for fr in flow_runs:
            print(f"💥 Deleting flow run {fr.id} {fr.name}")
            await client.delete_flow_run(fr.id)

        print(f"💥 Deleting deployment {d.id}")
        await client.delete_deployment(d.id)


def deploy_flow(product: str, env: str, flow: str, image_tag: str):
    """
    Deploy a Prefect flow with the specified parameters.

    Args:
        product (str): The product name
        env (str): Environment (e.g., dev, staging, prod)
        flow (str): Name of the flow to deploy
        image_tag (str): Docker image tag to use
    """
    print(
        f"Deploying flow '{flow}' for product '{product}' in environment '{env}' with image tag '{image_tag}'"
    )
    # Add deployment logic here
    module, flow_name = flow.split(":")
    flow = getattr(importlib.import_module(module), flow_name)
    asyncio.run(deploy(flow, product, env, image_tag=image_tag))


def clean_environment(env: str):
    """
    Clean up flows in the specified environment.

    Args:
        env (str): Environment to clean (e.g., dev, staging, prod)
    """
    print(f"Cleaning up flows in environment '{env}'")
    asyncio.run(remove_all_resource_for_pr(env.lower()))


def main():
    parser = argparse.ArgumentParser(description="Manage Prefect flows")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a flow")
    deploy_parser.add_argument("product", help="Product name")
    deploy_parser.add_argument("env", help="Environment (dev/staging/prod)")
    deploy_parser.add_argument("--flow", action="append", help="Flow name")
    deploy_parser.add_argument("--image-tag", type=str, help="Docker image tag")

    # Clean command
    clean_parser = subparsers.add_parser(
        "clean", help="Clean up flows in an environment"
    )
    clean_parser.add_argument("env", help="Environment to clean")

    args = parser.parse_args()

    if args.command == "deploy":
        if args.flow is None:
            print("🚨 No flow specified")
            sys.exit(1)
        for f in args.flow:
            deploy_flow(args.product, args.env, f, args.image_tag)
    elif args.command == "clean":
        clean_environment(args.env)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
