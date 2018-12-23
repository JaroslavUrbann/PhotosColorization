from keras.models import load_model
import matplotlib.pyplot as plt
import tensorflow as tf
import matplotlib
import numpy as np

model = load_model("FinalModel.hdf5")


def plot_filters(layer, x, y):
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        filters = sess.run(layer.kernel)
    fig = plt.figure()
    for i in range(filters.shape[3]):
        ax = fig.add_subplot(y, x, i+1)
        ax.imshow(filters[:, :, 0, i], cmap=matplotlib.cm.binary)
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    plt.tight_layout()
    return plt


plot_filters(model.layers[1], 4, 8).show()
