import numpy as np
import matplotlib.pyplot as plt
import mne
import os, sys
from scipy.io import loadmat
from pathlib import Path
from mne.channels import read_custom_montage

raws = mne.io.read_raw_fif('preprocessed.fif', preload=True)
#打印数据信息
print(raws.info)
#打印数据类型
print(type(raws))
#打印数据长度
print(len(raws))

file_path = r'F:\SEED\SEED_EEG\\Preprocessed_EEG\1_20131027.mat'
dawss = loadmat(file_path)
#打印数据信息
print(dawss)
#打印数据类型
print(type(dawss))
#打印数据长度
print(len(dawss))

#比较两个数据的占据内存大小
      




