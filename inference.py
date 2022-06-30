import torch
import image_classification.resnet as models
from PIL import Image
from torchvision import transforms
import numpy as np
import onnx
import onnxruntime as rt
from torch.autograd import Variable

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


model = models.build_resnet("resnet34", "fanin", 2, verbose=False)
model.load_state_dict(torch.load("face_score.onnx"),False)
model.eval()

img = Image.open("test1.jpg")
transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
        ])
input_tensor = transform(img).unsqueeze(0)
for
#input_tensor = Variable(torch.ones(1, 3, 224, 224))
torch_onnx_out = torch.onnx.export(model, input_tensor, "model_res34.onnx",
                    verbose=True,
                    input_names=['input'],
                    output_names=['output'],
                    opset_version=11)
print(input_tensor)
torch_out = model(input_tensor)
print("torch output: ")
print(to_numpy(torch_out))

#create runtime session
sess = rt.InferenceSession("model_res34.onnx")
# get output name
input_name = sess.get_inputs()[0].name
output_name= sess.get_outputs()[0].name
#forward model
res = sess.run([output_name], {input_name: to_numpy(input_tensor)})
out = np.array(res)
print("onnx ouptut: ")
print(out[0])
