from models.interface import AbstractModel

import torch
import torch.nn.functional as F
import torch.nn as nn
import torchvision
import torchvision.datasets as datasets
import matplotlib.pyplot as plt
import numpy as np
import pickle
from torch import Tensor
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from scipy.fft import rfft, rfftfreq, fft, fftfreq
import scipy
import time
import copy
import json
from pathlib import Path

class EEGPower(AbstractModel):
  DATA_PATH = "./"

  def __init__(self, sample_rate=1, data_frequency=128):
    self.sample_rate = sample_rate
    self.data_frequency = data_frequency
    print("Initialized EEG Power with sample rate {} data freq {}".format(self.sample_rate, self.data_frequency))

  # data passed in is one trial with only the 32 channels with last 3 sec trimmed
  # period has to be a factor of the total clip length
  
  def run(self, data_path):
    print("Running EEG Power")
    self.run_eeg(self.DATA_PATH + data_path, self.data_frequency, self.sample_rate)

  def run_eeg(self, data_path, data_frequency, sample_rate):
    self.data = np.array(pickle.load(open(data_path, "rb"), encoding='latin1'))
    # data is 32 channel, 7680 (60 * 128)
    channels_total = self.data.shape[0]
    time_total = self.data.shape[1]
    windows = int((time_total / data_frequency) * sample_rate)
    final_data = []
    # sliding window is 1 because thats what the window was when training
    train_sliding_window = 1
    # loops through all the windows
    for i in range(windows - train_sliding_window):
      time_window = self.data[:, int((data_frequency * i) / sample_rate): int((data_frequency * (i + train_sliding_window)) / sample_rate)]
      bins = []
      # loops through all the channels
      for channel_num in range(channels_total):
        channel_data = time_window[channel_num]
        # convert to frequency domain
        fft_channel = np.abs(rfft(channel_data))
        fftfreq_channel = rfftfreq(channel_data.size, 1/ data_frequency)
        fft_channel_normalized = fft_channel / channel_data.size
        power_spectrum = np.square(fft_channel_normalized)
        # identify frequency ranges
        one_freq = np.where(fftfreq_channel == 1)[0][0]
        eight_freq = np.where(fftfreq_channel == 8)[0][0]
        fourteen_freq = np.where(fftfreq_channel == 14)[0][0]
        thirty_freq = np.where(fftfreq_channel == 30)[0][0]
        fourtyfive_freq = np.where(fftfreq_channel == 45)[0][0]
        # make bins for frequency ranges
        theta_bin = power_spectrum[one_freq:eight_freq]
        alpha_bin = power_spectrum[eight_freq:fourteen_freq]
        beta_bin = power_spectrum[fourteen_freq:thirty_freq]
        gamma_bin = power_spectrum[thirty_freq:fourtyfive_freq]
        all_bins = [np.sum(theta_bin), np.sum(alpha_bin), np.sum(beta_bin), np.sum(gamma_bin)]
        bins.append(all_bins)
      final_data.append(bins)
    # makes last 1 sec the same as the last output
    for i in range(min(windows, train_sliding_window)):
      final_data.append(bins)
    # self.data = torch.tensor(final_data).float()
    # print(self.data.shape)
    # output data as json
    json_data = dict()
    for i in range(len(final_data)):
      json_channels = dict()
      for j in range(len(final_data[0])):
        json_channels[j] = {"theta": final_data[i][j][0], "alpha": final_data[i][j][1], "beta": final_data[i][j][2], "gamma": final_data[i][j][3]}
      json_data[i / sample_rate] = json_channels
    json_dict = dict()
    json_dict["metadata"] = {"dataPath": data_path, "eegLabelFrequency":str(sample_rate), "eegModelName":"defaulteegpower"}
    json_dict["data"] = json_data
    with open('./defaulteegpower.json', "w+") as outfile: 
      json.dump(json_dict, outfile)
