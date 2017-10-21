from jinja2 import Template
import click
import yaml
import os


@click.group()
@click.option('--verbose', is_flag=True)
def cli(verbose):
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

    if env != "":
        vars = vars[env]

    output = input.name.replace('tmpl', 'yaml')

    # Render template
    template = Template(input.read().decode("utf-8"))
    template.stream(vars).dump(output)
    os.system("kubectl create -f " + output + " -n " + env)


if __name__ == '__main__':
    cli()
