import click
import girder_client
import json


@click.command(
    name="populate-metadata",
    short_help="Populate collection metadata",
    help="Populate the specified collection(s) with the provided metadata",
)
@click.option(
    "--id",
    "ids",
    multiple=True,
    required=True,
    help="Used to specify a collection ID to extract metadata to.",
)
@click.option(
    "-d",
    "--data",
    help="The file containing metadata to populate the desired collection(s).",
)
@click.option(
    "-m",
    "--meta",
    help="The raw metadata to populate the desired collection(s).",
)
@click.option(
    "-u", "--username", help="The user's username on the Girder instance"
)
@click.option(
    "-p", "--password", help="The user's password on the Girder instance"
)
@click.option(
    "--api-key", help="The api key for the Girder instance being used."
)
@click.option(
    "--api-url",
    required=True,
    help="The api url of the Girder instance being used.",
)
def main(ids, data, meta, username, password, api_key, api_url):
    if data:
        json_meta = json.load(open(data, "r"))
    elif meta:
        json_meta = json.loads(meta)
    else:
        raise click.ClickException("Either --data or --meta required.")

    gc = girder_client.GirderClient(apiUrl=api_url)
    if username and password:
        gc.authenticate(username=username, password=password)
    elif api_key:
        gc.authenticate(apiKey=api_key)

    failed = []
    for colId in ids:
        try:
            gc.sendRestRequest(
                method="PUT",
                path="collection/" + colId + "/metadata",
                json=json_meta,
            )
        except girder_client.HttpError:
            failed.append(colId)

    click.echo("Operation failed on the following collection ids:")
    click.echo(", ".join(failed))
    click.echo("")
    click.echo(
        "Successfully set metadata on "
        + str(len(ids) - len(failed))
        + "/"
        + str(len(ids))
        + " collections"
    )


if __name__ == "__main__":
    main()
