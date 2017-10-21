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
    deploy_to_kb(output, env)


def deploy_to_kb(output, env):
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

    print(service)
    print(deployment)

    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    create_deployment(extensions_v1beta1, deployment, env)

    core = kubernetes.client.CoreV1Api()
    create_service(core, service, env)


def create_deployment(api_instance, deployment, env):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=env,
    )
    print("Deployment created. status='%s'" % str(api_response.status))


def create_service(api_instance, service, env):
    api_response = api_instance.create_namespaced_service(
        body=service,
        namespace=env,
    )
    print("Service creatd. Status='%s'" % str(api_response.status))


if __name__ == '__main__':
    cli()
