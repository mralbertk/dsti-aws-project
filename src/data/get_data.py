from zipfile import ZipFile

import glob2
import wget


def get_data(src, dst):
    """
    Downloads a file from a remote source to the local file system.

    :param src: Source URI
    :param dst: Destination directory
    """
    remote_url = src
    local_dir = dst
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
