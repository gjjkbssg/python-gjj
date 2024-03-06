"""
Global Field Power peaks
========================

This example demonstrates how to extract
:term:`Global Field Power` (:term:`GFP`) peaks from an EEG recording.
"""

#%%
# .. include:: ../../../../links.inc

#%%
# .. note::
#
#     The lemon datasets used in this tutorial is composed of EEGLAB files. To
#     use the MNE reader :func:`mne.io.read_raw_eeglab`, the ``pymatreader``
#     optional dependency is required. Use the following installation method
#     appropriate for your environment:
#
#     - ``pip install pymatreader``
#     - ``conda install -c conda-forge pymatreader``
#
#     Note that an environment created via the `MNE installers`_ includes
#     ``pymatreader`` by default.

import mne
from mne.io import read_raw_eeglab
ch_names = ['Fp1','Fpz','Fp2','AF3','AF4','F7','F5','F3','F1','Fz','F2','F4','F6'
            ,'F8','FT7','FC5','FC3','FC1','FCz','FC2','FC4','FC6','FT8','T7','C5'
            ,'C3','C1','Cz','C2','C4','C6','T8','TP7','CP5','CP3','CP1','CPz','CP2'
            ,'CP4','CP6','TP8','P7','P5','P3','P1','Pz','P2','P4','P6','P8','PO7'
            ,'PO5','PO3','POz','PO4','PO6','PO8','CB1','O1','Oz','O2','CB2']
std1020_eeglab = mne.channels.read_custom_montage("channel_62_pos.locs")
info = mne.create_info(ch_names=ch_names, sfreq=200, ch_types='eeg')


raw = read_raw_eeglab('F:\SEED\SEED_EEG\Preprocessed_EEG\gjj\gjj1\\15_20131105Data1.set', preload=True)

raw.pick('eeg')
raw.set_eeg_reference('average')

#%%
# :term:`Global Field Power` (:term:`GFP`) is computed as the standard
# deviation of the sensors at a given timepoint. Local maxima of the
# :term:`Global Field Power` (:term:`GFP`) are known to represent the portions
# of EEG data with highest signal-to-noise ratio\ :footcite:p:`KOENIG20161104`.
# We can use the :func:`~pycrostates.preprocessing.extract_gfp_peaks`
# function to extract samples with the highest Global Field Power.
# The minimum distance between consecutive peaks can be defined with the
# ``min_peak_distance`` argument.

from pycrostates.preprocessing import extract_gfp_peaks
gfp_data = extract_gfp_peaks(raw, min_peak_distance=3)
gfp_data

#%%
# :term:`GFP` peaks can also be extracted from an :class:`~mne.Epochs` object.

epochs = mne.make_fixed_length_epochs(raw, duration=20, preload=True) # 2s epochs
gfp_data = extract_gfp_peaks(epochs, min_peak_distance=3)
gfp_data

#%%
# The extracted :term:`GFP` peaks can be used in other preprocessing steps,
# such as a resampling using :func:`~pycrostates.preprocessing.resample`:

from pycrostates.preprocessing import resample
# extract 1 resample of 100 random high GFP samples
resample = resample(gfp_data, n_resamples=1, n_samples=100)
resample[0]

#%%
# Or they can be used to fit a clustering algorithm on the portion of EEG data
# with the highest signal-to-noise ratio.

from pycrostates.cluster import ModKMeans
ModK = ModKMeans(n_clusters=5, random_state=42)
ModK.fit(gfp_data, n_jobs=5, verbose="WARNING")
ModK.plot()

#%%
# References
# ----------
# .. footbibliography::
