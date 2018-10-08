from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
from main.Tools import crop_img

model = ResNet50(weights='imagenet')

img_path = 'elephant.jpg'
img2 = image.load_img(img_path, target_size=(224, 224))
img2 = image.img_to_array(img2)
img2 = np.expand_dims(img2, axis=0)
img2 = preprocess_input(img2)

x = Image.open(img_path)
x = crop_img(x, 224, 224)[0]
x = image.img_to_array(x)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(img2)
print('Predicted:', decode_predictions(preds, top=10))
