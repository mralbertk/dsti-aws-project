import os
import tensorflow as tf


def clean_data(folder):
    """Some comment here"""

    num_skipped = 0

    for folder_name in ("Cat", "Dog"):
        folder_path = f'{folder}/PetImages/{folder_name}'

        for file_name in os.listdir(folder_path):
            file_path = f'{folder_path}/{file_name}'

            try:
                file_obj = open(file_path, "rb")
                is_jfif = tf.compat.as_bytes("JFIF") in file_obj.peek(10)
            finally:
                file_obj.close()

            if not is_jfif:
                num_skipped += 1
                # Delete corrupted image
                os.remove(file_path)

    print("Deleted %d images" % num_skipped)