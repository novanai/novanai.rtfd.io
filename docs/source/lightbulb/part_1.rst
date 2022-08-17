Part 1 - Hikari Bot
===================

First, grab your bot's token from the `Discord Developer Portal <https://discord.com/developers/applications>`_
(refer to :ref:`bot_application`) and put it in the ``.env`` file, like so:

.. code-block:: bash

    BOT_TOKEN=your_bot_token


Next, in ``bot.py`` paste the following:

.. code-block:: python
    :linenos:

    import asyncio
    import os

    import dotenv
    import hikari

    dotenv.load_dotenv()

    bot = hikari.GatewayBot(
        os.environ["BOT_TOKEN"],
        intents=hikari.Intents.ALL,
    )


    @bot.listen()
    async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
        if not event.is_human or not event.content:
            return

        if event.content.strip() == "+ping":
            await event.message.respond(
                f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms"
            )


    if __name__ == "__main__":
        if os.name == "nt":
            # we are running on a Windows machine, and we have to add this so
            # the code doesn't error :< (it most likely will error without this)
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        bot.run()

Now save ``bot.py`` and run it:

.. code-block:: bash

    python bot.py

You should see an output similar to this:

.. _Hikari Output:

.. code-block::

    oooo         o8o  oooo                            o8o       光 2.0.0.dev110 [47bf3fcb]
    `888         `"'  `888                            `"'       © 2021-present davfsa - MIT license
     888 .oo.   oooo   888  oooo   .oooo.   oooo d8b oooo       interpreter:   CPython 3.10.5
     888P"Y88b  `888   888 .8P'   `P  )88b  `888""8P `888       running on:    AMD64 Windows 10
     888   888   888   888888.     .oP"888   888      888       installed at:  C:\Users\Nova\Documents\my_bot\.venv\lib\site-packages\hikari
     888   888   888   888 `88b.  d8(  888   888      888       documentation: https://hikari-py.dev/hikari
    o888o o888o o888o o888o o888o `Y888""8o d888b    o888o      support:       https://discord.gg/Jx4cNGG

    I 2022-08-13 16:38:07,798 hikari.bot: you can start 999 sessions before the next window which starts at 2022-08-13 17:38:11.748231+00:00; planning to start 1 session...
    I 2022-08-13 16:38:08,282 hikari.gateway.0: shard is ready: 1 guilds, Hikari#1093 (1007678609466601492), session '1868778c46c81d612853915354a51f37' on v8 gateway
    I 2022-08-13 16:38:08,291 hikari.bot: started successfully in approx 0.79 seconds

Now go into the server you invited your bot to, and send ``+ping``.

The bot should respond with ``Pong!`` and it's heartbeat latency:

.. image:: ../_static/ping_1.png

**Congratulations, you've just run your first Hikari bot!**

Now let's go through what everything does

- **Line 1-5** - Import the ``asyncio``, ``os``, ``dotenv`` and ``hikari`` modules
- **Line 7** - Load the ``.env`` file
- | **Line 9-12** - Create a bot using that token, and all Discord `intents <https://discord.com/developers/docs/topics/gateway#gateway-intents>`_
  | `Read the docs - Intents <https://hikari-lightbulb.readthedocs.io/en/latest/hikari_basics/intents.html>`_
- **Line 15-23** - The bot listens for messages sent in guilds (servers)
    - If the message author is not a human or the message has no text content (though it may have attachments), it ignores it
    - Otherwise, it checks if the message content is ``+ping`` and if it is, the bot responds with ``Pong!`` and it's heartbeat latency
- **Line 26-32**
    - If we are on a Windows machine, we have to add line 30 to stop a possible asyncio error from occuring
    - And finally, run the bot!

This bot works, but to add more commands other than ``+ping`` would be a *huge* hassle, so this is where Lightbulb comes in...