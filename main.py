import src.data.get_data as loader
import src.data.upload_data as uploader
import src.features.clean_data as cleaner
import src.models.cnn as classifier
import os
import glob2
import tensorflow as tf
from tensorflow import keras
from datetime import datetime
from dotenv import load_dotenv

# ----------------- Set up some variables -----------------
load_dotenv()
src = os.getenv("DATA_SOURCE")
dst = os.getenv("DATA_FOLDER")
bucket = os.getenv("S3_BUCKET")
obj_prefix = os.getenv("S3_OBJ_PREFIX")

# ---------------- Create data directories ---------------
os.makedirs("data/external", exist_ok=True)
os.makedirs("data/interim", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)

# --------------------- Data loading ----------------------
# Only download data if not available in local destination
if src.split("/")[-1] not in os.listdir(dst):
    loader.get_data(src, dst)
    loader.unzip_data(dst)

# --------------------- Data cleaning ---------------------
cleaner.clean_data(dst)

# ----------------- Training preparation ------------------
# image_size = tuple(os.getenv("IMAGE_SIZE"))
image_size = (180, 180)
batch_size = int(os.getenv("BATCH_SIZE"))

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    f"{dst}/PetImages",
    validation_split=0.2,
    subset="training",
    seed=int(os.getenv("RDN_SEED")),
    # important to specify the seed to make sure training and validation data are exclusive (no corruption)
    # because they are coming from the same directory
    image_size=image_size,
    batch_size=batch_size,
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    f"{dst}/PetImages",
    validation_split=0.2,
    subset="validation",
    seed=int(os.getenv("RDN_SEED")),
    image_size=image_size,
    batch_size=batch_size,
)

# -------------------- Model Creation ---------------------

model = classifier.make_model(
    input_shape=image_size + (3,), num_classes=2
)

epochs = 1

callbacks = [
    keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
]

model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

model.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=val_ds,
)

# ------------------- Save Model to S3 --------------------

# Use current datetime for distinct file name
current_date = datetime.now().strftime("%m%d%Y-%H%M%S")

# Local storage is temporary
result = model.save(f'./data/interim/model_{current_date}.h5')

# File path and object name are needed for S3 upload
upload_file = glob2.glob("./data/interim/*.h5")[0]
obj_suffix = upload_file.split("\\")[-1]
s3_object = f'{obj_prefix}{obj_suffix}' if obj_prefix else obj_suffix

# Upload to S3
uploader.upload_file(upload_file, bucket, s3_object)

# Remove the model from local storage
os.remove(upload_file)
