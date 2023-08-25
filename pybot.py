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

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(description="sends a test arg to the bot")
async def send(ctx, arg1):
    print(arg1)

class MyView(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.blurple)
    async def button_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_message("you pressed button")

@bot.slash_command(description="creates a button")
async def button(ctx: discord.Interaction):
    await ctx.response.send_message("this is a button", view=MyView())

@bot.slash_command(description="draw something")
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
        button = Button(label=f"image {i}", style=discord.ButtonStyle.blurple)
        view.add_item(button)
        i = i + 1

    await ctx.followup.send(files=files, view=view)

async def img2img(ctx: discord.Interaction, image, send_data):
    await ctx.response.defer(invisible=False)



@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if "poggers" == msg.content.lower():
        await msg.channel.send("pepega even")

bot.run(TOKEN)