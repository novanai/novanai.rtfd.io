Part 5 - Command Groups & Subcommands
=====================================

Create a new file named ``fun.py`` in the extensions folder - this will contain our bot's second extension.

In ``fun.py`` paste the following:

.. code-block:: python
    :linenos:

    import hikari
    import lightbulb

    fun_plugin = lightbulb.Plugin("Fun")


    @fun_plugin.command
    @lightbulb.command("fun", "All the entertainment commands you'll ever need!")
    @lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
    async def fun_group(ctx: lightbulb.Context) -> None:
        pass  # as slash commands cannot have their top-level command ran, we simply pass here


    @fun_group.child
    @lightbulb.command("meme", "Get a meme!")
    @lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
    async def meme_subcommand(ctx: lightbulb.Context) -> None:
        async with ctx.bot.d.aio_session.get(
            "https://meme-api.herokuapp.com/gimme"
        ) as response:
            res = await response.json()
            if response.ok and res["nsfw"] != True:
                link = res["postLink"]
                title = res["title"]
                img_url = res["url"]

                embed = hikari.Embed(colour=0x3B9DFF)
                embed.set_author(name=title, url=link)
                embed.set_image(img_url)

                await ctx.respond(embed)

            else:
                await ctx.respond(
                    "Could not fetch a meme :c", flags=hikari.MessageFlag.EPHEMERAL
                )


    def load(bot: lightbulb.BotApp) -> None:
        bot.add_plugin(fun_plugin)

- **Line 4** - Create a new plugin named ``Fun``
- **Line 7** - Decorator to attach the following command to the plugin
- **Line 8** - Decorator to create the command, setting the name to "``fun``" and adding a description
- **Line 9** - Converts the decorated function to a PrefixCommandGroup and SlashCommandGroup
- **Line 10** - The command's function
- **Line 11** - pass the function, as slash commands cannot have their top-level command ran
- **Line 14** - attach the decorated function to the ``fun_group`` command
- **Line 15** - Decorator to create the subcommand, setting the name to ``meme`` and adding a description
- **Line 16** - Converts the decorated function to a ``PrefixSubCommand`` and ``SlashSubCommand``
- **Line 17** - The subcommand's function
- | **Line 18-21** - Using the ``aio_session`` from the ``bot.d`` data store that we created in the previous section, get a meme from the API
  | `Read the docs - aiohttp.ClientSession <https://docs.aiohttp.org/en/stable/#client-example>`_
- **Line 22** - If the response is successful and the meme is not NSFW (Not Safe For Work), then
    - **Line 23-25** - Get the meme's link, title and image url
    - **Line 27** - Create an embed
    - **Line 28** - Set the embed's author to the meme's title and link
    - **Line 29** - Set the embed's image to the meme's image url
    - **Line 31** - Respond to the interaction with the embed
- **Line 33** - Otherwise, if the response was not successful or the meme was NSFW, then
    - **Line 34-36** - Respond to the interaction with an ephemeral message, stating that we could not fetch a meme

Now, let's test it!

.. image:: ../_static/meme_1.png

.. image:: ../_static/meme_2.png

and if we can't fetch a meme:

.. image:: ../_static/meme_3.png

.. note::

    Ephemeral response only work with application commands, not prefix commands