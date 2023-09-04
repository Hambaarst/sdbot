import base64
import io
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import requests
from discord.ui import Button, View

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content=True
urlt2i = "http://127.0.0.1:7860/sdapi/v1/txt2img"
urli2i = "http://127.0.0.1:7860/sdapi/v1/img2img"

send_data = {
        "sampler_name": "DPM++ SDE Karras",
        "n_iter": 1,
        "steps": 35,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "sampler_index": "DPM++ SDE Karras",
        "send_images": True,
        "save_images": False
        }

i2idata = {
  "init_images": [],
  "resize_mode": 1,
  "denoising_strength": 0.53,
  "prompt": "",
  "sampler_name": "DPM++ SDE Karras",
  "batch_size": 4,
  "n_iter": 1,
  "steps": 35,
  "cfg_scale": 7,
  "width": 512,
  "height": 512,
  "negative_prompt": "",
  "sampler_index": "DPM++ SDE Karras",
  "include_init_images": False,
  "script_name": None,
  "send_images": True,
  "save_images": False,
  "alwayson_scripts": {}
}

upscaledata={
    "init_images": [],
    "resize_mode": 1,
    "denoising_strength": 0.4,
    "sampler_name": "DPM++ SDE Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 15,
    "cfg_scale": 7,
    "width": 1024,
    "height": 1024,
    "sampler_index": "DPM++ SDE Karras",
    "send_images": True
}

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

class MyView(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.blurple)
    async def button_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_message("you pressed button")

@bot.command(description="creates a button")
async def button(ctx: discord.Interaction):
    await ctx.response.send_message("this is a button", view=MyView())

@bot.command(description="draw something")
async def draw(ctx: discord.Interaction, prompt: str = "", negatives: str = "", amount: int = 1):
    await ctx.response.defer(invisible=False)
    if amount > 4:
        amount = 4
    send_data["prompt"] = prompt
    send_data["batch_size"] = amount
    send_data["negative_prompt"] = "BadDream " + negatives
    
    post_response = requests.post(urlt2i, json=send_data)
    post_response_json = post_response.json()
    files: list[discord.File] = []
    i: int = 1
    view = View()
    for image in post_response_json["images"]:
        img = base64.b64decode(image)
        files.append(discord.File(io.BytesIO(img),filename=f"img{i}.png"))
        button = ImageButton(image=image, send_data=send_data, row=0, label=f"redo {i}", style=discord.ButtonStyle.gray)
        button2= UpscaleButton(image=image, row=1, label=f"upscale {i}", style=discord.ButtonStyle.gray)
        view.add_item(button)
        view.add_item(button2)
        i = i + 1

    await ctx.followup.send(files=files, view=view, ephemeral=True)

async def img2img(image, send_data):
    # await ctx.response.defer(invisible=False)

    # image_data = base64.b64encode(image).decode("utf-8")
    i2idata["init_images"]=['data:image/png;base64,' + image]
    i2idata["prompt"] = send_data["prompt"]
    i2idata["negative_prompt"] = send_data["negative_prompt"]
    post_response = requests.post(urli2i, json=i2idata)
    post_response_json = post_response.json()
    i: int = 1
    files:list[discord.File] = []
    view = View()
    for item in post_response_json["images"]:
        img = base64.b64decode(item)
        files.append(discord.File(io.BytesIO(img),filename=f"img{i}.png"))
        button = ImageButton(image=item, send_data=send_data, row=0, label=f"{i}", style=discord.ButtonStyle.gray)
        button2= UpscaleButton(image=item, row=1, label=f"upscale {i}", style=discord.ButtonStyle.gray)
        view.add_item(button)
        view.add_item(button2)
        i = i + 1
    return (files, view)

#function that takes image and uses img2img api to upscale said image
async def upscale(image):
    # await ctx.response.defer(invisible=False)
    # image_data = base64.b64encode(image).decode("utf-8")
    upscaledata["init_images"]=['data:image/png;base64,' + image]
    post_response = requests.post(urli2i, json=upscaledata)
    post_response_json = post_response.json()
    files:list[discord.File] = []
    view = View()
    for item in post_response_json["images"]:
        img = base64.b64decode(item)
        files.append(discord.File(io.BytesIO(img),filename=f"upscaled_img.png"))
    return (files, view)

#button class that takes image and upscales said image
class UpscaleButton(discord.ui.Button):
    def __init__(self, image, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs
        )
        self.image = image
        
    #button function when pressed takes the image and sends it to upscale and disables all buttons
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=False)
        response = await upscale(self.image)
        await interaction.followup.send(files=response[0], view=response[1], ephemeral=True)

#button class that takes image and send_data and creates variations of images and buttons to create more variations
class ImageButton(discord.ui.Button):
    def __init__(self, image, send_data, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs
        )
        self.image = image
        self.send_data = send_data

    #button function when pressed takes the image and sends it to img2img and disables all buttons
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(invisible=False)
        response = await img2img(self.image, self.send_data)
        await interaction.followup.send(files=response[0], view=response[1], ephemeral=True)

class MyView(discord.ui.View):
    @discord.ui.button(style=discord.ButtonStyle.grey)
    async def button_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_message("you pressed button")


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if "poggers" == msg.content.lower():
        await msg.channel.send("pepega even")

bot.run(TOKEN)