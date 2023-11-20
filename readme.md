# Basic bot
-----

A simple fun project to use in private discord server with friends

## requirements
-pycord https://pycord.dev/
-locally installed automatic1111 sd webui and its requirements https://github.com/AUTOMATIC1111/stable-diffusion-webui
-discord bot

You also need .env to add your own TOKEN or create another .py file and import it

## usage
/draw is the command
there's 3 extra parameters you can add to the command:
-prompt
-negatives
-amount (hardcoded max to 4)

There are some hard coded settings you may want to modify to your own preference:
-sampler
-steps
-batch sizes
-size of image
-upscale size
-noise for redo
-amount of redo images depending on your machine

The bot uses the model that you have currently loaded in to your webui