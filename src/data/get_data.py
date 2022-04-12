import wget, glob2
from zipfile import ZipFile


def get_data(src, dst):
    """
    Downloads a file from a remote source src to a local destination dst.
    """
    remote_url = src
    local_dir = dst
    wget.download(remote_url, local_dir)


def unzip_data(dir):
    """Unpacks the first zip file in a directory"""
    local_dir = dir
    file = glob2.glob(f'{local_dir}/*.zip')[0]
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dir)
