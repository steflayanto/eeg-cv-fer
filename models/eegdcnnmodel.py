# -*- coding: utf-8 -*-
try:
  from models.interface import AbstractModel
except:
  from interface import AbstractModel

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

class EEGDCNNModel(AbstractModel):
  DATA_PATH = "./"
  OUTPUT_PATH = "./"

  def __init__(self, sample_rate=1, data_frequency=128):
    model = nn.Sequential(
      nn.Conv2d(4, 32, [3, 1]),
      nn.ReLU(),
      nn.Dropout(),
      nn.Conv2d(32, 64, [3, 1]),
      nn.ReLU(),
      nn.Dropout(),
      nn.MaxPool2d([3, 3]),
      nn.Flatten(),
      nn.Linear(5760, 512),
      nn.ReLU(),
      nn.Linear(512, 256),
      nn.ReLU(),
      nn.Linear(256, 4)
    )
    self.model = model
    base_path = Path(__file__).parent
    self.model.load_state_dict(torch.load((base_path / 'model_multi.pth').resolve(), 'cpu'))
    self.model.eval()
    self.sample_rate = sample_rate
    self.data_frequency = data_frequency
    print("Initialized EEG DCNN Model with sample rate {} data freq {}".format(self.sample_rate, self.data_frequency))

  # data passed in is one trial with only the 32 channels with last 3 sec trimmed
  # period has to be a factor of the total clip length
  
  def run(self, data_path):
    print("Running EEG DCNN Model")
    self.run_eeg(self.DATA_PATH + data_path, self.data_frequency, self.sample_rate)

  def run_eeg(self, data_path, data_frequency, sample_rate):
    self.data = np.array(pickle.load(open(data_path, "rb"), encoding='latin1'))
    # data is 32 channel, 7680 (60 * 128)
    channels_total = self.data.shape[0]
    time_total = self.data.shape[1]
    windows = int((time_total / data_frequency) * sample_rate)
    final_data = []
    # sliding window is 8 because thats what the window was when training
    train_sliding_window = 4
    # loops through all the windows
    for i in range(windows - train_sliding_window):
      time_window = self.data[:, int((data_frequency * i) / sample_rate): int((data_frequency * (i + train_sliding_window)) / sample_rate)]
      transformed_channel = []
      # loops through all the channels
      for channel_num in range(channels_total):
        channel_data = time_window[channel_num]
        # convert to frequency domain
        fft_channel = np.abs(rfft(channel_data))
        fftfreq_channel = rfftfreq(channel_data.size, 1/ data_frequency)
        # fft_channel_normalized = np.fft.fftshift(fft_channel / channel_data.size)
        # power_spectrum = np.square(fft_channel_normalized)
        # power = np.sum(power_spectrum)
        # identify frequency ranges
        one_freq = np.where(fftfreq_channel == 1)[0][0]
        eight_freq = np.where(fftfreq_channel == 8)[0][0]
        fourteen_freq = np.where(fftfreq_channel == 14)[0][0]
        thirty_freq = np.where(fftfreq_channel == 30)[0][0]
        fourtyfive_freq = np.where(fftfreq_channel == 45)[0][0]
        # make bins for frequency ranges
        theta_bin = fft_channel[one_freq:eight_freq]
        alpha_bin = fft_channel[eight_freq:fourteen_freq]
        beta_bin = fft_channel[fourteen_freq:thirty_freq]
        gamma_bin = fft_channel[thirty_freq:fourtyfive_freq]
        all_bins = [theta_bin, alpha_bin, beta_bin, gamma_bin]
        transformed_channel.append(all_bins)
      binned_pcc_matrix = np.ones((4, channels_total, channels_total)) # 4, 32, 32
      for bin_num in range(4):
        pcc_matrix = binned_pcc_matrix[bin_num]  # 32, 32
        index_mover = 0
        # creates correlation matrices for each bin
        for channel_num_i in range(0, channels_total):
          for channel_num_j in range(index_mover, channels_total):
            data1 = transformed_channel[channel_num_i][bin_num]
            data2 = transformed_channel[channel_num_j][bin_num]
            pcc_num = scipy.stats.pearsonr(data1, data2)[0]
            pcc_matrix[channel_num_i][channel_num_j] = pcc_num
            pcc_matrix[channel_num_j][channel_num_i] = pcc_num
          index_mover += 1
      binned_pcc_matrix[bin_num] = pcc_matrix
      final_data.append(binned_pcc_matrix)
    # makes last 8 sec the same as the last output
    for i in range(min(windows, train_sliding_window)):
      final_data.append(binned_pcc_matrix)
    self.data = torch.tensor(final_data).float()
    # run model
    output = self.model(self.data)
    _, preds = torch.max(output, 1)
    # output data as json
    json_data = dict()
    for i in range(len(preds)):
      json_data[i / sample_rate] = int(preds[i])
    json_dict = dict()
    json_dict["metadata"] = {"dataPath": data_path, "eegLabelFrequency": str(sample_rate), "eegModelName":"defaulteeg"}
    json_dict["data"] = json_data
    with open(self.OUTPUT_PATH + 'defaulteeg.json', "w+") as outfile: 
       json.dump(json_dict, outfile)

def test_output_format_eeg():
    model = EEGDCNNModel(sample_rate=2)
    model.OUTPUT_PATH = './output/'
    print("Testing output format")
    model.run('uploads/dev/s01_trial01.dat')
    output = json.load(open('output/defaulteeg.json', 'r'))
    # print(type(output), output)
    assert set(output.keys()) == set(['metadata', 'data']), "Error: wrong keys in output json: " + str(output.keys())
    assert "59.0" in output['data'].keys() and '58.5' in output['data'].keys(), "Error with timestamps: " + str(output['data'].keys())
    print("Passed output test")

def test_parameters_eeg():
    print("Testing model parameters")
    model = EEGDCNNModel(sample_rate=4)
    model.OUTPUT_PATH = './output/'
    model.run('uploads/dev/s01_trial01.dat')
    output = json.load(open('output/defaulteeg.json', 'r'))
    assert str(output['metadata']['eegLabelFrequency']) == '4', "Error setting eegLabelFrequency: " + str(output['metadata'])
    print("Passed parameter test")


if __name__ == "__main__":
  # test_run = EEGDCNNModel(sample_rate=1, data_frequency=128)
  # test_run.run('s01_trial01.dat')
  test_output_format_eeg()
  test_parameters_eeg()