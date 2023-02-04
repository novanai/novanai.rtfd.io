# Introduction

I highly recommand an **intermediate level** of Python knowledge before you begin this guide. If you don't know Python well, Carberra Tutorials is a good place to get started: [https://www.youtube.com/playlist?list=PLYeOw6sTSy6bHRFwzIA3VAy05J2tJAAoS](https://www.youtube.com/playlist?list=PLYeOw6sTSy6bHRFwzIA3VAy05J2tJAAoS)

Throughout this guide you will see links like "[Read the docs](#introduction)" which go to the [Hikari docs](https://www.hikari-py.dev/hikari/), [Lightbulb docs](https://hikari-lightbulb.readthedocs.io/en/latest/) or other documentation. I try to put them in useful places where people might need them to modify their code to suit a different purpose.

The GitHub Repository for this guide is located [here](https://github.com/novanai/hikari-lightbulb-guide). This should really only be used as an assist to the guide, and *not to just copy and paste from*. :<

This guide was last updated on ``4 February 2023``.

## What does this guide cover?

* Slash commands & command options
* Lightbulb extensions & plugins
* Message components (specifically select menus)
* Command checks & cooldowns 
* Basic error handling (command-specific)

# Make your Discord Bot Application

[Carberra Tutorials](https://www.youtube.com/channel/UC13cYu7lec-oOcqQf5L-brg) made a video on [Creating a bot on the Developer Portal](https://www.youtube.com/watch?v=jSGPNChqGAY?t=76) which you can follow to do this:

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/jSGPNChqGAY?start=76"
    title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write;
    encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>

```{note}
Make sure to enable the ``Guild Members`` intent for your bot.
```

# Set up the files

Make a folder for your bot:

```bash
mkdir my_bot
cd my_bot
```

Then, make 3 files:

* `bot.py`
* `requirements.txt`
* `.env`

After all that, your file structure should look like this:

```
my_bot
├─ bot.py
├─ requirements.txt
├─ .env
```

# Make a virtual environment

This is optional, but recommended.

Windows:
```
python -m venv .venv
.\.venv\Scripts\activate
```

Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

You'll need to activate this venv when running your bot.

[Read the docs - Virtual Environments](https://docs.python.org/3/tutorial/venv.html).

# Install requirements

In `requirements.txt` paste the following:

```
hikari[speedups]==2.0.0.dev115
hikari-lightbulb==2.3.1
hikari-miru==2.0.4
python-dotenv==0.21.1
```
And then run

```bash
pip install -r requirements.txt
```

## What have we just installed?

* [Hikari](https://www.hikari-py.dev/hikari/) - a "Discord API wrapper for Python and asyncio built on good intentions"
* [Lightbulb](https://hikari-lightbulb.readthedocs.io/en/latest) - a "simple and easy to use command framework for Hikari"
* [Miru](https://hikari-miru.readthedocs.io/en/latest/index.html) - an "optional component handler for Hikari"

So now, let's begin!