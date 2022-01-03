# -*- coding: utf-8 -*-

# LeNet : 학습 모델의 종류
# 라이브러리 준비
import tensorflow as tf
import pandas as pd 
import matplotlib.pyplot as plt

"""# MNIST"""

# 데이터 준비
(독립, 종속), _ = tf.keras.datasets.mnist.load_data()
print(독립.shape, 종속.shape)
mnist_x, mnist_y = 독립, 종속

독립 = 독립.reshape(60000, 28, 28, 1)
종속 = pd.get_dummies(종속)
print(독립.shape, 종속.shape)

# 화면 출력
print(mnist_y[:10])
plt.imshow(mnist_x[0])

# 모델 생성(LeNet5)
# Conv2D(Convolution)의 경우에는 3차원(유채색)의 데이터를 Input으로 받음
X = tf.keras.layers.Input(shape=[28, 28, 1])

# same : 필터셋의 크기와 Input 이미지의 크기가 같게 한다.
H = tf.keras.layers.Conv2D(6, kernel_size = 5, padding='same', activation='swish')(X)    # 6개의 필터셋 = 6채널의 특징맵, (5,5) 사이즈의 필터셋(특징맵)
H = tf.keras.layers.MaxPool2D()(H)
H = tf.keras.layers.Conv2D(16, kernel_size = 5, activation='swish')(H)    # 16개의 필터셋 = 16채널의 특징맵
H = tf.keras.layers.MaxPool2D()(H)

H = tf.keras.layers.Flatten()(H)
H = tf.keras.layers.Dense(120, activation='swish')(H)
H = tf.keras.layers.Dense(84, activation='swish')(H)    # 84개의 특징 추출
Y = tf.keras.layers.Dense(10, activation='softmax')(H)  # 10개로 분류

model = tf.keras.models.Model(X, Y)
model.compile(loss='categorical_crossentropy', metrics="accuracy")

print(model.metrics_names)

# 모델 이용

model.fit(독립, 종속, epochs=10)

from google.colab import drive
drive.mount('/content/drive')

import time
t = time.time()

export_path = "/content/save_model/{}".format(int(t))
model.save(export_path, save_format='tf')

export_path

print(mnist_y[:10])
pred = model.predict(mnist_x[:10])
pd.DataFrame(pred).round(2)

"""# Cifar10"""

# 데이터 준비
(독립, 종속), _ = tf.keras.datasets.cifar10.load_data()
print(독립.shape, 종속.shape)

종속 = pd.get_dummies(종속.reshape(50000))
print(독립.shape, 종속.shape)

# 화면 출력
print(종속[:10])
plt.imshow(독립[0])
print(독립[0][0][0])
print(독립[0][0])

# 모델 생성(LeNet5)
# Conv2D(Convolution)의 경우에는 3차원(유채색)의 데이터를 Input으로 받음
X = tf.keras.layers.Input(shape=[32, 32, 3])

# same : 필터셋의 크기와 Input 이미지의 크기가 같게 한다.
H = tf.keras.layers.Conv2D(6, kernel_size = 5, activation='swish')(X)    # 3개의 필터셋 = 3채널의 특징맵, (5,5) 사이즈의 필터셋(특징맵)
H = tf.keras.layers.MaxPool2D()(H)
H = tf.keras.layers.Conv2D(16, kernel_size = 5, activation='swish')(H)    # 6개의 필터셋 = 6채널의 특징맵
H = tf.keras.layers.MaxPool2D()(H)

H = tf.keras.layers.Flatten()(H)
H = tf.keras.layers.Dense(120, activation='swish')(H)
H = tf.keras.layers.Dense(84, activation='swish')(H)    # 84개의 특징 추출
Y = tf.keras.layers.Dense(10, activation='softmax')(H)  # 10개로 분류

model = tf.keras.models.Model(X, Y)
model.compile(loss='categorical_crossentropy', metrics="accuracy")

model.fit(독립, 종속, epochs=10)

print(종속[:10])
pred = model.predict(독립[:10])
pd.DataFrame(pred).round(2)

model.summary()

"""# 학습 모델 저장

"""

import os

checkpoint_path = "/content/save_model/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# 모델의 가중치를 저장하는 콜백 만들기
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

# 새로운 콜백으로 모델 훈련하기
model.fit(독립, 
          종속,  
          epochs=10,
          validation_data=(독립[:10],종속[:10]),
          callbacks=[cp_callback])  # 콜백을 훈련에 전달합니다

loss, acc = model.evaluate(독립[:10],  종속[:10], verbose=2)
print("훈련되지 않은 모델의 정확도: {:5.2f}%".format(100*acc))

# 가중치 로드
model.load_weights(checkpoint_path)

# 모델 재평가
loss, acc = model.evaluate(독립[:10],  종속[:10], verbose=2)
print("복원된 모델의 정확도: {:5.2f}%".format(100*acc))

