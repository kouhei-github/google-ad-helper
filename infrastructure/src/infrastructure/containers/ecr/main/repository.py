import base64
import pulumi_aws as aws
import pulumi_docker as docker
import pulumi


def create(repository_name: str, dockerfile_context_path: str):
    repository = aws.ecr.Repository(
        "ecr-repository-" + repository_name,
        force_delete=True
    )

    image = docker.Image(
        repository_name + "-image",
        build=docker.DockerBuildArgs(
            context=dockerfile_context_path,
            dockerfile=f"{dockerfile_context_path}/Dockerfile"
        ),
        image_name=repository.repository_url,
        registry=repository.registry_id.apply(get_registry_info),
    )

    pulumi.export("repository", repository.repository_url)

    return repository


def get_registry_info(rid):
    creds = aws.ecr.get_credentials(registry_id=rid)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(':')
    if len(parts) != 2:
        raise Exception("Invalid credentials")

    return docker.RegistryArgs(server=creds.proxy_endpoint, username=parts[0], password=parts[1])
