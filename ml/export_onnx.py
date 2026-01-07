import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

model = joblib.load("model.pkl")

initial = [("float_input", FloatTensorType([None, model.n_features_in_]))]
onnx = convert_sklearn(model, initial_types=initial)

with open("../backend/app/models/sample_model.onnx","wb") as f:
    f.write(onnx.SerializeToString())
