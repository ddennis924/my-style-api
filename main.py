import replicate
from flask import Flask, request, jsonify
app = Flask(__name__)
import os
import openai
model = replicate.models.get("pharmapsychotic/clip-interrogator")
version = model.versions.get("a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90")

openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route('/getprompt/', methods=['GET'])
def getPrompt():
    link = request.args.get("link", None)
    response = {}
    if link is None:
        response["ERROR"] = "The name can't be numeric. Please send a string."
        return jsonify(response)

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
        response["DATA"] = openai.Image.create_edit(
            image=open("./resources/defautlers.png", 'rb'),
            mask=open("./resources/torso_masker.png", 'rb'),
            prompt="A man wearing " + output,
            n=2,
            size="1024x1024"
        )
        return jsonify(response)

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our style-me-api!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
