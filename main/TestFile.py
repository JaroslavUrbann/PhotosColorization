import numpy as np
from keras import layers
from keras import backend as K
from keras.models import model_from_json, load_model
from keras.backend import tf as ktf
import h5py


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

# np.save("pspnet.npy", pspnet.get_weights())
# weights = np.load('pspnet_8.npy')
with open("DesktopApp/models/pspnet.json") as pspnet_architecture:
    json_string = pspnet_architecture.read()
pspnet_8 = model_from_json(json_string, custom_objects={'Interp': Interp})
pspnet_8.load_weights("DesktopApp/models/pspnet.h5")
pspnet_8._make_predict_function()
# h = h5py.File('test.hdf5', 'w')
# h.create_dataset('weights_data', data=weights)
# pspnet.load_weights("test.hdf5")
# pspnet.summary()
pspnet = load_model("pspnet.h5", custom_objects={'Interp': Interp})
# print(pspnet.layers[len(pspnet.layers) - 10:])
# print(len(pspnet.layers))
# get_intermediate_output = K.function([pspnet.layers[0].input], [pspnet.layers[len(pspnet.layers) - 9].output])
# layer_output = get_intermediate_output([np.zeros((1, 473, 473, 3))])
# print(layer_output)
pspnet._make_predict_function()
# pspnet.fit(np.zeros((1, 473, 473, 3)), np.zeros((1, 473, 473, 150)))
# print(np.max(pspnet.predict(np.zeros((1, 473, 473, 3)))))

# print(pspnet_8.layers[len(pspnet.layers) - 17])
# print(len(pspnet_8.layers[len(pspnet.layers) - 17].get_weights()))
# 17
# i = 1
# pspnet.layers[len(pspnet.layers) - i].set_weights(pspnet_8.layers[len(pspnet.layers) - i].get_weights())
# print(np.max(pspnet.predict(np.zeros((1, 473, 473, 3)))))
for i in range(len(pspnet.layers)):
    if i == len(pspnet.layers) - 17:
        p_8 = pspnet_8.layers[len(pspnet.layers) - 17].get_weights()[:3]
        p_8.append(pspnet.layers[len(pspnet.layers) - 17].get_weights()[3])
        pspnet.layers[i].set_weights(p_8)
        continue
    pspnet.layers[i].set_weights(pspnet_8.layers[i].get_weights())
# print(pspnet.layers[len(pspnet.layers) - 8].get_weights())
pspnet.save_weights("pspnet_1.h5")
