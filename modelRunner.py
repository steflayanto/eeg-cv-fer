import sys, getopt

from models.interface import DefaultCVModel
from models.eegdcnnmodel import EEGDCNNModel

usage = "Usage: modelRunner.py [-n, --modelName] defaultcv [-l, --labelFrequency] 2 [-f, --dataFrequency] 2 [-d, --dataPath] video_or_eegfilename"

def main(argv):
    model_name, sample_rate, data_freq, data_path = None, None, None, None
    try:
        opts, args = getopt.getopt(argv,"hn:lfd:",["modelName=","labelFrequency=","dataFrequency=","dataPath="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ("-n", "--modelName"):
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
    if None in (model_name, data_path):
        print("Error: Missing an argument.")
        print(usage)
        sys.exit()
    return model_name, sample_rate, data_freq, data_path

if __name__ == "__main__":
    ret = main(sys.argv[1:])
    if not ret:
        print("Error parsing args")
    model_name, sample_rate, data_freq, data_path = ret
    print('Running model: {}, at frequency {} Hz, on data: {}'.format(model_name, sample_rate, data_path))
    if model_name == "defaultcv":
        if sample_rate:
            model = DefaultCVModel(sample_rate=sample_rate)
        else:
            model = DefaultCVModel()
        model.run(data_path)
    elif model_name == "defaulteeg":
        if sample_rate and data_freq:
            model = EEGDCNNModel(sample_rate=sample_rate, data_frequency=data_freq)
        else:
            model = EEGDCNNModel()
        model.run(data_path)
    