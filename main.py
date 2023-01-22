

import replicate
from fastapi import FastAPI
import PIL.Image
import os
import openai
app = FastAPI()
model = replicate.models.get("pharmapsychotic/clip-interrogator")
version = model.versions.get("a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90")

openai.api_key = os.getenv("OPENAI_API_KEY")



@app.get("/get-prompt")
def getPrompt(link = None):
    print(os.getenv("OPENAI_API_KEY"))
    if link is None:
        text = 'No link'
        return text

    else:
        inputs = {
        # Input image
        'image': link,

        # Choose ViT-L for Stable Diffusion 1, and ViT-H for Stable Diffusion
        # 2
        'clip_model_name': "ViT-L-14/openai",

        # Prompt mode (best takes 10-20 seconds, fast takes 1-2 seconds).
        'mode': "fast",
        }
        output = version.predict(**inputs)
        output = output.replace('kanye west', '')
        print(output)
        response = openai.Image.create_edit(
            image=open("./resources/defautlers.png", 'rb'),
            mask=open("./resources/torso_masker.png", 'rb'),
            prompt="A man wearing " + output,
            n=2,
            size="1024x1024"
        )
        return response
