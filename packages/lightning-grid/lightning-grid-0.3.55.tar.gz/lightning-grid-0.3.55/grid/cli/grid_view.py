import click

from grid.client import Grid
import grid.globals as env
from grid.types import ObservableType


@click.group()
def view():
    pass


@view.command()
@click.argument('experiment_id', type=str, required=True, nargs=1)
@click.argument('page', type=str, nargs=1, required=False)
def experiment(experiment_id: [str], page: str) -> None:
    """Grid view shows we web UI page for your runs and experiments."""
    # Fetch URL from globals.
    url = env.GRID_URL.replace('/graphql', '#')

    # Instantiate Grid client.
    client = Grid()

    # Figure out which object is requested
    # so we can construct path.
    base_path = 'view'
    qualifier_path = 'experiment'

    # Combine all strings into a single URL.
    if page:
        launch_url = '/'.join(
            [url, base_path, qualifier_path, experiment_id, page])
    else:
        launch_url = '/'.join([url, base_path, qualifier_path, experiment_id])

    # If the page requested is Tensorboard
    # get the URLs for those services from the backend and
    # open those specific pages in the browser.
    #
    # We'll use Tensorboard filtering to construct the right URL.
    error_message = ''
    tensorboard_url = None
    if page == 'tensorboard':

        resp = client.experiment_details(experiment_id)
        run_name = resp['getExperimentDetails']['run']['name']

        # Always get the status for a given Run because
        # that's where we store the resource URLs.
        observable = client.status(kind=ObservableType.RUN,
                                   identifiers=[run_name])

        # Finds the run result.
        run_data = None
        for run in observable['getRuns']:
            if run['name'] == run_name:
                run_data = run
                break

        # Construct the URLs for both services.
        if run_data:
            resource_urls = run_data.get('resourceUrls')
            if resource_urls:
                tensorboard_url = run_data['resourceUrls'].get('tensorboard')
                if tensorboard_url:
                    tensorboard_url = f"{tensorboard_url}#scalars&regexInput={experiment_id}"

            if not tensorboard_url:
                error_message = "Tensorboard isn't ready yet."

            launch_url = tensorboard_url

    # If we could not find the requested URL, raise an error.
    if not launch_url:
        raise click.ClickException(
            f'Could not view page {page} for {experiment_id}. {error_message}')

    # Open browser.
    click.echo()
    click.echo(f'Opening URL: {launch_url}')
    click.echo()

    click.launch(launch_url)


@view.command()
@click.argument('run_name', type=str, nargs=1)
@click.argument('page', type=str, nargs=1, required=False)
def run(run_name: str, page: str) -> None:
    """Grid view shows we web UI page for your runs and experiments."""
    # Fetch URL from globals.
    url = env.GRID_URL.replace('/graphql', '#')

    # Instantiate Grid client.
    client = Grid()

    # Figure out which object is requested
    # so we can construct path.
    base_path = 'view'
    qualifier_path = 'run'

    # Combine all strings into a single URL.
    if page:
        launch_url = '/'.join([url, base_path, qualifier_path, run_name, page])
    else:
        launch_url = '/'.join([url, base_path, qualifier_path, run_name])

    # If the page requested is Tensorboard
    # get the URLs for those services from the backend and
    # open those specific pages in the browser.
    #
    # We'll use Tensorboard filtering to construct the right URL.
    error_message = ''
    tensorboard_url = None
    if page == 'tensorboard':
        # Always get the status for a given Run because
        # that's where we store the resource URLs.
        observable = client.status(kind=ObservableType.RUN,
                                   identifiers=[run_name])

        # Finds the run result.
        run_data = None
        for run in observable['getRuns']:
            if run['name'] == run_name:
                run_data = run
                break

        # Construct the URLs for both services.
        if run_data:
            resource_urls = run_data.get('resourceUrls')
            if resource_urls:
                tensorboard_url = run_data['resourceUrls'].get('tensorboard')
                if tensorboard_url:
                    tensorboard_url = f"{tensorboard_url}#scalars&regexInput={run_name}"

            if not tensorboard_url:
                error_message = "Tensorboard isn't ready yet."

            launch_url = tensorboard_url

    # If we could not find the requested URL, raise an error.
    if not launch_url:
        raise click.ClickException(
            f'Could not view page {page} for {run_name}. {error_message}')

    # Open browser.
    click.echo()
    click.echo(f'Opening URL: {launch_url}')
    click.echo()

    click.launch(launch_url)
