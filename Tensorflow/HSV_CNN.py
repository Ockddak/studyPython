#!/usr/bin/env python
# coding: utf-8

import tensorflow as tf
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from scipy.linalg import eigh
import numpy as np
from time import time
from datetime import datetime

print(tf.__version__)
print(tf.keras.__version__)


import os
 
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
root_path = 'x, y공통 경로'
load_xyz_path = 'x 상세 경로'
ref_df = pd.read_excel(root_path + 'y 상세 경로', header = None)

a = datetime.now()
print("시작시간 : %3s" %(a))

save_xyz_path = root_path + 'Point9/'
p = 25

createFolder(save_xyz_path)

sugars  = []
sugarsGrade = []

roi_nps = []
zip_dfs = pd.DataFrame()
xyzFileCnt = len(os.listdir(root_path+load_xyz_path))
sucCnt     = 1
for f in os.listdir(root_path+load_xyz_path):    
    if '.xyz' in f :
        roi_df = pd.read_csv(root_path + load_xyz_path + f, sep = '\t', header = None, error_bad_lines=False, skiprows=1)
        roi_df = pd.concat([roi_df.loc[:,:173], roi_df.loc[:, 176: ]], axis=1)
        x_avg = (roi_df[0].max() + roi_df[0].min() + 1) // 2
        y_avg = (roi_df[1].max() + roi_df[1].min() + 1) // 2

        zip_df = pd.DataFrame()
        for i in range(-25, 26, 1) :
            for j in range(-25, 26, 1) :
                point  = roi_df[(roi_df[0] == x_avg + i) & (roi_df[1] == y_avg + j)].loc[:,2:]
                zip_df = zip_df.append(point)

        sugar           = float(ref_df[(ref_df[0]== f)].loc[:,1:1].values)

        # 학습용
        sugarsGrade.append(int(n // 0.5))
        roi_nps.append(roi_df.loc[:,2:].to_numpy().reshape(140,140,202))
        sugars.append(sugar)
        zip_df['sugar'] = sugar
        zip_dfs = zip_dfs.append(zip_df)
        
        print("%3d / %3d Success!" %(xyzFileCnt, sucCnt))
        sucCnt += 1

saveFileName = datetime.today().strftime('%Y%m%d%H%M') + '_' + str(xyzFileCnt) + '.csv'
zip_dfs.to_csv(save_xyz_path+ saveFileName , encoding = 'euc-kr', index=False)

b = datetime.now()
print("종료시간 : %3s" %(b))
print("종료 - 시작 : %3s" %(b-a))

batch_size = 10
max_epochs = 100
learning_rate = 0.001

sugarsGrade = []

for n in sugars :
    sugarsGrade.append(int(n // 0.5))
print(set(sugarsGrade))
print(len(set(sugarsGrade)))
print("=======================================")

train_labes = np.array(sugarsGrade).astype(np.float32)
print(train_labels.shape)

print("=======================================")
from collections import Counter
print(Counter(sugarsGrade))


train_data, test_data, train_labels, test_labels = train_test_split(np.array(roi_nps).astype(np.float32), 
                                                    np.array(sugarsGrade).astype(np.float32),
                                                    stratify=np.array(sugarsGrade).astype(np.float32), 
                                                    test_size=0.10)
print(f"X_train: {train_data.shape}\ny_train: {train_labels.shape}\nX_test: {test_data.shape}\ny_test: {test_labels.shape}") 




checkpoint_path = "./train_model/exp_cnn/cp-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

tensorboard = tf.keras.callbacks.TensorBoard(log_dir='./train_model/GA_logs/{}'.format(time()))



class Conv(tf.keras.Model):
    def __init__(self, filters, kernel_size):
        super(Conv, self).__init__()
        
        self.conv = tf.keras.layers.Conv2D(filters = filters
                                           , kernel_size = kernel_size
                                           )
        self.bn = tf.keras.layers.BatchNormalization() 
        self.relu = tf.keras.layers.ReLU()
        self.pool = tf.keras.layers.MaxPool2D()
        self.drop = tf.keras.layers.Dropout(0.4)

    def call(self, inputs, training=False):

        x = self.conv(inputs)
        x = self.bn(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.drop(x)
        
        return x


model = tf.keras.Sequential()



model.add(tf.keras.layers.Input(shape=[140,140,202]))
model.add(Conv(64, 3))
model.add(Conv(128, 3))
model.add(Conv(256, 3))
model.add(Conv(256, 3))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(units=512))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.ReLU())
model.add(tf.keras.layers.Dropout(0.4))
model.add(tf.keras.layers.Dense(units=256))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.ReLU())
model.add(tf.keras.layers.Dropout(0.4))
model.add(tf.keras.layers.Dense(units=26, activation='softmax'))



model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate), 
              loss = 'sparse_categorical_crossentropy',
              metrics = 'accuracy')

model.summary()



print(datetime.now())
print("=================================================")

hist = model.fit(train_data,
                 train_labels,
              epochs = 20, 
              batch_size = 10,
              verbose   = 1,
              validation_data = (test_data, test_labels),
              callbacks = [cp_callback, tensorboard])

print("=================================================")
print(datetime.now())



get_ipython().run_line_magic('load_ext', 'tensorboard')

get_ipython().run_line_magic('tensorboard', '--logdir ./train_model/GA_logs/')



loss, acc = model.evaluate(test_data, test_labels)


print(f"Accuracy: {acc*100}\nLoss: {loss}")


target_names = []

for n in range(26):
    target_names.append(n)

pred = model.predict(test_data)

suc_cnt  = 0
fail_cnt = 0
for i, (py, y_pred) in enumerate(zip(test_labels, pred)) :
    if py == np.argmax(y_pred) :
        suc_cnt  += 1
    else :
        fail_cnt += 1

print(np.argmax(pred))
print("==========================")     
print("suc_cnt : %3d, fail_cnt : %3d" %(suc_cnt, fail_cnt))
print("==========================")
print(Counter(sugarsGrade)) 

pred = model.predict(train_data[:10])
print(pred)
print("===================================")
print(pd.DataFrame(pred).round(2).loc[:,13:])

print(train_labes[:10])

print("===================================")
print(Counter(sugarsGrade))

