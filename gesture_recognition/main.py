# main.py
import sys
import cv2
import numpy as np
import time

from unitree_sdk2py.core.channel import ChannelPublisher, ChannelFactoryInitialize
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.utils.thread import Thread
from inspire_sdkpy import inspire_hand_defaut,inspire_dds

from gesture_recognition.landmark import Landmark

def main():
    if len(sys.argv)>1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)
    # Create a publisher to publish the data defined in UserData class
  
    publ = ChannelPublisher("rt/inspire_hand/ctrl/l", inspire_dds.inspire_hand_ctrl)
    publ.Init()
    pubr = ChannelPublisher("rt/inspire_hand/ctrl/r", inspire_dds.inspire_hand_ctrl)
    pubr.Init()
    cmd = inspire_hand_defaut.get_inspire_hand_ctrl()
    short_value=1000

    hand_landmark_detect = Landmark()        
    
    target_positions = [1000]*6
    # # 记录六个关节的最小值与最大值
    # min_vals = [99999] * 6
    # max_vals = [-99999] * 6

    while(1):

        hand_landmark_detect.detect(alpha = 0.1)
        hand_landmark_detect.draw()
        flexion_data = hand_landmark_detect.finger_flexion
        if flexion_data:
            for hand_info in flexion_data:
                print(f"检测到手 ({hand_info['Handedness']}):")
                print(f"  食指 PIP 角度: {hand_info['Index_PIP_Angle']}°")
                target_positions[3] = round(hand_info['Index_PIP_Angle']/180 * 1000)

                print(f"  中指 PIP 角度: {hand_info['Middle_PIP_Angle']}°")
                target_positions[2] = round(hand_info['Middle_PIP_Angle']/180 * 1000)

                print(f"  无名指 PIP 角度: {hand_info['Ring_PIP_Angle']}°")
                target_positions[1] = round(hand_info['Ring_PIP_Angle']/180 * 1000)

                print(f"  小指 PIP 角度: {hand_info['Pinky_PIP_Angle']}°")
                target_positions[0] = round(hand_info['Pinky_PIP_Angle']/180 * 1000)

                print(f"  大指 PIP 角度: {hand_info['Thumb_IP_Angle']}°")

                target_positions[4] = round(np.interp(hand_info['Thumb_IP_Angle'], [110, 180], [1, 999]))

                target_positions[5] = 0

                # for i in range(6):
                #     val = target_positions[i]
                #     min_vals[i] = min(min_vals[i], val)
                #     max_vals[i] = max(max_vals[i], val)
        
            cmd.angle_set=target_positions
            cmd.mode=0b0001
            publ.Write(cmd)
            pubr.Write(cmd)


        if  publ.Write(cmd) and pubr.Write(cmd):
            # print("Publish success. msg:", cmd.crc)
            pass
        else:
            print("Waitting for subscriber.")
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            hand_landmark_detect.destory()
            # print("当前关节最小值：", min_vals)
            # print("当前关节最大值：", max_vals)
            break
    
    

if __name__ == '__main__':

    main()