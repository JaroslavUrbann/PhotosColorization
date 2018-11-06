import os
from generator_fn import generator_fn
from evaluate_model import validate_images
from train_model import model_definition, train_model, load_trained_model
from keras.models import load_model
current_directory = os.path.dirname(os.path.abspath(__file__))

batch_size = 1
batches_per_epoch = 1
n_epochs = 1
batches_per_validation = 1
images_size = (255, 255)

training_path = os.path.join(current_directory, "dataset_training.zip")
validation_path = os.path.join(current_directory, "test_dataset.zip")
trained_model_path = os.path.join(current_directory, "pspnet.h5")
trained_model = load_trained_model(trained_model_path)

# training_data_fn = generator_fn(batch_size, training_path, images_size, trained_model)
validation_data_fn = generator_fn(batch_size, validation_path, images_size, trained_model)
# model = model_definition()
model = load_model("model_final.hdf5")

# train_model(model,
#             training_data_fn,
#             validation_data_fn,
#             n_epochs,
#             batches_per_epoch,
#             batches_per_validation,
#             current_directory)

validate_prediction = True
n_batches = 1
validate_images(validate_prediction, model, validation_data_fn, n_batches, current_directory)
