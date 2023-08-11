import os
import io
import base64
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content=True

urlt2i = "http://127.0.0.1:7860/sdapi/v1/txt2img"

message = "Hello, {ctx.author.mention}!"

bot = commands.Bot(command_prefix='¤', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def hello(ctx):
    await ctx.send(message)

@bot.command()
async def test(ctx, *args):
    print(args)
    print(args[1])

send_data = {
        "enable_hr": False,
        "denoising_strength": 0,
        "firstphase_width": 0,
        "firstphase_height": 0,
        "hr_scale": 2,
        "hr_upscaler": None,
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_sampler_name": None,
        "hr_prompt": None,
        "hr_negative_prompt": None,
        "styles": [""],
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "UniPC",
        "n_iter": 1,
        "steps": 35,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "restore_faces": True,
        "tiling": False,
        "do_not_save_samples": False,
        "do_not_save_grid": False,
        "eta": 0,
        "s_min_uncond": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {},
        "override_settings_restore_afterwards": True,
        "script_args": [],
        "sampler_index": "UniPC",
        "script_name": None,
        "send_images": True,
        "save_images": False,
        "alwayson_scripts": {}
        }

@bot.command()
async def draw(ctx, *args):
    if len(args) >= 2:
        negative = args[1]
    else:
        negative = ""

    send_data["batch_size"] = 1
    send_data["negative_prompt"] = "BadDream FastNegativeV2 " + negative

    post_response = requests.post(urlt2i, json=send_data)
    post_response_json = post_response.json()
    files: list[discord.File] = []
    for image in post_response_json["images"]:
        img = base64.b64decode(image)
        files.append(discord.File(io.BytesIO(img),filename="img.png"))
    await ctx.send(files=files)

@bot.command()
async def draw4(ctx, *args):
    if len(args) >= 2:
        negative = args[1]
    else:
        negative = ""

    send_data["batch_size"] = 4
    send_data["negative_prompt"] = "BadDream FastNegativeV2 " + negative
    
    post_response = requests.post(urlt2i, json=send_data)
    post_response_json = post_response.json()
    files: list[discord.File] = []
    for image in post_response_json["images"]:
        img = base64.b64decode(image)
        files.append(discord.File(io.BytesIO(img),filename="img.png"))
    await ctx.send(files=files)

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if "poggers" == msg.content.lower():
        await msg.channel.send("pepega even")

    await bot.process_commands(msg)


bot.run(TOKEN)