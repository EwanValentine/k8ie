from jinja2 import Template
import click
import yaml

from kubernetes import client, config


@click.group()
@click.option('--verbose', is_flag=True)
def cli(verbose):
    config.load_kube_config()
    if verbose:
        click.echo('Running in verbose mode')


@cli.command()
@click.argument('input', type=click.File('rb'))
@click.option('--env', help='Environment')
def deploy(input, env):
    with open("service.yaml", 'r') as stream:
        try:
            vars = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    vars = dict(list(vars.items()) + list(vars[env].items()))

    output = input.name.replace('tmpl', 'yaml')

    # Render template
    template = Template(input.read().decode("utf-8"))
    template.stream(vars).dump(output)
    commit_changes(output, env)


def commit_changes(output, env):
    print(output)
    with open(output, 'r') as stream:
        try:
            docs = yaml.load_all(stream)
            for doc in docs:
                if doc['kind'] == "Service":
                    service = doc
                elif doc['kind'] == "Deployment":
                    deployment = doc

        except yaml.YAMLError as exc:
            print(exc)
            return

    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    exists = does_deployment_exist(extensions_v1beta1, deployment['metadata']['name'], env)

    if exists is True:
        update_deployment(extensions_v1beta1, deployment, env)
    else:
        create_deployment(extensions_v1beta1, deployment, env)

    core = client.CoreV1Api()
    exists = does_service_exist(core, service['metadata']['name'], env)

    if exists is not True:
        create_service(core, service, env)
        return

    update_service(core, service, env)


def does_deployment_exist(api_instance, name, env):
    click.echo('Checking if deployment already exists or not.')
    try:
        api_response = api_instance.read_namespaced_deployment(
            name=name,
            namespace=env,
        )
    except client.rest.ApiException as http_exception:
        return False

    click.echo("Deployment already exists")
    return True


def create_deployment(api_instance, deployment, env):
    click.echo('Creating deployment.')
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=env,
    )
    print("Deployment created. status='%s'" % str(api_response.status))


def update_deployment(api_instance, deployment, env):
    click.echo("Updating existing deployment")
    api_response = api_instance.replace_namespaced_deployment(
        name=deployment['metadata']['name'],
        namespace=env,
        body=deployment,
    )
    print("Deployment updated. Status='%s'" % str(api_response.status))


def create_service(api_instance, service, env):
    api_response = api_instance.create_namespaced_service(
        body=service,
        namespace=env,
    )
    print("Service creatd. Status='%s'" % str(api_response.status))


def update_service(api_instance, service, env):
    api_response = api_instance.patch_namespaced_service(
        name=service['metadata']['name'],
        namespace=env,
        body=service,
    )
    print("Service updated. Status='%s'" % str(api_response.status))


def does_service_exist(api_instance, service_name, env):
    try:
        api_response = api_instance.read_namespaced_service(
            name=service_name,
            namespace=env,
        )
    except client.rest.ApiException as http_exception:
        return False
    return True

if __name__ == '__main__':
    cli()
