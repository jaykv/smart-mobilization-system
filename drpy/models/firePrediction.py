from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
import tensorflow as tf

imageWidth, imageHeight = 200,200
train_data_dir 			= 'C:\\Users\\mural\\Downloads\\disaster-response-pipeline-master\\data\\train'
validation_data_dir 	= 'C:\\Users\\mural\\Downloads\\disaster-response-pipeline-master\\data\\validation'
finalTesting_data_dir	= 'C:\\Users\\mural\\Downloads\\disaster-response-pipeline-master\\data\\FinalTesting'
trainSamples 			= 1914
validationSamples 		= 182
epochs 					= 50
batchSize 				= 32

if K.image_data_format() == 'channels_first':
    input_shape 		= (3, imageWidth, imageHeight)
else:
    input_shape 		= (imageWidth, imageHeight, 3)

model 					= Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('sigmoid'))               
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

train_datagen 			= ImageDataGenerator(rescale=1. / 255,shear_range=0.2,zoom_range=0.2,horizontal_flip=True)

# augmentation : only rescaling
test_datagen 			= ImageDataGenerator(rescale=1. / 255)

train_generator 		= train_datagen.flow_from_directory(train_data_dir,target_size=(imageWidth, imageHeight),batch_size=batchSize,class_mode='binary')

validation_generator 	= test_datagen.flow_from_directory(validation_data_dir,target_size=(imageWidth, imageHeight),batch_size=batchSize,class_mode='binary')

# checkpoint 				= ModelCheckpoint("first1_cp.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=5)

history 				= model.fit_generator(train_generator,steps_per_epoch=trainSamples // batchSize,epochs=epochs,validation_data=validation_generator,validation_steps=validationSamples // batchSize)

# predict_generator(generator, steps=None, callbacks=None, max_queue_size=10, workers=1, use_multiprocessing=False, verbose=0)

model.save('first_try.h5')

loaded_model 			= tf.keras.models.load_model('first_try.h5')
print ("loaded the model")
print (finalTesting_data_dir)
generator 				= test_datagen.flow_from_directory(validation_data_dir,target_size=(imageWidth, imageHeight),batch_size=batchSize,class_mode=None,shuffle=False)
prediction 				= loaded_model.predict_generator(generator)

prediction 				= [(1 if x < 0.5  else 0 ) for x in prediction]
print (prediction)
