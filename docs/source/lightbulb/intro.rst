Introduction
============

| I hightly recommand an **intermediate level** of Python knowledge before you begin this guide.
| If you don't know Python well, Carberra Tutorials is a good place to get started: https://www.youtube.com/playlist?list=PLYeOw6sTSy6bHRFwzIA3VAy05J2tJAAoS

Throughout this guide you will see links like "`Read the docs <#>`_" which go to the
`Hikari docs <https://www.hikari-py.dev/hikari/>`_, `Lightbulb docs <https://hikari-lightbulb.readthedocs.io/en/latest/>`_
or other documentation.
I try to put them in useful places where people might need them to modify their code to suit a different purpose.

| The GitHub Repository for this guide is located `here <https://github.com/novanai/hikari-lightbulb-guide>`_
| This should really only be used as an assist to the guide, and *not to just copy and paste*. :<

This guide was last updated on ``17 August 2022``.

What does this guide cover?
---------------------------

- Commands & command options (text-based prefix & slash)
- Lightbulb extensions & plugins
- Message components (specifically select menus)
- Command checks & cooldowns 
- Basic error handling

.. _bot_application:

Making your Discord Bot Application
===================================

`Carberra Tutorials <https://www.youtube.com/channel/UC13cYu7lec-oOcqQf5L-brg>`_ made a video on
`Creating a bot on the Developer Portal <https://www.youtube.com/watch?v=jSGPNChqGAY?t=76>`_ which you can follow to do this:

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/jSGPNChqGAY?start=76"
        title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write;
        encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
    </iframe>

Setting up the files
====================

Make a folder for your bot:

.. code-block:: bash

    mkdir my_bot
    cd my_bot

Then, make 3 files:

* ``bot.py``
* ``requirements.txt``
* ``.env``

After all that, your file structure should look like this:

.. code-block:: 

    my_bot
    │ bot.py
    │ requirements.txt
    │ .env


Make a virtual environment
==========================
This is optional, but recommended.

Windows:

.. code-block:: bash

    python -m venv .venv
    .\.venv\Scripts\activate

Linux:

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate

You'll need to activate this venv when running your bot.

Read more about virtual environments here: https://docs.python.org/3/tutorial/venv.html.

Installing requirements
=======================

In ``requirements.txt`` paste the following

.. code-block::

    hikari[speedups]>=2.0.0.dev111
    hikari-lightbulb>=2.2.4
    hikari-miru>=1.1.2
    python-dotenv>=0.21.0

And then run

.. code-block:: bash

    python -m pip install -r requirements.txt

What have we just installed?
----------------------------

- `Hikari <https://www.hikari-py.dev/hikari/>`_ - a "sane Python framework for writing modern Discord bots"
- `Lightbulb <https://hikari-lightbulb.readthedocs.io/en/latest>`_ - a "simple and easy to use command framework for Hikari"
- `Miru <https://hikari-miru.readthedocs.io/en/latest/index.html>`_ - an "optional component handler for Hikari"

So now, let's begin!