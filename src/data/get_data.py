from zipfile import ZipFile

import glob2
import wget
import boto3


def get_data(src, dst, s3_obj = None):
    """
    Downloads a file from a remote source to the local file system.

    :param src: Source URI (S3 bucket name or a URL)
    :param dst: Destination directory
    :param s3_obj: (Optional) S3 object name
    """
    local_dir = dst

    # If an S3 object is set, load directly from S3
    if s3_obj:
        s3_client = boto3.client('s3')
        target = f'{dst}/{s3_obj.split("/")[-1]}'
        s3_client.download_file(src, s3_obj, target)

    # If no S3 object is set, load from URL
    else:
        remote_url = src
        wget.download(remote_url, local_dir)


def unzip_data(folder):
    """
    Unpacks the first zip file in a directory

    :param folder: Directory to scan for .zip files
    """
    local_dir = folder
    file = glob2.glob(f'{local_dir}/*.zip')[0]
    if not file:
        return False
    with ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(folder)
    return True
