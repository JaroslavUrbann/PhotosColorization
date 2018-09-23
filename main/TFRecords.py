import tensorflow as tf
from matplotlib.image import imread
import glob
from skimage import io, color
from tensorflow.python import keras as keras
import os
from PIL import Image

train_tfrecords_path = "../datasets/celebA_train.tfrecords"
test_tfrecords_path = "../datasets/celebA_test.tfrecords"

def split_images(images_path, train_size=0.9):
    image_paths = glob.glob(images_path + "/*.*")
    a = int(len(image_paths)*train_size)
    train_x = image_paths[:a]
    test_x = image_paths[a:len(image_paths)]
    return train_x, test_x


def png2jpeg():



def write(image_paths, output_path):
    with tf.python_io.TFRecordWriter(output_path) as writer:
        for path in image_paths:
            with tf.gfile.FastGFile(path, 'rb') as fid:
                img_bytes = fid.read()

            # TODO: png -> jpeg, resize img, convert to lab
            if os.path.splitext(path)[1].lower() == ".png":
                im = Image.open(path)
            data = {
                    "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_bytes])),
                }
            feature = tf.train.Features(feature=data)
            example = tf.train.Example(features=feature)
            serialized = example.SerializeToString()
            writer.write(serialized)


def read(serialized):
    features = {
        "image": tf.FixedLenFeature([], tf.string)
    }
    parsed_example = tf.parse_single_example(serialized=serialized, features=features)
    return tf.cast(tf.decode_raw(parsed_example['image'], tf.uint8), tf.float32)


def input_fn(path, train=False, batch_size=16, buffer_size=1024):
    dataset = tf.data.TFRecordDataset(filenames=path)
    dataset = dataset.map(read)

    if train:
        dataset = dataset.shuffle(buffer_size)
        repeat = None
    else:
        repeat = 1

    dataset = dataset.repeat(repeat)
    dataset = dataset.batch(batch_size)
    iterator = dataset.make_one_shot_iterator()
    images = iterator.get_next()
    x = {"image": images}
    return x


train_x_paths, test_x_paths = split_images("../datasets/celebA")
print("writing")
write(train_x_paths, test_tfrecords_path)
