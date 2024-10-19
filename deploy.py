from botocore.exceptions import ClientError
import boto3
import click
import os
import time


def get_script_directory() -> str:
    script_path = __file__
    full_path = os.path.realpath(script_path)
    script_dir = os.path.dirname(full_path)
    return script_dir


def get_template_path() -> str:
    script_directory = get_script_directory()
    # parent_directory = os.path.dirname(script_directory)
    template_path = os.path.join(script_directory, "vpn_server.yaml")
    return template_path


def get_console_url(region_name, stack_id):
    return f"https://console.aws.amazon.com/cloudformation/home?region={region_name}#/stacks/stackinfo?stackId={stack_id}"


def print_stack_outputs(cf, stack_name):
    try:
        response = cf.describe_stacks(StackName=stack_name)
        stack = response["Stacks"][0]
        outputs = stack.get("Outputs", [])
        for output in outputs:
            if output["OutputKey"] == "ConnectionInstructions":
                print("\nConnection Instructions:")
                print(output["OutputValue"])
                break
    except ClientError as e:
        print(f"Failed to retrieve stack outputs for '{stack_name}'. Error: {e}")


def track_stack_progress(cf, region_name, stack_name):
    stack_url = get_console_url(region_name, stack_name)
    print(f"Tracking stack progress, URL to CloudFormation console: {stack_url}")
    while True:
        try:
            response = cf.describe_stacks(StackName=stack_name)
            stack = response["Stacks"][0]
            status = stack["StackStatus"]
            print(f"Current stack status: {status}")
            if status.endswith(("COMPLETE", "FAILED")):
                break
        except ClientError as e:
            print(f"Error tracking stack progress: {e}")
            break
        time.sleep(10)
    print(f"Done, CloudFormation URL is: {stack_url}")
    # If stack creation/update is complete, retrieve and print the ConnectionInstructions
    if status.endswith("COMPLETE"):
        print_stack_outputs(cf, stack_name)


def deploy_cloudformation_stack(
    stack_name: str, key_pair_name: str, instance_type: str, region: str
):
    # Create a CloudFormation client
    boto3.setup_default_session(region_name=region)
    cf = boto3.client("cloudformation")
    region_name = cf.meta.region_name  # Get the region name from the client

    # Define the CloudFormation template
    template_path = get_template_path()
    with open(template_path, "r") as file:
        template_body = file.read()

    # Create the CloudFormation stack
    try:
        cf.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=[
                {"ParameterKey": "KeyPairName", "ParameterValue": key_pair_name},
                {"ParameterKey": "InstanceType", "ParameterValue": instance_type}
            ],
            Capabilities=["CAPABILITY_IAM"],
        )
        print(f"Stack '{stack_name}' creation initiated.")
        track_stack_progress(cf, region_name, stack_name)
    except ClientError as e:
        print(f"Failed to create stack '{stack_name}'. Error: {e}")
        return


@click.command()
@click.option(
    "--stack-name",
    required=True,
    help="Name for CloudFormation stack",
    default="vpn-server",
)
@click.option(
    "--key-pair-name",
    required=True,
    help="Name for ssh key pair",
    default="vpn",
)
@click.option(
    "--region",
    required=True,
    help="The region in which the bucket should be deployed",
    default="us-west-2",
)
@click.option(
    "--instance-type",
    required=True,
    help="Instance type for the EC2 instance, see https://aws.amazon.com/ec2/instance-types/",
    default="t3a.small",
)
def main(stack_name: str, key_pair_name: str, instance_type: str, region: str):
    deploy_cloudformation_stack(stack_name, key_pair_name, instance_type, region)


if __name__ == "__main__":
    main()
