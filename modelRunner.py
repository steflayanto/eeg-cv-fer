import sys, getopt

from models.interface import DefaultCVModel, RandomCVModel
from models.eegdcnnmodel import EEGDCNNModel
from models.dualmodel import DualModel

usage = "Usage:\n\tmodelRunner.py [-n, --modelName] defaultcv [-l, --labelFrequency] 2 [-f, --dataFrequency] 2 [-d, --dataPath] video_or_eegfilename \nOR\n\tmodelRunner.py -n dual [-c, --cvPath] default-cv.json [-e, --eegPath] default-eeg.json"

def main(argv):
    model_name, sample_rate, data_freq, data_path, cv_path, eeg_path = None, None, None, None, None, None
    try:
        # print(argv)
        opts, args = getopt.getopt(argv,"hn:l:f:d:c:e:")
        # print(opts, args)
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ("-n", "--modelName"):
            # print("Printing Model Name", opt, arg)
            model_name = arg
        elif opt in ("-l", "--labelFrequency"):
            try:
                sample_rate = int(arg)
                if not sample_rate:
                    print("Error parsing labelFrequency: ", arg)
                    sys.exit()
                if sample_rate < 1:
                    print("Invalid sample rate:", sample_rate)
                    sys.exit()
            except Exception as e:
                print("Error parsing labelFrequency: ", e)
                sys.exit()
        elif opt in ("-f", "--dataFrequency"):
            try:
                data_freq = int(arg)
                if not data_freq:
                    print("Error parsing dataFrequency: ", arg)
                    sys.exit()
                if data_freq < 1:
                    print("Invalid data frequency:", data_freq)
                    sys.exit()
            except Exception as e:
                print("Error parsing dataFrequency: ", e)
                sys.exit()
        elif opt in ("-d", "--dataPath"):
            data_path = arg
        elif opt in ("-c", "--cvPath"):
            cv_path = arg
        elif opt in ("-e", "--eegPath"):
            eeg_path = arg
    if None in (model_name, data_path) and model_name != 'dual':
        print("Error: Missing an argument.", model_name, "oi")
        print(usage)
        sys.exit()
    return model_name, sample_rate, data_freq, data_path, cv_path, eeg_path

if __name__ == "__main__":
    ret = main(sys.argv[1:])
    if not ret:
        print("Error parsing args")
    model_name, sample_rate, data_freq, data_path, cv_path, eeg_path = ret
    if model_name == "defaultcv":
        print('Running model: {}, at frequency {} Hz, on data: {}'.format(model_name, sample_rate, data_path))
        if sample_rate:
            model = DefaultCVModel(sample_rate=sample_rate)
        else:
            model = DefaultCVModel()
        model.run(data_path)
    if model_name == "randomcv":
        print('Running model: {}, at frequency {} Hz, on data: {}'.format(model_name, sample_rate, data_path))
        if sample_rate:
            model = RandomCVModel(sample_rate=sample_rate)
        else:
            model = RandomCVModel()
        model.run(data_path)
    elif model_name == "defaulteeg":
        print('Running model: {}, at frequency {} Hz, on data: {}'.format(model_name, sample_rate, data_path))
        if sample_rate and data_freq:
            model = EEGDCNNModel(sample_rate=sample_rate, data_frequency=data_freq)
        else:
            model = EEGDCNNModel()
        model.run(data_path)
    elif model_name == "dual":
        print("Running dual model on {} and {}".format(eeg_path, cv_path))
        model = DualModel()
        model.run(eeg_path, cv_path)
    else:
        print("Error: Model not found")