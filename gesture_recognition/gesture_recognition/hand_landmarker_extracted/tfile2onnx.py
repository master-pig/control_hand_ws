import tflite2onnx

tflite_path = './hand_detector.tflite'
onnx_path = './hand_detector.onnx'

tflite2onnx.convert(tflite_path, onnx_path)