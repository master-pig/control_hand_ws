import tensorflow as tf

# interpreter = tf.lite.Interpreter(model_path="/home/mkbk/hand_control_ws/control_hand_ws/gesture_recognition/gesture_recognition/hand_landmarker_extracted/hand_detector.tflite")
interpreter = tf.lite.Interpreter(model_path="/home/mkbk/hand_control_ws/control_hand_ws/gesture_recognition/gesture_recognition/hand_landmarker_extracted/hand_landmarks_detector.tflite")
interpreter.allocate_tensors()

print("=== Input ===")
for i in interpreter.get_input_details():
    print(i)

print("=== Output ===")
for o in interpreter.get_output_details():
    print(o)
