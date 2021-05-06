import sys, getopt

from models.interface import DefaultCVModel

usage = "Usage: modelRunner.py [-n, --modelName] cv-default-mtcnn [-f, --labelFrequency] 2 [-d, --dataPath] video_or_eegfilename"

def main(argv):
    model_name, sample_rate, data_path = None, None, None
    try:
        opts, args = getopt.getopt(argv,"hn:f:d:",["modelName=","labelFrequency=","dataPath="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ("-n", "--modelName"):
            model_name = arg
        elif opt in ("-f", "--labelFrequency"):
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
        elif opt in ("-d", "--dataPath"):
            data_path = arg
    if None in (model_name, sample_rate, data_path):
        print("Error: Missing an argument.")
        print(usage)
        sys.exit()
    return model_name, sample_rate, data_path

if __name__ == "__main__":
    ret = main(sys.argv[1:])
    if not ret:
        print("Error parsing args")
    model_name, sample_rate, data_path = ret
    print('Running model: {}, at frequency {} Hz, on data: {}'.format(model_name, sample_rate, data_path))
    model = DefaultCVModel(sample_rate=sample_rate)
    model.run("s01_trial01.avi")