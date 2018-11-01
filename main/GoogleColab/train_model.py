from keras.models import Model, load_model
from keras.layers import Conv2D, concatenate, Input
from keras.callbacks import ModelCheckpoint
from keras import layers
from keras.backend import tf as ktf
import tensorflow as tf
import os
tf.logging.set_verbosity(tf.logging.ERROR)


class Interp(layers.Layer):

    def __init__(self, new_size, **kwargs):
        self.new_size = new_size
        super(Interp, self).__init__(**kwargs)

    def build(self, input_shape):
        super(Interp, self).build(input_shape)

    def call(self, inputs, **kwargs):
        new_height, new_width = self.new_size
        resized = ktf.image.resize_images(inputs, [new_height, new_width],
                                          align_corners=True)
        return resized

    def compute_output_shape(self, input_shape):
        return tuple([None, self.new_size[0], self.new_size[1], input_shape[3]])

    def get_config(self):
        config = super(Interp, self).get_config()
        config['new_size'] = self.new_size
        return config


# Returns trained model instance
def load_trained_model(path):
    trained_model = load_model(path, custom_objects={'Interp': Interp})
    trained_model._make_predict_function()
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
