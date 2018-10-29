import os
from generator_fn import generator_fn
from evaluate_model import validate_images
from train_model import model_definition, train_model, load_trained_model

current_directory = os.path.dirname(os.path.abspath(__file__))

n_images = 1
batch_size = 1
n_epochs = 1
batches_per_epoch = int(n_images / batch_size)
validation_batches = 1

images_path = os.path.join(current_directory, "test_dataset.zip")
trained_model_path = os.path.join(current_directory, "pspnet.h5")
trained_model = load_trained_model(trained_model_path)

# training_data_fn = generator_fn(n_images, batch_size, images_path, trained_model)
validation_data_fn = generator_fn(n_images, batch_size, images_path, trained_model)
model = model_definition()
# train_model(model,
#             training_data_fn,
#             validation_data_fn,
#             n_epochs,
#             batches_per_epoch,
#             validation_batches,
#             current_directory)

validate_prediction = False
n_batches = 1
validate_images(validate_prediction, model, validation_data_fn, n_batches, current_directory)
