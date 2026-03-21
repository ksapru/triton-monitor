import numpy as np
import triton_python_backend_utils as pb_utils
import torch

class TritonPythonModel:
    def initialize(self, args):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Running on: {self.device}")

    def execute(self, requests):
        responses = []
        for request in requests:
            input_tensor = pb_utils.get_input_tensor_by_name(request, "INPUT0")
            x = input_tensor.as_numpy()
            x_gpu = torch.tensor(x).to(self.device)
            y_gpu = x_gpu * 2
            y = y_gpu.cpu().numpy()
            out = pb_utils.Tensor("OUTPUT0", y.astype(np.float32))
            responses.append(pb_utils.InferenceResponse(output_tensors=[out]))
        return responses

    def finalize(self):
        pass
