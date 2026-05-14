from sentence_transformers import SentenceTransformer

_model = None
_device = None


def get_device():
    global _device

    # if _device == None:
    #     try:
    #         import torch_directml
    #         _device = torch_directml.device()
    #         return _device
    #     except ImportError:
    #         pass
    # else:
    #     _device = "cpu"

    _device = "cpu"


    return _device

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2", device=get_device())
    return _model
