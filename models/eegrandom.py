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

class RandomEEGModel(AbstractModel):
  DATA_PATH = "./"

  def __init__(self, sample_rate=1, data_frequency=128):
    base_path = Path(__file__).parent
    self.sample_rate = sample_rate
    self.data_frequency = data_frequency
    print("Initialized EEG DCNN Model with sample rate {} data freq {}".format(self.sample_rate, self.data_frequency))

  # data passed in is one trial with only the 32 channels with last 3 sec trimmed
  # period has to be a factor of the total clip length
  
  def run(self, data_path):
    print("Running EEG Random Model")
    self.run_eeg(self.DATA_PATH + data_path, self.data_frequency, self.sample_rate)

  def run_eeg(self, data_path, data_frequency, sample_rate):
    self.data = np.array(pickle.load(open(data_path, "rb"), encoding='latin1'))
    # data is 32 channel, 7680 (60 * 128)
    #channels_total = self.data.shape[0]
    time_total = self.data.shape[1]
    windows = int((time_total / data_frequency) * sample_rate)
    final_data = []
    # sliding window is 8 because thats what the window was when training
    train_sliding_window = 8
    # loops through all the windows
    for i in range(windows - train_sliding_window):
        final_data.append(np.random.randint(4))
    # makes last 8 sec the same as the last output
    for i in range(min(windows, train_sliding_window)):
      final_data.append(np.random.randint(4))
    # output data as json
    json_data = dict()
    for i in range(len(final_data)):
      json_data[i / sample_rate] = final_data[i]
    json_dict = dict()
    json_dict["metadata"] = {"dataPath": data_path, "eegLabelFrequency":str(sample_rate), "eegModelName":"randomeeg"}
    json_dict["data"] = json_data
    with open('./randomeeg.json', "w+") as outfile: 
      json.dump(json_dict, outfile)