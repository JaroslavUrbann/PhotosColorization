# # from keras.preprocessing import image
# # from keras.applications.resnet50 import decode_predictions
# from PIL import Image, ImageOps
# # import numpy as np
# # import keras
# # import time
#
# # model = keras.applications.xception.Xception(include_top=False) # 16 x 16 x 2048 5.90s
# # model = keras.applications.inception_v3.InceptionV3(include_top=False) # 14 x 14 x 2048 4.07s
# # model = keras.applications.nasnet.NASNetMobile(include_top=False, input_shape=(512, 512, 3)) # 16 x 16 x 1056 (non flexible) 8.83s
# # model = keras.applications.vgg16.VGG16(include_top=False) 16 x 16 x 512 7.38s
# # model = keras.applications.densenet.DenseNet121(include_top=False) # 16 x 16 x 1024 7.66s
# # model = keras.applications.inception_v3.InceptionV3(include_top=False) # 14 x 14 x 2048 4.35s
# # model = keras.applications.mobilenet_v2.MobileNetV2(include_top=False) # 16 x 16 x 1280 2.42s
# #
# # img_path = 'testimg2.jpg'
# # img2 = image.load_img(img_path, target_size=(512, 512))
# # img2 = image.img_to_array(img2)
# # img2 = np.expand_dims(img2, axis=0)
#
# image = Image.open('x.jpg')
# image.thumbnail((256, 256))
# new_im = Image.new('RGB', (256, 256))
# new_im.paste(image, (int((256 - image.size[0])/2), int((256 - image.size[1])/2)))
# new_im.save("output.jpg")
#
#
# # start_time = time.time()
# # preds = model.predict(img2)
# # print(time.time() - start_time)
# # print(preds.shape)
# # print(np.min(preds))
# # print(np.max(preds))
# # print('Predicted:', decode_predictions(preds, top=10))

m = "one" if False else "two" if False else "three" if True else "four"
print(m)