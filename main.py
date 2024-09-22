import boto3
import json

CLUSTER = "foo"
SUBNETS = ["bar", "baz"]
SECURITY_GROUPS = ["foobarbaz"]


def run_ecs_task(cluster: str, task: str, container: str, subnets: list[str], security_groups: list[str], item: str, env: list[dict[str, str]]):
    print(f"starting task {task} cluster {cluster} item: {item}")
    client = boto3.client("ecs", region_name="region")
    response = client.run_task(
        cluster=cluster,
        launchType="FARGATE",
        taskDefinition=task,
        count=1,
        platformVersion="LATEST",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": subnets,
                "securityGroups": security_groups,
                "assignPublicIp": "DISABLED",
            }
        },
        overrides={
            "containerOverrides": [
                {
                    "name": container,
                    "environment": env,
                },
            ]
        },
    )
    print(f"ecs run task response: {response} item: {item}")


def run_some_ecs_task(item: str, foo: str, bar: str, baz: str, foobarbaz: str = None) -> None:
    task = "foo"
    container = "bar"
    foobarbaz = json.dumps({"foobarbaz": foobarbaz})
    env = [
        {"name": "foo", "value": foo},
        {"name": "bar", "value": bar},
        {"name": "baz", "value": baz},
        {"name": "foobarbaz", "value": foobarbaz},
    ]
    run_ecs_task(CLUSTER, task, container, SUBNETS, SECURITY_GROUPS, item, env)


if __name__ == "__main__":
    run_some_ecs_task("item", "foo", "bar", "baz", "foobarbaz")
