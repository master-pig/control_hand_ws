# STEP 1: 导入必要的模块 (确保您已经安装了 mediapipe 和 opencv-python)
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from gesture_recognition.visualization import draw_landmarks_on_image
from gesture_recognition.calculate import get_full_finger_flexion
import cv2
import time 

class Landmark():
    def __init__(self, model_asset_path = './gesture_recognition/hand_landmarker.task', num_hands = 1):
        base_options = python.BaseOptions(model_asset_path = model_asset_path,
                                        delegate = python.BaseOptions.Delegate.GPU)
        options = vision.HandLandmarkerOptions(base_options = base_options,
                                            num_hands = num_hands,
                                            running_mode=vision.RunningMode.IMAGE, # 保持 IMAGE 模式，但每次传入时间戳
                                            )
        self.detector = vision.HandLandmarker.create_from_options(options)

        self.pTime = time.time()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("错误：无法打开摄像头。请检查设备是否连接或被占用。")



    def detect(self, alpha):
        if self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                print("警告：无法读取摄像头帧，退出。")
        self.frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
        
        # 将 NumPy 数组帧转换为 MediaPipe Image 对象
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.frame_rgb)
        self.detection_result = self.detector.detect(mp_image)

        # self.finger_flexion = get_full_finger_flexion(self.detection_result)

        new_flexion = get_full_finger_flexion(self.detection_result)

        if not hasattr(self, "filtered_flexion"):
            self.filtered_flexion = new_flexion.copy()

        if len(self.filtered_flexion) != len(new_flexion):
            self.filtered_flexion = new_flexion.copy()
        else:
            # --- 指数滑动平均滤波 ---
            for i, hand_info in enumerate(new_flexion):
                for key, value in hand_info.items():
                            if isinstance(value, (int, float)):  # 只对数值型平滑
                                last_val = self.filtered_flexion[i].get(key, value)
                                self.filtered_flexion[i][key] = alpha * value + (1 - alpha) * last_val

        # 用平滑后的值替代原始结果
        self.finger_flexion = self.filtered_flexion
        

        self.cTime = time.time()
        self.fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime

    def destory(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def draw(self):
        self.annotated_image_rgb = draw_landmarks_on_image(self.frame_rgb, self.detection_result)
        # 转换回 BGR 格式以便 OpenCV 显示
        self.annotated_image_bgr = cv2.cvtColor(self.annotated_image_rgb, cv2.COLOR_RGB2BGR)
        cv2.putText(self.annotated_image_bgr, f"FPS: {int(self.fps)}", (10, 30), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # 显示图像
        cv2.imshow('MediaPipe Hand Landmarker', self.annotated_image_bgr)

        
