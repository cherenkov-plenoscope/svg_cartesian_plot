from PIL import Image as pimg
import tempfile
import os
import base64

def image_to_png_base64(mat):
    assert len(mat.shape) == 3
    assert mat.shape[2] == 3
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "img.png")
        img = pimg.fromarray(mat)
        img.save(path, "PNG")
        with open(path, "rb") as f:
            img_bytes = f.read()
        img_base64 = base64.encodebytes(img_bytes)
    return str(img_base64, "ascii")
