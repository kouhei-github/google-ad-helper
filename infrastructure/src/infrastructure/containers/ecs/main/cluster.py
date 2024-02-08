import pulumi_aws as aws


def create(cluster_config: dict):
    return aws.ecs.Cluster(
        "ecs-cluster-" + cluster_config['name'],
        name="cluster-" + cluster_config['name'],
        tags={"Name": "Author", "Author": "Pulumi"},
    )
