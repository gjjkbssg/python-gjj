import mne
import mne_microstates

from mne.datasets import sample
fname = (sample.data_path() / 'MEG/sample/sample_audvis_raw.fif') #
raw = mne.io.read_raw_fif(fname, preload=True)



# Select sensor type
# raw.pick_types(meg=False, eeg=True)
raw.pick_types(meg='mag', eeg=False)

# Segment the data into 5 microstates
maps, segmentation, polarity = mne_microstates.segment(raw.get_data(), n_states=5,
                                                       random_state=0,
                                                       return_polarity=True)
    
# Plot the topographic maps of the microstates and part of the segmentation
mne_microstates.plot_maps(maps, raw.info)
mne_microstates.plot_segmentation(segmentation[:500], raw.get_data()[:, :500],
                                  raw.times[:500], polarity=polarity[:500])