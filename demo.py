import numpy as np
import matplotlib.pyplot as plt
import mne
import os, sys
from scipy.io import loadmat
from pathlib import Path
import scipy.io as sio

mat_file = 'F:\SEED\SEED_EEG\Preprocessed_EEG\\1_20131027.mat'
data = loadmat(mat_file)

# # 打印数据的key
# for key in data.keys():
#     if key.startswith('__'):
#         continue
#     print(key)
# #打印数据的shape
# for key in data.keys():
#     if key.startswith('__'):
#         continue
#     print(f"Shape of {key} = {data[key].shape}")
# #打印数据的类型
# for key in data.keys():
#     if key.startswith('__'):
#         continue
#     print(f"Type of {key} = {type(data[key])}")

# 采样频率
sfreq = 200
# 每个.mat文件中的数据label
basic_label = [1, 0, -1, -1, 0, 1, -1, 0, 1, 1, 0, -1, 0, 1, -1]

#通道名
ch_names = ['Fp1','Fpz','Fp2','AF3','AF4','F7','F5','F3','F1','Fz','F2','F4','F6'
            ,'F8','FT7','FC5','FC3','FC1','FCz','FC2','FC4','FC6','FT8','T7','C5'
            ,'C3','C1','Cz','C2','C4','C6','T8','TP7','CP5','CP3','CP1','CPz','CP2'
            ,'CP4','CP6','TP8','P7','P5','P3','P1','Pz','P2','P4','P6','P8','PO7'
            ,'PO5','PO3','POz','PO4','PO6','PO8','CB1','O1','Oz','O2','CB2']

# 读取单个.mat文件
def read_one_file(file_path):
    """
    input:单个.mat文件路径
    output:raw格式数据
    """
    data = sio.loadmat(file_path)
    # 获取keys并转化为list，获取数据所在key
    keys = list(data.keys())[3:]
    # print(keys)
    # 获取数据
    raw_list = []
    for i in range(len(keys)):
        # 获取数据
        stamp = data[keys[i]]
        # print(stamp.shape)
        # 创建info
        info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
        # 创建raw，取第5秒开始的数据
        raw = mne.io.RawArray(stamp, info).crop(tmin=5,tmax=180)
        # 添加到raw_list
        raw_list.append(raw)
    return raw_list


raw_list = read_one_file(mat_file)


#打印数据的类型
for i in range(len(raw_list)):
    print(f"Type of {i} = {type(raw_list[i])}")
#打印数据的信息
for i in range(len(raw_list)):
    print(f"Info of {i} = {raw_list[i].info}")


#存储数据
    
for i in range(len(raw_list)):
     #存到data1文件夹下
    raw_list[i].save('data1' + '\\'+str(i)+'.mat',overwrite=True)
    


