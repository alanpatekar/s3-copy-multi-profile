# S3 Copy Objects using multiple boto3 sessions

AWS default s3 copy API call does not work with two AWS principals (except for head object operation).
The use case for this tool is when you have divided permissions on different AWS principals and want to
use one principal for the get_object operation and another principal for the put_object operation in an automated fashion.

Simple AWS S3 utility used to copy S3 objects from one bucket to another using two AWS profiles.
It also keeps all the metadata associated with the objects - tags.

The tool will grab the source objects and metadata, save them in memory, switch boto3 sessions and upload the 
objects and metadata into the destination bucket.

## NOTE

This is a work in progress and should not be used with prod data.
It currently works with s3 objects with only one level of "directory" prefix.
This utility does not scale well. Tested with ~100 objects.

## Usage example

You can use poetry to install the environment for s3-copy-multi-profile tool.

**Note**: cd into s3-copy-multi-profile directory

Command to run utility:

```
python s3-copy-multi-profile.py --src_profile "my-src-profile" --src_bucket "my-src-bucket" --src_prefix "multiple" --dest_profile "my-dest-profile" --dest_bucket "my-dest-bucket" --dest_prefix "multiple"
```

## Arguments explained
```commandline
    :param src_s3_client: s3_client with permissions to get_object on source objects
    :param src_bucket: source bucket
    :param src_prefix: source s3 prefix
    :param dest_s3_client: destination s3 client with put_object permissions
    :param dest_bucket: destionation s3 bucket
    :param dest_prefix: destination s3 prefix
```

## Future focus

    - the base for loop does not scale well
    - run the utility in an automated fasion, inside CodeBuild/Pipeline/Lambda
