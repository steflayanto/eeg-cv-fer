from fer import FER
import matplotlib.pyplot as plt
import cv2
import json
import os
import random as rand
from pathlib import Path

DATA_PATH = "./uploads/dev/"

class AbstractModel:
    DATA_PATH = "./uploads/dev/"
    OUTPUT_PATH = "./output/"
    def __init__(self, sample_rate=2):
        print("Error: called init on abstract class")
        pass

    def run(self, data_path):
        pass

class DefaultCVModel(AbstractModel):
    DATA_PATH = "./uploads/dev/"
    OUTPUT_PATH = "./output/"

    def __init__(self, sample_rate=2, verbose=False):
        self.detector = FER(mtcnn=True)
        self.name = "default-cv"
        self.sample_rate = sample_rate
        self.verbose = verbose

    # def run(self, video_name): # sample data: s01_trial01.avi acting-lady.mp4
    #     data = self.detect_emotions_from_video(self.detector, self.DATA_PATH + video_name, sample_rate=2) # self, video_name, sample_rate, cv_model_name, data, write=False
    #     video_name = video_name.split('.')[0] # Strip off any file extensions .avi
    #     self.write_output(video_name, self.sample_rate, self.name, data, write=True)

    def run(self, data_path): # "s01_trial01.avi"
        data = self.detect_emotions_from_video(self.detector, self.DATA_PATH + data_path, sample_rate=1)
        # detect_still_img(detector, read_img("3-people.jpg"))
        data_path = Path(data_path).stem 
        self.write_output(data_path, self.sample_rate, self.name, data, write=True)
        # self, video_name, sample_rate, cv_model_name, data, write=False

    def detect_still_img(self, image, visualize=False):
    #     img1 = cv2.imread("tiger.jpg", 3)
    #     b,g,r = cv2.split(img)           # get b, g, r
    #     img = cv2.merge([r,g,b])     # switch it to r, g, b
        faces = self.detector.detect_emotions(image)
        
        if len(faces) == 0:
            print("ERROR: No faces detected")
            plt.imshow(image)
            return None
        
        if len(faces) > 1:
            if self.verbose:
                print("WARNING: {} faces detected... selecting largest".format(len(faces)))
            sizes = []
            for face in faces:
                box = face['box']
                sizes.append(box[2] * box[3])
                cv2.rectangle(image,(box[0], box[1]), (box[0] + box[2], box[1] + box[3]),(0, 155, 255), 4,)
            
            max_idx = sizes.index(max(sizes))
            plt.imshow(image)
            return faces[max_idx]['emotions']
    #         return None
        
        box = faces[0]['box']
        emotions = faces[0]['emotions']
        if visualize:
            cv2.rectangle(image,(box[0], box[1]), (box[0] + box[2], box[1] + box[3]),(0, 155, 255), 4,)
            plt.imshow(image)
        return emotions

    """
    Function takes in a facial detector, video path, and a sample rate (Hz).
    It then returns an dictionary of timestamps -> dict of emotions
        
        Example output:
            {
            "0:00.00" : {"angry": 0.1, "happy": 0.5, "otherEmotions":0.4},
            "0:00.50" : {"angry": 0.2, "happy": 0.4, "otherEmotions":0.4}, ...
            }
    """
    def detect_emotions_from_video(self, detector, path, sample_rate=1):
        # print(os.getcwd())
        assert os.path.exists(path), "Error: Path not found " + path
        video = cv2.VideoCapture(path)
        fps = video.get(cv2.CAP_PROP_FPS)
        
        assert fps >= sample_rate, "Error: FPS {} < Sample Rate {}".format(fps, sample_rate)
        if self.verbose:
            print("Processing video {} with FPS: {} at Sample Rate: {} Hz".format(path, fps, sample_rate))
        frame_skip = fps / sample_rate
        i = 0
        data = dict()
        while(video.isOpened()):
            ret, frame = video.read()
            if not ret:
                break

            if i % frame_skip == 0:
                R, G, B = cv2.split(frame)
                frame = cv2.merge([B, G, R])
    #             print("Showing_img")
    #             plt.imshow(frame)
                emotions = self.detect_still_img(frame)
                if not emotions:
                    emotions  = {"angry": 0.0, "disgust": 0.0, "fear": 0.0, "happy": 0.0, "sad": 0.0, "surprise": 0.0, "neutral": 0.0}
                    # break
                data[i / fps] = emotions
            i += 1
        # print(data)
        video.release()    
        return data

    """
    [cvModelName]-[videoPath].json
    {
    "metadata": {
    "videoPath": "filename.mp4",
    "cvLabelFrequency": "2Hz",
    "cvModelName": "default",...
    },
    "data": {
    "0:00.00" : {"angry": 0.1, "happy": 0.5, "otherEmotions":0.4},
    "0:00.50" : {"angry": 0.2, "happy": 0.4, "otherEmotions":0.4}, ...
    }
    }
    """

    def write_output(self, video_name, sample_rate, cv_model_name, data, write=False):
        json_dict = dict()
        json_dict["metadata"] = {"videoPath": video_name, "cvLabelFrequency":sample_rate, "cvModelName":cv_model_name}
        json_dict["data"] = data
    #     json_object = json.dumps(json_dict, indent = 4)  
    #     print(json_object)
        if write:
            with open(self.OUTPUT_PATH + f"{cv_model_name}.json", "w+") as outfile: 
                json.dump(json_dict, outfile)


