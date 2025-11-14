import torch
from model import MyModel  # 你的模型结构

model = MyModel()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

dummy = torch.randn(1, 3, 224, 224)  # 按你的模型改

torch.onnx.export(
    model,
    dummy,
    "model.onnx",
    opset_version=13,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}}
)
