import json

"""
Reads in input from both CV and EEG, compares them, then returns a combined output.
Input format:
CV:
    {
        "metadata": {"videoPath": "s01_trial01", "cvLabelFrequency": 2, "cvModelName": "default-mtcnn"}, 
        "data": {"0.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.05, "sad": 0.14, "surprise": 0.0, "neutral": 0.77}, "1.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.21, "surprise": 0.0, "neutral": 0.7}, "2.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.38, "surprise": 0.0, "neutral": 0.52}, "3.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.01, "happy": 0.02, "sad": 0.28, "surprise": 0.0, "neutral": 0.65}, "4.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.21, "surprise": 0.0, "neutral": 0.7}, "5.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.01, "happy": 0.04, "sad": 0.16, "surprise": 0.0, "neutral": 0.77}, "6.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.02, "sad": 0.32, "surprise": 0.0, "neutral": 0.61}, "7.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.02, "happy": 0.05, "sad": 0.24, "surprise": 0.0, "neutral": 0.65}, "8.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.14, "sad": 0.16, "surprise": 0.0, "neutral": 0.65}, "9.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.03, "happy": 0.04, "sad": 0.3, "surprise": 0.0, "neutral": 0.6}, "10.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.03, "happy": 0.06, "sad": 0.24, "surprise": 0.0, "neutral": 0.62}, "11.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.04, "sad": 0.4, "surprise": 0.0, "neutral": 0.51}, "12.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.03, "happy": 0.05, "sad": 0.26, "surprise": 0.0, "neutral": 0.63}, "13.0": {"angry": 0.06, "disgust": 0.0, "fear": 0.03, "happy": 0.07, "sad": 0.32, "surprise": 0.0, "neutral": 0.52}, "14.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.01, "happy": 0.03, "sad": 0.25, "surprise": 0.0, "neutral": 0.68}, "15.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.01, "sad": 0.24, "surprise": 0.0, "neutral": 0.7}, "16.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.03, "sad": 0.42, "surprise": 0.0, "neutral": 0.5}, "17.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.28, "surprise": 0.0, "neutral": 0.64}, "18.0": {"angry": 0.05, "disgust": 0.0, "fear": 0.02, "happy": 0.06, "sad": 0.2, "surprise": 0.01, "neutral": 0.66}, "19.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.3, "surprise": 0.0, "neutral": 0.61}, "20.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.07, "sad": 0.2, "surprise": 0.0, "neutral": 0.67}, "21.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.32, "surprise": 0.0, "neutral": 0.6}, "22.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.35, "surprise": 0.0, "neutral": 0.58}, "23.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.01, "happy": 0.01, "sad": 0.16, "surprise": 0.0, "neutral": 0.8}, "24.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.02, "sad": 0.14, "surprise": 0.0, "neutral": 0.79}, "25.0": {"angry": 0.05, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.16, "surprise": 0.0, "neutral": 0.74}, "26.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.02, "happy": 0.12, "sad": 0.18, "surprise": 0.01, "neutral": 0.63}, "27.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.14, "surprise": 0.0, "neutral": 0.77}, "28.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.18, "surprise": 0.0, "neutral": 0.75}, "29.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.07, "sad": 0.33, "surprise": 0.0, "neutral": 0.56}, "30.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.03, "happy": 0.11, "sad": 0.23, "surprise": 0.01, "neutral": 0.58}, "31.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.04, "sad": 0.27, "surprise": 0.0, "neutral": 0.65}, "32.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.02, "happy": 0.02, "sad": 0.26, "surprise": 0.0, "neutral": 0.65}, "33.0": {"angry": 0.07, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.34, "surprise": 0.0, "neutral": 0.54}, "34.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.29, "surprise": 0.0, "neutral": 0.63}, "35.0": {"angry": 0.05, "disgust": 0.0, "fear": 0.02, "happy": 0.06, "sad": 0.18, "surprise": 0.0, "neutral": 0.68}, "36.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.02, "sad": 0.19, "surprise": 0.0, "neutral": 0.75}, "37.0": {"angry": 0.01, "disgust": 0.0, "fear": 0.01, "happy": 0.02, "sad": 0.09, "surprise": 0.0, "neutral": 0.87}, "38.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.02, "sad": 0.21, "surprise": 0.0, "neutral": 0.73}, "39.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.01, "happy": 0.05, "sad": 0.31, "surprise": 0.0, "neutral": 0.59}, "40.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.02, "sad": 0.14, "surprise": 0.01, "neutral": 0.78}, "41.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.21, "surprise": 0.0, "neutral": 0.72}, "42.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.03, "happy": 0.02, "sad": 0.12, "surprise": 0.0, "neutral": 0.8}, "43.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.13, "surprise": 0.0, "neutral": 0.8}, "44.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.02, "sad": 0.18, "surprise": 0.0, "neutral": 0.73}, "45.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.03, "sad": 0.16, "surprise": 0.0, "neutral": 0.77}, "46.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.03, "happy": 0.03, "sad": 0.17, "surprise": 0.01, "neutral": 0.74}, "47.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.03, "happy": 0.02, "sad": 0.14, "surprise": 0.01, "neutral": 0.77}, "48.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.04, "sad": 0.24, "surprise": 0.0, "neutral": 0.68}, "49.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.17, "surprise": 0.0, "neutral": 0.73}, "50.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.03, "happy": 0.03, "sad": 0.13, "surprise": 0.01, "neutral": 0.76}, "51.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.08, "sad": 0.23, "surprise": 0.0, "neutral": 0.63}, "52.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.02, "happy": 0.09, "sad": 0.18, "surprise": 0.0, "neutral": 0.67}, "53.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.16, "surprise": 0.01, "neutral": 0.74}, "54.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.23, "surprise": 0.01, "neutral": 0.67}, "55.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.01, "happy": 0.05, "sad": 0.21, "surprise": 0.01, "neutral": 0.69}, "56.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.02, "happy": 0.06, "sad": 0.21, "surprise": 0.01, "neutral": 0.67}, "57.0": {"angry": 0.03, "disgust": 0.0, "fear": 0.03, "happy": 0.04, "sad": 0.19, "surprise": 0.0, "neutral": 0.7}, "58.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.01, "happy": 0.07, "sad": 0.12, "surprise": 0.01, "neutral": 0.77}, "59.0": {"angry": 0.02, "disgust": 0.0, "fear": 0.02, "happy": 0.05, "sad": 0.11, "surprise": 0.0, "neutral": 0.79}, "60.0": {"angry": 0.04, "disgust": 0.0, "fear": 0.02, "happy": 0.04, "sad": 0.26, "surprise": 0.0, "neutral": 0.64}}
    }
EEG:
    {
        "metadata": {"dataPath": "s01_trial01.npy", "eegLabelFrequency": "1", "eegModelName": "default"}, 
        "data": {"0": 0, "1": 1, "2": 2, "3": 3, "4": 3, "5": 0, "6": 2, "7": 3, "8": 3, "9": 3, "10": 0, "11": 0, "12": 0, "13": 1, "14": 0, "15": 1, "16": 3, "17": 0, "18": 3, "19": 1, "20": 3, "21": 1, "22": 3, "23": 3, "24": 0, "25": 3, "26": 0, "27": 0, "28": 1, "29": 0, "30": 1, "31": 3, "32": 1, "33": 0, "34": 1, "35": 2, "36": 1, "37": 1, "38": 1, "39": 1, "40": 1, "41": 2, "42": 0, "43": 3, "44": 0, "45": 3, "46": 3, "47": 3, "48": 1, "49": 0, "50": 0, "51": 2, "52": 2, "53": 1, "54": 0, "55": 0, "56": 2, "57": 3, "58": 2, "59": 3}
    }

Output format: 
    {
        "metadata": {"eegDataPath": "s01_trial01.npy", "cvDataPath":"s01_trial01.avi", "eegLabelFrequency": "1", "eegModelName": "default", "cvLabelFrequency": "1", "cvModelName": "default", "bsScore": 0.2}, 
        "data": {"0": (cvArousal, cvValence, eegQuadrant, matchBoolean), ...}
    }
"""
class DualModel:
    def __init__(self):
        self.DATA_PATH = "./"
        # disgust mapped to reproach. sad mapped roughly to disappointment and remorse
        self.cat_av_consts = {"angry": (.59,-.62), "disgust": (.47,-.41), "fear": (.47,-.74), "happy": (.17,.75), "sad": (-.1,-.5), "surprise": (.47,-.74), "neutral": (0,0)}

    def cat_to_av(self, cat_dict):
        arousal, valence = 0, 0
        for key, value in cat_dict.items():
            new_arousal, new_valence = self.cat_av_consts[key][0] * value, self.cat_av_consts[key][1] * value
            arousal += new_arousal
            valence += new_valence
        # print(arousal, valence)
        return arousal, valence

    # def av_to_cat(av_tup):
    #     av_tup

    def check_match(self, arousal, valence, eegQuadrant):
        if eegQuadrant == 0:
            return arousal <= 0 and valence <= 0
        elif eegQuadrant == 1:
            return arousal >= 0 and valence <= 0
        elif eegQuadrant == 2:
            return arousal >= 0 and valence >= 0
        elif eegQuadrant == 3:
            return arousal <= 0 and valence >= 0
        else:
            print("ERROR")
            return None

    def read_input(self, eegPath, cvPath):
        cv_data, eeg_data = dict(), dict()

        with open(self.DATA_PATH + eegPath, "r") as infile1: 
            # print("Reading", DATA_PATH + f"{eegModelName}-{eegDataPath}.json")
            eeg_data = json.load(infile1)
        
        with open(self.DATA_PATH + cvPath, "r") as infile2: 
            # print("Reading", DATA_PATH + f"{cvModelName}-{cvDataPath}.json")
            cv_data = json.load(infile2)
        # print(cv_data)
        # print(eeg_data)
        return cv_data, eeg_data

    def write_output(self, metadata, data, write=False):
        json_dict = dict()
        json_dict["metadata"] = metadata
        json_dict["data"] = data
    #     json_object = json.dumps(json_dict, indent = 4)  
    #     print(json_object)
        if write:
            print("Writing to", self.DATA_PATH + f"dual-{metadata['eegModelName']}-{metadata['cvModelName']}.json")
            with open(self.DATA_PATH + f"dual-{metadata['eegModelName']}-{metadata['cvModelName']}.json", "w+") as outfile: 
                json.dump(json_dict, outfile)


    def process_data(self, cv_data, eeg_data):
        # print("Processing data")
        metadata, data = dict(), dict()

        # Create "metadata": {"eegDataPath": "s01_trial01.npy", "cvDataPath":"s01_trial01.avi", "eegLabelFrequency": "1", "eegModelName": "default", "cvLabelFrequency": "1", "cvModelName": "default", "bsScore": 0.2}, 
        metadata['eegDataPath'] = eeg_data['metadata']['dataPath']
        metadata['cvDataPath'] = cv_data['metadata']['videoPath']
        metadata['eegLabelFrequency'] = eeg_data['metadata']['eegLabelFrequency']
        metadata['eegModelName'] = eeg_data['metadata']['eegModelName']
        metadata['cvLabelFrequency'] = cv_data['metadata']['cvLabelFrequency']
        metadata['cvModelName'] = cv_data['metadata']['cvModelName']
        
        # Process data
        cv_trial = cv_data['data']
        eeg_trial = eeg_data['data']
        data = dict()
        # print(cv_data, "\n-----------------------------------------\n" ,eeg_data)
        #assert len(cv_trial) == len(eeg_trial), f"Invalid lengths. cv:{len(cv_trial)} and eeg:{len(eeg_trial)}"

        match_count = 0
        for key in cv_trial.keys():
            arousal, valence = self.cat_to_av(cv_trial[key])
            if (str(int(float(key))) not in eeg_trial.keys()):
                # print("Did  not find key for", key)
                break
            eeg_quadrant = eeg_trial[str(int(float(key)))]
            data[key] = arousal, valence, eeg_quadrant, self.check_match(arousal, valence, eeg_quadrant)
            if data[key][2]:
                match_count += 1
            # print(data[key])

        metadata['bsScore'] = match_count / len(cv_trial)
        # print(metadata)
        # print(data)

        return metadata, data

    def run(self, eeg_path, cv_path):
        cv_data, eeg_data = self.read_input(eeg_path, cv_path)
        metadata, data = self.process_data(cv_data, eeg_data)
        self.write_output(metadata, data, write=True)

