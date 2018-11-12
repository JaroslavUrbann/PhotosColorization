import os
from generator_fn import generator_fn
from evaluate_model import validate_images
from train_model import model_definition, train_model, load_trained_model
from keras.models import load_model

batch_size = 7
images_size = (256, 256)
validate_prediction = True
current_directory = os.path.dirname(os.path.abspath(__file__))

images_path = os.path.join(current_directory, "places_dataset.zip")
images_destination = os.path.join(current_directory, "validation")
trained_model_path = os.path.join(current_directory, "pspnet.h5")
trained_model = load_trained_model(trained_model_path)
validation_data_fn = generator_fn(batch_size, images_path, images_size, trained_model, validation=True)
model = load_model("model_final.hdf5")

validate_images(validate_prediction, model, validation_data_fn, images_destination)
