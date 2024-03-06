import numpy as np
import matplotlib.pyplot as plt
import mne
import os, sys
from scipy.io import loadmat
from pathlib import Path
from mne.channels import read_custom_montage
#导入fastica
from mne.preprocessing import ICA
from sklearn.decomposition import FastICA
import mne_microstates
from sklearn.neighbors import KNeighborsClassifier

"""
通过mne.io.read_raw_eeglab来读取.set文件
得到原始数据对象
"""
raw = mne.io.read_raw_eeglab("F:\SEED\SEED_EEG\Preprocessed_EEG\gjj\gjj2\\15_20131105Data15.set",preload=True,verbose=True)

raw.plot(start=5, duration=5)
plt.show()

# 使用陷波滤波器49-51Hz去除工频干扰
raw.notch_filter([49, 51], fir_design='firwin')

# 使用ICA去除眼动伪迹
ica = ICA(n_components=20, random_state=97, max_iter=800).fit(raw) # 这一步是训练ICA模型
ica.fit(raw)
ica.plot_components(range(20), inst=raw) # 画出ICA成分
ica.exclude = [0]  # Exclude the first component (eye blink)
raw = ica.apply(raw)

# 使用带通滤波器0.05-47Hz对数据进行滤波处理
raw.filter(0.05, 47, fir_design='firwin')

# 重新绘制滤波后的数据
raw.plot(start=5, duration=5)
plt.show()

#提取特征



print("功率谱密度特征提取开始...")
# 计算每个频段的功率谱密度
# 特定频带
FREQ_BANDS = {"delta": [0.5, 4.5],
                  "theta": [4.5, 8.5],
                  "alpha": [8.5, 11.5],
                  "sigma": [11.5, 15.5],
                  "beta": [15.5, 30]}
# 特征矩阵
feature_matrix = []
# 遍历每个raw
for raw in raws: # raws是一个列表，每个元素是一个raw对象
        # 生成频谱特征向量
    feature_vector = []
        # 遍历每个频段
    for band in FREQ_BANDS:
            # 计算功率谱密度
        power = raw.compute_psd(picks='all', method='welch', fmin=FREQ_BANDS[band][0],
                                           fmax=FREQ_BANDS[band][1], verbose=False)
        # print(power.shape)
        # 添加到特征向量，在第二个维度方向扩展
        for i in range(power.shape[0]):
            feature_vector.extend(power[i])
    # 添加到特征矩阵
    # print(len(feature_vector))
    feature_matrix.append(feature_vector)
    # 将特征矩阵转换为numpy数组
feature_matrix = np.array(feature_matrix, dtype=object)


   

