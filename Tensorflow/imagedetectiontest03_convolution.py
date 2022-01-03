# -*- coding: utf-8 -*-
# Convolution(합성곱) : 특정한 패턴의 특징이 어디서 나타나는지를 확인하는 도구
# 라이브러리 준비
import tensorflow as tf
import pandas as pd

# 데이터 준비
(독립, 종속), _ = tf.keras.datasets.mnist.load_data()
print(독립.shape, 종속.shape)

독립 = 독립.reshape(60000, 28, 28, 1)
종속 = pd.get_dummies(종속)
print(독립.shape, 종속.shape)

# 모델 생성
# Conv2D(Convolution)의 경우에는 3차원(유채색)의 데이터를 Input으로 받음
X = tf.keras.layers.Input(shape=[28, 28, 1])
H = tf.keras.layers.Conv2D(3, kernel_size = 5, activation='swish')(X)    # 3개의 필터셋 = 3채널의 특징맵, (5,5) 사이즈의 필터셋(특징맵)
H = tf.keras.layers.Conv2D(6, kernel_size = 5, activation='swish')(H)    # 6개의 필터셋 = 6채널의 특징맵
H = tf.keras.layers.Flatten()(H)
H = tf.keras.layers.Dense(84, activation='swish')(H)    # 84개의 특징 추출
Y = tf.keras.layers.Dense(10, activation='softmax')(H)  # 10개로 분류

model = tf.keras.models.Model(X, Y)
model.compile(loss='categorical_crossentropy', metrics="accuracy")

# 모델 학습
model.fit(독립, 종속, epochs=10)

# 모델을 이용
pred = model.predict(독립[:5])
pd.DataFrame(pred).round(2)

model.summary()

