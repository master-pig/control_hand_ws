#@markdown We implemented some functions to visualize the hand landmark detection results. <br/> Run the following cell to activate the functions.

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import math

def calculate_angle(p1_coord, p2_coord, p3_coord):
    """计算由三个坐标点 p1-p2-p3 构成的夹角（以 p2 为顶点），单位：度。"""
    
    # 将 MediaPipe 的 NormalizedLandmark 对象转换为 NumPy 数组
    # 注意：这里我们假设传入的 pX_coord 已经是 NumPy 数组 (x, y, z)
    v_a = p1_coord - p2_coord
    v_b = p3_coord - p2_coord
    
    dot_product = np.dot(v_a, v_b)
    magnitude_a = np.linalg.norm(v_a)
    magnitude_b = np.linalg.norm(v_b)
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
        
    cosine_angle = dot_product / (magnitude_a * magnitude_b)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle_degrees = math.degrees(math.acos(cosine_angle))

    # cross_z = v_a[0] * v_b[1] - v_a[1] * v_b[0]

    # # 如果你希望右侧为正：
    # if cross_z < 0:
    #     angle_degrees = +angle_degrees  # 右侧 → 正
    # else:
    #     angle_degrees = -angle_degrees   # 左侧 → 负
    
    return angle_degrees

def get_full_finger_flexion(detection_result):
    """
    计算检测到的每只手所有五个手指的多个关节弯曲角度。
    
    Args:
        detection_result: MediaPipe HandLandmarkerResult 对象。
        
    Returns:
        list of dict: 包含每只手及其所有手指多关节弯曲角度的列表。
    """
    flexion_results = []

    # MediaPipe 手部关键点的索引定义
    # 0: Wrist (手腕)
    # 食指 (Index Finger): 5 (MCP), 6 (PIP), 7 (DIP), 8 (TIP)
    # 中指 (Middle Finger): 9 (MCP), 10 (PIP), 11 (DIP), 12 (TIP)
    # 无名指 (Ring Finger): 13 (MCP), 14 (PIP), 15 (DIP), 16 (TIP)
    # 小指 (Pinky Finger): 17 (MCP), 18 (PIP), 19 (DIP), 20 (TIP)
    
    # 关键点索引定义：[关节1的前一点, 关节顶点/中点, 关节的后一点]
    # 我们用三个关键点来测量一个关节的弯曲角度。
    
    # 【四指】：MCP (指根) - PIP (中间关节) - DIP (远端关节)
    # 【拇指】：CMC/Wrist - MP (掌指关节) - IP (指间关节)
    
    FINGER_JOINTS_MAPPING = {
        "Thumb_MP":  [1, 2, 3],  # 拇指掌指关节 (Wrist-MP-IP)
        "Thumb_IP":  [2, 3, 4],  # 拇指指间关节 (MP-IP-TIP)
        
        "Index_PIP": [5, 6, 7],  # 食指近端指间关节 (MCP-PIP-DIP)
        "Index_DIP": [6, 7, 8],  # 食指远端指间关节 (PIP-DIP-TIP)
        
        "Middle_PIP": [9, 10, 11], # 中指 PIP 关节
        "Middle_DIP": [10, 11, 12], # 中指 DIP 关节
        
        "Ring_PIP": [13, 14, 15], # 无名指 PIP 关节
        "Ring_DIP": [14, 15, 16], # 无名指 DIP 关节
        
        "Pinky_PIP": [17, 18, 19], # 小指 PIP 关节
        "Pinky_DIP": [18, 19, 20], # 小指 DIP 关节
    }

    if not detection_result.hand_landmarks:
        return flexion_results

    for idx, hand_landmarks in enumerate(detection_result.hand_landmarks):
        handedness = detection_result.handedness[idx][0].category_name
        hand_angles = {"Handedness": handedness}
        
        # 将所有关键点转换为 NumPy 数组，方便索引和计算
        landmarks_np = np.array([
            # [lm.x, lm.y, lm.z] for lm in hand_landmarks
            [lm.x, lm.y] for lm in hand_landmarks
        ])
        
        for joint_name, indices in FINGER_JOINTS_MAPPING.items():
            # 1. 提取三个关键点坐标
            p1_coord = landmarks_np[indices[0]] # 关节的前一个点
            p2_coord = landmarks_np[indices[1]] # 关节的顶点 (测量角度的点)
            p3_coord = landmarks_np[indices[2]] # 关节的后一个点
            
            # 2. 计算弯曲角度 (以 p2 为顶点)
            angle = calculate_angle(p1_coord, p2_coord, p3_coord)
            
            # 3. 存储结果
            hand_angles[f"{joint_name}_Angle"] = round(angle, 2)
        
        flexion_results.append(hand_angles)
        
    return flexion_results
