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


# 确保文件路径正确
file_path = r'F:\SEED\SEED_EEG\\Preprocessed_EEG\1_20131027.mat'

# 检查文件是否存在
if not Path(file_path).is_file():
    print(f"File not found: {file_path}")
    sys.exit(1)

try:
    raw_file = loadmat(file_path)
except Exception as e:
    print(f"Failed to load file: {e}")
    sys.exit(1)

# 读取自定义蒙太奇
try:
    std1020_eeglab = mne.channels.read_custom_montage("channel_62_pos.locs")
except FileNotFoundError:
    print("Montage file not found. Please check the file path.")
    sys.exit(1)

ch_names = ['Fp1','Fpz','Fp2','AF3','AF4','F7','F5','F3','F1','Fz','F2','F4','F6'
            ,'F8','FT7','FC5','FC3','FC1','FCz','FC2','FC4','FC6','FT8','T7','C5'
            ,'C3','C1','Cz','C2','C4','C6','T8','TP7','CP5','CP3','CP1','CPz','CP2'
            ,'CP4','CP6','TP8','P7','P5','P3','P1','Pz','P2','P4','P6','P8','PO7'
            ,'PO5','PO3','POz','PO4','PO6','PO8','CB1','O1','Oz','O2','CB2']


#创建一个空raw来存储数据
info = mne.create_info(ch_names=ch_names, sfreq=200, ch_types='eeg')
raw = mne.io.RawArray(np.zeros((len(ch_names), 1)), info)
# 处理.mat文件中的数据
for key in raw_file.keys():
    if key.startswith('__'):
        continue

    data = raw_file[key] # 读取数据
    print(f"Processing {key}: Shape = {data.shape}")

    info = mne.create_info(ch_names=ch_names, sfreq=200, ch_types='eeg')
    try:
        raw = mne.io.RawArray(data, info)
    except Exception as e:
        print(f"Failed to create Raw object for {key}: {e}")

scalings = {'eeg': 50} #
raw.load_data()
raw.plot(scalings=scalings)
plt.show(block=True)

# 插值处理
raw_pass = raw.copy()
raw_pass.load_data()
raw_pass.set_montage(std1020_eeglab, on_missing='warn')
raw_pass.interpolate_bads()
raw_pass.plot(scalings=scalings)
plt.show(block=True)

# 滤波处理
raw_pass.filter(1, 40)
raw_pass.plot(scalings=scalings)
plt.show(block=True)

# 重参考
raw_pass.set_eeg_reference(ref_channels='average', projection=True)
#应用参考投影
raw_pass.apply_proj()
raw_pass.plot(scalings=scalings)
plt.show(block=True)

# 用mne的ICA进行去噪
ica = ICA(n_components=20, random_state=97, max_iter=800).fit(raw_pass) # 这一步是训练ICA模型
ica.fit(raw_pass)
ica.plot_components(range(20), inst=raw_pass) # 画出ICA成分


ica.apply(raw_pass) # 这一步是应用ICA模型
raw_pass.plot(scalings=scalings)
plt.show(block=True)



# 保存处理后的数据
raw_pass.save('test1-raw.fif', overwrite=True) # 保存处理后的数据
print("File saved successfully.")

#对比处理前后的数据
raw.plot(scalings=scalings)
plt.show(block=True)
raw_pass.plot(scalings=scalings)
plt.show(block=True)



# 分割数据为5个频段
freq_bands = [(1, 3), (3, 7), (8, 13), (14, 30), (31, 45)]

# 创建空列表来存储分割后的数据
segmented_data = []

# 遍历每个频段
for band in freq_bands:
    # 使用mne的filter方法过滤数据
    filtered_data = raw_pass.copy().filter(band[0], band[1])
    segmented_data.append(filtered_data)

# 画出分割后的数据
for data in segmented_data:
    data.plot(scalings=scalings)
    plt.show(block=True)

# 保存分割后的数据
for i, data in enumerate(segmented_data):
    data.save(f'segmented_{i}.fif', overwrite=True)


fname = ('alpha.fif') #
raw = mne.io.read_raw_fif(fname, preload=True)
raw.set_montage(std1020_eeglab, on_missing='warn')



# Select sensor type

raw.pick_types(meg=False, eeg=True)

#raw.pick_types(meg='mag', eeg=False)

# Segment the data into 5 microstates
maps, segmentation, polarity = mne_microstates.segment(raw.get_data(), n_states=5,
                                                       random_state=0,
                                                       return_polarity=True,)
    
# Plot the topographic maps of the microstates and part of the segmentation
mne_microstates.plot_maps(maps, raw.info)
#画彩图
mne_microstates.plot_segmentation(segmentation[:500], raw.get_data()[:, :500],
                                  raw.times[:500], polarity=polarity[:500],)









                  






