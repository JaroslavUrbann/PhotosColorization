from keras.models import load_model, Model
from keras import backend as K
import matplotlib.pyplot as plt
from skimage.color import rgb2lab
from PIL import Image
import matplotlib
import numpy as np
from PSPNet import predict_segmentation
model = load_model("FinalModel.hdf5")


def plot_filters(layer, x, y):
    filters = layer.get_weights()[0]
    fig = plt.figure()
    for i in range(min(filters.shape[3], x*y)):
        ax = fig.add_subplot(y, x, i+1)
        ax.set_title(12)
        im = ax.imshow(np.fliplr(filters[:, :, 0, i+28]), cmap=matplotlib.cm.binary, vmin=filters.min(), vmax=filters.max())
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    plt.show()


def plot_activation_maps(model, layer, path, x, y):
    img = Image.open(path)
    w, h = img.size
    while w % 8 != 0:
        w += 1
    while h % 8 != 0:
        h += 1
    img = img.resize((w, h))
    l = rgb2lab(img)[:, :, 0]
    l = np.expand_dims(np.array(l) / 100, axis=2)
    l = np.expand_dims(l, axis=0)
    s = predict_segmentation(img)
    get_intermediate_output = K.function([model.layers[0].input, model.layers[16].input], [model.layers[layer].output])
    layer_output = get_intermediate_output([l, s])[0]
    fig = plt.figure()
    for i in range(min(layer_output.shape[3], x * y)):
        ax = fig.add_subplot(y, x, i+1)
        ax.set_title(i)
        im = ax.imshow(layer_output[0, :, :, i+48], cmap=matplotlib.cm.binary, vmin=layer_output.min(), vmax=layer_output.max())
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    plt.show()


# plot_filters(model.layers[1], 1, 1)
plot_activation_maps(model, 12, "w.jpg", 4, 4)
# print(model.layers[16].get_config())
