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
imp

# Define the function for computing PSD
def compute_psd(raw):
    # Perform PSD computation on the raw object
    # and return the computed PSD
    freqs=200
    psd, freqs = mne.time_frequency.psd_welch(raw)
    return psd

# Define the file paths for the five fif files
file_paths = [
    'alpha.fif',
    'beta.fif',
    'delta.fif',
    'sigma.fif',
    'theta.fif'
]

# Load the fif files
raws = []
for file_path in file_paths:
    raw = mne.io.read_raw_fif(file_path)
    raws.append(raw)

# Apply feature extraction on each raw object
features = []
for raw in raws:
    # Perform feature extraction on the raw object
    # and append the extracted features to the features list
    psd = compute_psd(raw)
    de = compute_de(raw)
    stats = compute_statistics(raw)
    extracted_features = {
        'psd': psd,
        'de': de,
        'statistics': stats
    }
    features.append(extracted_features)

# Define the function for computing PSD
def compute_psd(raw):
    # Perform PSD computation on the raw object
    # and return the computed PSD
    freqs=200
    psd, freqs = mne.time_frequency.psd_welch(raw)
    return psd

# Define the function for computing DE
def compute_de(raw):
    # Perform DE computation on the raw object
    # and return the computed DE

    de = ...
    return de

# Define the function for computing statistics
def compute_statistics(raw):
    # Perform statistical computations on the raw object
    # and return the computed statistics
    stats = ...
    return stats