class RandomCVModel(AbstractModel):
    
    def __init__(self, sample_rate=2, verbose=False):
        self.sample_rate = sample_rate
        self.verbose = verbose
    
    def write_output(self, video_name, sample_rate, cv_model_name, data, write=False):
        json_dict = dict()
        json_dict["metadata"] = {"videoPath": video_name, "cvLabelFrequency":sample_rate, "cvModelName":cv_model_name}
        json_dict["data"] = data
    #     json_object = json.dumps(json_dict, indent = 4)  
    #     print(json_object)
        if write:
            with open(self.OUTPUT_PATH + f"{cv_model_name}.json", "w+") as outfile: 
                json.dump(json_dict, outfile)

    def write_output(self, video_name, sample_rate, cv_model_name, data, write=False):
        json_dict = dict()
        json_dict["metadata"] = {"videoPath": video_name, "cvLabelFrequency":sample_rate, "cvModelName":cv_model_name}
        json_dict["data"] = data
    #     json_object = json.dumps(json_dict, indent = 4)  
    #     print(json_object)
        if write:
            with open(self.OUTPUT_PATH + f"{cv_model_name}.json", "w+") as outfile: 
                json.dump(json_dict, outfile)

    def run(self, data_path):
        path = self.DATA_PATH + data_path
        assert os.path.exists(path), "Error: Path not found " + path
        video = cv2.VideoCapture(path)
        fps = video.get(cv2.CAP_PROP_FPS)
        
        assert fps >= self.sample_rate, "Error: FPS {} < Sample Rate {}".format(fps, self.sample_rate)
        if self.verbose:
            print("Processing video {} with FPS: {} at Sample Rate: {} Hz".format(path, fps, self.sample_rate))
        frame_skip = fps / self.sample_rate
        i = 0
        data = dict()
        while(video.isOpened()):
            ret, _ = video.read()
            if not ret:
                break

            if i % frame_skip == 0:
                nums = [rand.random() for i in range(7)]
                normalized = [num  / sum(nums) for num in nums]
                # print(normalized)
                emotions  = {"angry": normalized[0], "disgust": normalized[1], "fear": normalized[2], "happy": normalized[3], "sad": normalized[4], "surprise": normalized[5], "neutral": normalized[6]}
                data[i / fps] = emotions
            i += 1
        # print(data)
        video.release()    
        self.write_output(data_path, self.sample_rate, "random-cv", data, write=True)

def read_img(img_path):
    return plt.imread(DATA_PATH + img_path)

# def get_area(box):
#     x1, y1 = box[0]
#     x2, y2 = box[2]
#     return (x2 - x1) * (y2 - y1)

if __name__ == '__main__':
    # detector = FER(mtcnn=True)
    # data = detect_emotions_from_video(detector, DATA_PATH + "s01_trial01.avi", sample_rate=2)
    # detect_still_img(detector, read_img("3-people.jpg"))

    # write_output("s01_trial01", 2, "default-mtcnn", data, write=True)
    model = DefaultCVModel()
    model.run("acting-lady.mp4")