import click
import logging
import boto3
import os


def s3_copy(src_s3_client, src_bucket, src_prefix, dest_s3_client, dest_bucket, dest_prefix=None, logger=None):
    """
     Grabs src object and metadata, saves them locally and copies the objects and metadata into destination bucket.
    :param src_s3_client: s3_client with permissions to get_object on source objects
    :param src_bucket: source bucket
    :param src_prefix: source s3 prefix
    :param dest_s3_client: destination s3 client with put_object permissions
    :param dest_bucket: destionation s3 bucket
    :param dest_prefix: destination s3 prefix
    :return:
    """
    logger.info("S3-copy-multi-profile START")
    objects = src_s3_client.list_objects_v2(Bucket=src_bucket, Prefix=src_prefix)['Contents']

    for obj in objects:
        # get key, get tags, download locally,  switch session, upload object, put tag, remove local object

        # remove prefix from src object
        removed_prefix = obj['Key'].split("/")[-1]
        # download object locally
        res_download = src_s3_client.download_file(src_bucket, obj['Key'], removed_prefix)

        # upload object in destination
        dest_key = f"{dest_prefix}/{removed_prefix}"
        local_file = open(removed_prefix, 'rb')
        res_put_obj = dest_s3_client.put_object(Body=local_file,Bucket=dest_bucket, Key=dest_key)

        # get object tags from src object
        tag_res = src_s3_client.get_object_tagging(Bucket=src_bucket, Key=obj.get('Key'))

        # put src object tags on dest object
        put_tags_response = dest_s3_client.put_object_tagging(
            Bucket=dest_bucket,
            Key=dest_key,
            Tagging={'TagSet': tag_res.get('TagSet')})

        logger.debug(f'Successfully copied {removed_prefix} into {dest_bucket}.')

        # cleanup downloaded local file
        os.remove(removed_prefix)

    logger.info("S3-copy-multi-profile DONE.")


def handle_arguments(kwargs, logger=None):
    """
    Handle s3-copy-multi-profile arguments, establish boto3 sessions and s3 clients.
    :param kwargs:
    :param logger:
    :return: dict {"src_s3_client":src_s3_client,
           "src_bucket": src_bucket,
           "src_prefix": src_prefix,
           "dest_s3_client": dest_s3_client,
           "dest_bucket": dest_bucket,
           "dest_prefix": dest_prefix,
           "logger": logger,
           }
    """
    src_profile = kwargs.get('src_profile')
    src_session = boto3.session.Session(profile_name=src_profile)
    src_bucket = kwargs.get('src_bucket')
    src_prefix = kwargs.get('src_prefix')
    src_s3_client = src_session.client('s3')

    dest_profile = kwargs.get('dest_profile')
    dest_session = boto3.session.Session(profile_name=dest_profile)
    dest_bucket = kwargs.get('dest_bucket')
    dest_prefix = kwargs.get('dest_prefix')
    dest_s3_client = dest_session.client('s3')

    res = {"src_s3_client":src_s3_client,
           "src_bucket": src_bucket,
           "src_prefix": src_prefix,
           "dest_s3_client": dest_s3_client,
           "dest_bucket": dest_bucket,
           "dest_prefix": dest_prefix,
           "logger": logger,
           }

    return res


@click.command()
@click.option('--src_profile', help="Override envname from account")
@click.option('--src_bucket', help="Override envname from account")
@click.option('--src_prefix', help="Override envname from account")
@click.option('--dest_profile', help="Override envname from account")
@click.option('--dest_bucket', help="Override envname from account")
@click.option('--dest_prefix', help="Override envname from account")
@click.help_option()
def _run(** cmdargs):
    """
    Run s3-copy-multi-profile utilty.
    """
    logger = logging.getLogger()

    cmdargs = handle_arguments(cmdargs, logger=logger)
    s3_copy(**cmdargs)


if __name__ == '__main__':

    _run()