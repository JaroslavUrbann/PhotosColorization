#   If you write anything else than jpeg coded files into TFRecords, it will reach enormous sizes. (38MB -> 1.2GB)
#   Reading from TFRecords will always return tensors and even if it is possible to decode them into numpy arrays
#   or image objects, and then flip them, convert them to Lab, split them and then convert them back to tensors,
#   it just defeats the purpose of using TFRecords. Don't come back.

import tensorflow as tf
import io
from PIL import Image
from main.Tools import split_images, png2jpg, resize_img, crop_img, flip_img

train_tfrecords_path = "../datasets/celebA_train2.tfrecords"
test_tfrecords_path = "../datasets/celebA_test2.tfrecords"


def write(image_paths, output_path, width=960, height=540):
    with tf.python_io.TFRecordWriter(output_path) as writer:
        for path in image_paths:
            img = Image.open(path)
            img = png2jpg(img)
            images = crop_img(img, width, height)
            # TODO: _2lab, "image_target":, flip_image
            for img in images:
                bytes_img = io.BytesIO()
                img.save(bytes_img, format="JPEG")
                data = {
                        "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[bytes_img.getvalue()])),
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
    print(parsed_example)
    raw_img = parsed_example['image']
    print(raw_img)
    decoded_img = tf.decode_raw(raw_img, tf.uint8)
    print(decoded_img)
    float_img = tf.cast(decoded_img, tf.float32)
    print(float_img)
    return float_img


def pipeline(path, train=False, flip=False, batch_size=2, buffer_size=2):
    dataset = tf.data.TFRecordDataset(filenames=path)
    dataset = dataset.map(read)
    print(dataset)
    if train:
        dataset = dataset.shuffle(buffer_size)
        repeat = None
    else:
        repeat = 1

    dataset = dataset.repeat(repeat)
    dataset = dataset.batch(batch_size)
    iterator = dataset.make_one_shot_iterator()
    images = iterator.get_next()
    print(images)
    x = {"image": images}
    # return x


train_x_paths, test_x_paths = split_images("../datasets/celebA")
print("writing")
write(train_x_paths, test_tfrecords_path)
print("reading")
pipeline(test_tfrecords_path)
