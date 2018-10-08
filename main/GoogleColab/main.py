import zipfile
from PIL import Image
from skimage.color import rgb2lab


def lab_img(img):
    img = img.convert("RGB")
    print(img)
    img = rgb2lab(img) / 255
    l = img[:, :, 0]
    ab = []
    a = img[:, :, 1]
    b = img[:, :, 2]
    ab.append(a)
    ab.append(b)
    return l, ab


def crop_img(img, crop_width, crop_height):
    img_width, img_height = img.size
    images = []
    x, y = 0, 0
    # TODO: center cropped image(s)
    while img_height >= y + crop_height:
        while img_width >= x + crop_width:
            images.append(img.crop((x, y, x + crop_width, y + crop_height)))
            x = x + crop_width
        x = 0
        y = y + crop_height
    return images


def flip_img(img):
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return flipped_img


def batch_images(index, batch_size, filepath):
    with zipfile.ZipFile(filepath) as myzip:
        image_paths = myzip.infolist()
        x = []
        y = []
        for image in range(index * batch_size, min(len(image_paths), index * batch_size + batch_size)):
            with myzip.open(image_paths[image]) as img:
                img = Image.open(img)
                cropped_img = crop_img(img, 200, 200)[0]
                flipped_img = flip_img(cropped_img)
                l, ab = lab_img(img)
                flipped_l, flipped_ab = lab_img(flipped_img)
                x.append(l)
                y.append(ab)
                x.append(flipped_l)
                y.append(flipped_ab)
        return x, y


def generator_fn(n_images, batch_size, filepath):
    # B&W x, y done
    # return PSPNet prediction here as the second x that will get fused with the first x in the model
    n_iterations = int(n_images / batch_size)
    for i in range(n_iterations):
        x, y = batch_images(i, batch_size, filepath)
        yield x, y


generator_fn(1000, 32, 'b_probs.zip')

# model.fit_generator(generator_fn(1000, 32, 'b_probs.zip'),
#         samples_per_epoch=10000, nb_epoch=10)
