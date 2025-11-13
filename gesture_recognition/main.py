# main.py
import sys
from typing import List, Dict
from gesture_recognition.landmark import Landmark
import cv2
import numpy as np
# import time

# from unitree_sdk2py.core.channel import ChannelPublisher, ChannelFactoryInitialize
# from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
# from unitree_sdk2py.utils.thread import Thread

# from inspire_sdkpy import inspire_hand_defaut,inspire_dds


def main():

    hand_landmark_detect = Landmark()        
    
    while(1):

        hand_landmark_detect.detect(alpha = 0.1)
        hand_landmark_detect.draw()
        flexion_data = hand_landmark_detect.finger_flexion

        if flexion_data:
            for hand_info in flexion_data:
                print(1)
                
        if cv2.waitKey(10) & 0xFF == ord('q'):
            hand_landmark_detect.destory()
            break
    
    

if __name__ == '__main__':

    main()