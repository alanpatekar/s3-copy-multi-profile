import click
import logging
import boto3


def get_from_s3_source(s3_client, bucket_name):
    # grabs s3 objects and metadata from source and saves it to local temp dir
    res = s3_client.get_object(Bucket='string', Key='')

    print(res)


@click.command()
#@click.option('--envname', help="Override envname from account")
@click.help_option()
def run(** cmdargs):
    """
    Delete all objects in path
    """
    logger = logging.getLogger()

    # cmdargs = dsc.handle_common_cli_args(cmdargs, has_aws=True, logger=logger)
    # session = cmdargs.get('session')
    #
    # res = delete_s3_objects(session)
    source_profile = 'aws-it-sec-sbx-03.Developer'
    session = boto3.session.Session(profile_name=source_profile)


if __name__ == '__main__':

    run()