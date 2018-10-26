from keras.models import model_from_json
from keras.models import Model
from keras.layers import Conv2D, concatenate, Input
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import os
tf.logging.set_verbosity(tf.logging.ERROR)


# Returns trained model instance
def load_trained_model(path):
    json_path = path + ".json"
    h5_path = path + ".h5"
    with open(json_path, 'r') as model_file:
        trained_model = model_from_json(model_file.read())
    trained_model._make_predict_function()
    trained_model.load_weights(h5_path)
    return trained_model


# Returns main model
def model_definition():
    grayscale_input = Input(shape=(None, None, 1))
    grayscale = Conv2D(1, (3, 3), padding="same", activation="relu", use_bias=True)(grayscale_input)

    segmentation_input = Input(shape=(None, None, 150))
    segmentation = Conv2D(1, (3, 3), padding="same", activation="relu", use_bias=True)(segmentation_input)

    merged = concatenate([grayscale, segmentation], axis=3)
    colorized = Conv2D(2, (3, 3), padding="same", activation="relu", use_bias=True)(merged)

    model = Model(inputs=[grayscale_input, segmentation_input], outputs=colorized)
    model.compile(loss="mse", optimizer="adam")
    return model


# Returns list of used keras callbacks
def callbacks(model_path):
    cb = list()
    cb.append(ModelCheckpoint(os.path.join(model_path, "model_checkpoint.hdf5")))
    return cb


# Returns the model after training it
def train_model(model, training_data_fn, validation_data_fn, epochs, steps_per_epoch, validation_steps, save_path):
    model.fit_generator(training_data_fn,
                        epochs=epochs,
                        steps_per_epoch=steps_per_epoch,
                        callbacks=callbacks(save_path),
                        validation_data=validation_data_fn,
                        validation_steps=validation_steps)
    return model
