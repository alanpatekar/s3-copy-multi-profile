import click
import logging


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
    print('hey')


if __name__ == '__main__':

    run()