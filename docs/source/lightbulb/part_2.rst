Part 2 - Lightbulb Bot
======================

Lightbulb is a command handler for Hikari, making it easy to create commands.

So to start using Lightbulb, let's change our ``bot.py`` a little (new code has been highlighted): 

.. code-block:: python
    :linenos:
    :emphasize-lines: 6, 10-15, 18-22

    import asyncio
    import os

    import dotenv
    import hikari
    import lightbulb

    dotenv.load_dotenv()

    bot = lightbulb.BotApp(
        os.environ["BOT_TOKEN"],
        intents=hikari.Intents.ALL,
        prefix="+",
        banner=None,
    )


    @bot.command
    @lightbulb.command("ping", description="The bot's ping")
    @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
    async def ping(ctx: lightbulb.Context) -> None:
        await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")


    if __name__ == "__main__":
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        bot.run()


- **Line 6** - We've imported lightbulb now too
- **Line 10-15** - We've used lightbulb to create the bot, adding
    - a ``prefix`` kwarg set to ``"+"``, for text-based commands
    - | a ``banner`` kwarg set to ``None``, disabling the hikari banner that appears when the bot starts
      | This isn't necessary, but the banner can get a little annoying after a while (sorry dav >_>)
- **Line 18-22** - Creates a command with the lightbulb bot named ``ping`` which works the same as the old ``ping`` command, responding with ``Pong!`` and the bot's heartbeat latency

Now let's run the bot again!

You should see a slightly different output this time:

.. code-block::

    I 2022-08-13 16:40:23,476 hikari.bot: you can start 998 sessions before the next window which starts at 2022-08-13 17:23:11.910600+01:00; planning to start 1 session...
    I 2022-08-13 16:40:24,051 hikari.gateway.0: shard is ready: 1 guilds, Hikari#1093 (1007678609466601492), session '9c0a984004cdf4ed7d52ee1343f44121' on v8 gateway
    I 2022-08-13 16:40:24,368 lightbulb.internal: Processing guild application commands
    I 2022-08-13 16:40:24,973 lightbulb.internal: Processing application commands for guild 765236394577756171
    I 2022-08-13 16:40:25,250 lightbulb.internal: Processing global application commands
    I 2022-08-13 16:40:25,517 lightbulb.internal: Application command processing completed
    I 2022-08-13 16:40:25,520 hikari.bot: started successfully in approx 2.35 seconds

Again, if you run the command ``+ping`` in your server, the bot should respond with it's heartbeat latency.

Now, try typing ``/ping`` in Discord. A command should appear, with your bot's avatar next to it:

.. image:: ../_static/ping_cmd.png

Hit enter, and let's run this new command!

.. image:: ../_static/ping_2.png

We've just made a slash command! By passing ``lightbulb.SlashCommand`` to the ``@lightbulb.implements`` decorator, lightbulb
will turn the command into a slash command, as well as a text-based prefix command (``lightbulb.PrefixCommand``).

.. note::

    If you wanted to make your commands slash-only, you can remove the prefix kwarg on line 14 and
    ``lightbulb.PrefixCommand`` from the implements decorator.

Command Options
---------------

| Commands, both prefix and slash, can have options. Discord supports quite a few
 `options types <https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type>`_
 for slash commands.
| `Read the docs - Command Option Types <https://hikari-lightbulb.readthedocs.io/en/latest/guides/commands.html#converters-and-slash-command-option-types>`_

Let's make a new command using some of these option types to demonstrate them!

After your ``ping`` command, add this:

.. code-block:: python
    :linenos:

    @bot.command
    @lightbulb.option("ping", "Role to ping with announcement.", type=hikari.Role)
    @lightbulb.option(
        "channel", "Channel to post announcement to.", type=hikari.TextableChannel
    )
    @lightbulb.option("image", "Announcement attachment.", type=hikari.Attachment)
    @lightbulb.option("message", "The message to announce.", type=str)
    @lightbulb.command("announce", "Make an announcement!", pass_options=True)
    @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
    async def announce(
        ctx: lightbulb.Context,
        message: str,
        image: hikari.Attachment,
        channel: hikari.InteractionChannel,
        ping: hikari.Role,
    ) -> None:
        embed = hikari.Embed(
            title="Announcement!",
            description=message,
        )
        embed.set_image(image)

        await ctx.bot.rest.create_message(
            content=ping.mention,
            channel=channel.id,
            embed=embed,
            role_mentions=True,
        )

        await ctx.respond(
            f"Announcement posted to <#{channel.id}>!", flags=hikari.MessageFlag.EPHEMERAL
        )

- **Line 2-8** - Specifying the options for our command
    - You can see that we've specified a type for each option, such as ``hikari.Role``, ``hikari.TextableChannel`` and ``hikari.Attachment``
    - Using built-in Python types such as ``str`` and ``int`` is also valid (**Line 7**)    
- **Line 12-15** - We've passed our options as parameters to the command's function
    - **NOTE:** The parameters must be named exactly as the options
    - | You **cannot**, for example, call your ``message`` parameter ``msg``
      | Lightbulb will error if you do so
- | **Line 17-21** - Create an embed, setting its description to the message our author gave, and the image to the image they chose too
  | We'll go into more detail on creating embeds in the next part (:ref:`section_3`)
- **Line 23-28** - Send the message to the give channel, pinging the role given in the command options
    - **NOTE:** To ping everyone with the role, you must have set ``role_mentions`` to ``True``, and the bot must have the ``Mention All Roles`` permission in the guild
- **Line 30-32** - Respond to the interaction with an ``ephemeral`` message, stating where the announcement has been posted

.. image:: ../_static/announcement_1.png
.. image:: ../_static/announcement_2.png
.. image:: ../_static/announcement_3.png
.. image:: ../_static/announcement_4.png

`Read the docs - Commands <https://hikari-lightbulb.readthedocs.io/en/latest/guides/commands.html>`_