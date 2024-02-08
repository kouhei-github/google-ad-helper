

def get(
        resource_type,
        resource_name
):
    return '{}-{}'.format(
        resource_name,
        resource_type
    )
