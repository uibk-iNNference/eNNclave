import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import MobileNet
import tensorflow.keras.layers as layers

from flowers_prepare_data import load_data

IMG_SIZE = 224

BATCH_SIZE = 32

x_train, y_train, x_test, y_test = load_data()

mobilenet = MobileNet(include_top = False, input_shape=(224,224,3))

model = Sequential()

for l in mobilenet.layers:
    if type(l).__name__ == 'BatchNormalization':
        continue
    else:
        l.trainable = False
        model.add(l)

model.add(layers.MaxPooling2D(7))
model.add(layers.GlobalAveragePooling2D())

# add dense layers
model.add(layers.Dropout(0.2))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.2))

model.add(layers.Dense(5, activation='softmax'))

model.compile(optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])
model.summary()
history = model.fit(x_train, y_train,
        epochs = 100,
        )

loss0, accuracy0 = model.evaluate(x_test, y_test)

print("loss: {:.2f}".format(loss0))
print("accuracy: {:.2f}".format(accuracy0))

model.save('models/flowers.h5')