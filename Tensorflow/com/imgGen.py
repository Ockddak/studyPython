import pandas as pd
import sys
from os import path, walk

if __name__ == '__main__':
    if __package__ is None:
        print(path.dirname(path.dirname(sys.argv[0])))
        sys.path.append(path.dirname(path.dirname(sys.argv[0])))
        from libs import dataCls
    else:
        from ..libs.dataCls import DataGenerator


    train_path = './data/감귤/Training'
    print(walk(train_path).__next__())


    # 이미지 주소 및 클래스 라벨 파일 불러오기
    # train_labels = pd.read_csv('train.csv')
    #
    # # 라벨 정보 전처리
    # # 전체 클래스 수
    # class_num = len(train_labels['labels'].unique())
    # # 클래스 -> 숫자로 변환 (카테고리 형식의 클래스를 원 핫 인코딩)
    # labels_dict = dict(zip(train_labels['labels'].unique(), range(class_num)))
    # print(labels_dict)
    # train_labels = train_labels.replace({"labels": labels_dict})




    #
    # tartget_size = 150
    # img_ch = 3
    # num_class = 12
    # batch_size = 32
    #
    # train_generator = dataCls.DataGenerator('train_images/', train_labels['image'],
    #                                 train_labels['labels'],
    #                                 batch_size, tartget_size,
    #                                 img_ch, num_class)
    #
    # print(train_generator)