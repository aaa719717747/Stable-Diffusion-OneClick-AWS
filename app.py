from flask import Flask, request, send_file, render_template
from diffusers import (
    StableDiffusionPipeline,
    EulerDiscreteScheduler,
    StableDiffusionImg2ImgPipeline,
)
import torch
from PIL import Image
from io import BytesIO
import requests
from flask_cors import CORS

# from oss_moudle import OSSUploader

app = Flask(__name__, template_folder="frontend", static_folder="frontend")
CORS(app, support_credentials=True)

import chatgpt_module

m_gpt = chatgpt_module.ChatGPT()


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health_check():
    return "Healthy", 200


@app.get("/hello")
def hello():
    return "hi!", 200


@app.post("/history")
def fetch_story_history():
    return m_gpt.request_gpt_quesion("请总结我的冒险历程，要求有时间线，有故事节点，有结局。不超过150字"), 200

@app.post("/changedscript")
def changedscript():
    data = request.json
    return m_gpt.changedscript_gpt(data["prompt"]), 200


@app.post("/gpt")
def ask_to_gpt():
    data = request.json
    result = m_gpt.request_gpt_quesion(data["prompt"])
    return result, 200


@app.post("/txt2img")
def text_to_img():
    data = request.json
    model_id = "runwayml/stable-diffusion-v1-5"
    output = "output_txt2img.png"

    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, scheduler=scheduler, revision="fp16", torch_dtype=torch.float16
    )
    pipe = pipe.to("cuda")
    image = \
        pipe(data["prompt"], guidance_scale=7.5, num_inference_steps=15, height=data["height"],
             width=data["width"]).images[
            0]

    # image.save(output)
    # url = oss_moudle.upload_file()
    #
    return send_file(output), 200


@app.post("/img2img")
def img_to_img():
    data = request.json
    model_id = "runwayml/stable-diffusion-v1-5"
    output = "output_img2img.png"

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16
    )
    pipe = pipe.to("cuda")
    response = requests.get(data["url"])
    init_image = Image.open(BytesIO(response.content)).convert("RGB")
    init_image = init_image.resize((768, 512))
    images = pipe(
        prompt=data["prompt"], image=init_image, strength=0.75, guidance_scale=7.5
    ).images

    images[0].save(output)
    return send_file(output), 200


app.run(host='0.0.0.0', port=5000)