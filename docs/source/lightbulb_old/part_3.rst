.. _section_3:

Part 3 - Making a lightbulb extension
=====================================

Extensions are a useful way of separating parts of your bot into different files, making it easier to manage.

So, let's create an extension!

In your ``my_bot`` folder make a new folder named ``extensions``.

Then in that folder create a file named ``info.py``.

Your file structure should look like this now:

.. code-block::

    my_bot
    │ bot.py
    │ requirements.txt
    │ .env
    │
    └── extensions
    │ │ info.py

In ``info.py`` paste the following:

.. code-block:: python
    :linenos:

    from datetime import datetime
    from typing import Optional

    import hikari
    import lightbulb

    info_plugin = lightbulb.Plugin("Info")


    @info_plugin.command
    @lightbulb.option(
        "user", "The user to get information about.", hikari.User, required=False
    )
    @lightbulb.command("userinfo", "Get info on a server member.", pass_options=True)
    @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
    async def userinfo(ctx: lightbulb.Context, user: Optional[hikari.User] = None) -> None:
        if not (guild := ctx.get_guild()):
            await ctx.respond("This command may only be used in servers.")
            return

        user = user or ctx.author
        user = ctx.bot.cache.get_member(guild, user)

        if not user:
            await ctx.respond("That user is not in the server.")
            return

        created_at = int(user.created_at.timestamp())
        joined_at = int(user.joined_at.timestamp())

        roles = (await user.fetch_roles())[1:]  # All but @everyone
        roles = sorted(
            roles, key=lambda role: role.position, reverse=True
        )  # sort them by position, then reverse the order to go from top role down

        embed = (
            hikari.Embed(
                title=f"User Info - {user.display_name}",
                description=f"ID: `{user.id}`",
                colour=0x3B9DFF,
                timestamp=datetime.now().astimezone(),
            )
            .set_footer(
                text=f"Requested by {ctx.author.username}",
                icon=ctx.author.display_avatar_url,
            )
            .set_thumbnail(user.avatar_url)
            .add_field(
                "Bot?",
                "Yes" if user.is_bot else "No",
                inline=True,
            )
            .add_field(
                "Created account on",
                f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
                inline=True,
            )
            .add_field(
                "Joined server on",
                f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
                inline=True,
            )
            .add_field(
                "Roles",
                ", ".join(r.mention for r in roles),
                inline=False,
            )
        )

        await ctx.respond(embed)


    def load(bot: lightbulb.BotApp) -> None:
        bot.add_plugin(info_plugin)


And in ``bot.py`` we'll need to make a little change. On line 17, add:

.. code-block:: python

    bot.load_extensions_from("./extensions/")

So, now let's run the bot with our new ``userinfo`` command!

You should see a new line in your output:

.. code-block::

    I 2022-08-13 17:22:03,151 lightbulb.app: Extension loaded 'extensions.info'

Now let's go and try out the command:

.. image:: ../_static/userinfo_1.png

.. image:: ../_static/userinfo_2.png

Now to go through what everything does...

- | **Line 7** - Create a plugin named ``Info``, which will be used to add our new command
  | `Read the docs - Creating plugins <https://hikari-lightbulb.readthedocs.io/en/latest/guides/plugins.html>`_
- **Line 10** - Decorator to attach the following command to the plugin
- | **Line 11-13** - Add a command option named "``user``" with a type of ``hikari.User`` that is **not required**
                     and a description of "``The user to get information about.``"
  | `Read the docs - Converters and Slash Command Options Types <https://hikari-lightbulb.readthedocs.io/en/latest/guides/commands.html#converters-and-slash-command-option-types>`_
- **Line 14** - Decorator to create the command, setting the name to "``userinfo``" and the description to "``Get info on a server member.``"
- **Line 15** - Converts the decorated function into a prefix command and slash command
- | **Line 16** - The command's function, which takes the parameters ``ctx`` and ``user``
  | `Read the docs - lightbulb.Context <https://hikari-lightbulb.readthedocs.io/en/latest/api_references/context.html>`_
  | `Read the docs - hikari.User <https://www.hikari-py.dev/hikari/users.html#hikari.users.User>`_
- | **Line 17** - Get the guild (``ctx.get_guild()``)
  | `Read the docs - Python Walrus Operator (:=) <https://realpython.com/python-walrus-operator/>`_
- | **Line 21-22** - If a user was not passed as an option (``user`` will be ``None``), we assign ``ctx.author`` to ``user``
  | Then, get the member of the guild
  | **Note:** This will return ``None`` if the target is not found in the guild
- | **Line 28-29** - Get the `UNIX Timestamps <https://www.unixtimestamp.com/>`_ for when the member created their account and joined the guild
  | **Note:** The rounding with ``int()`` is necessary, as Discord timestamps only work with integers, not floats
- **Line 31-34** - Get the member's list of roles, excluding ``@everyone``, then sort them from highest role to lowest
- **Line 37-42** - Make a Discord `embed <https://www.hikari-py.dev/hikari/embeds.html#hikari.embeds.Embed>`_ setting the title, description, colour and timestamp
- **Line 43-47** - Set the embed's `footer <https://www.hikari-py.dev/hikari/embeds.html#hikari.embeds.Embed.set_footer>`_ and `thumbnail <https://www.hikari-py.dev/hikari/embeds.html#hikari.embeds.Embed.set_footer>`_
- **Line 48-67** - Add `fields <https://www.hikari-py.dev/hikari/embeds.html#hikari.embeds.Embed.add_field>`_ to the embed, stating
    - whether the user is a bot or not
    - when their account was created & when they joined the server, using `Discord Timestamps <https://discord.com/developers/docs/reference#message-formatting-timestamp-styles>`_
    - a list of roles the member has
- **Line 70** - respond to the interaction with the embed (`Read the docs - Context.respond <https://hikari-lightbulb.readthedocs.io/en/latest/api_references/context.html#lightbulb.context.base.ApplicationContext.respond>`_)
- | **Line 73-74** - the load function, to load the extension when the bot starts
  | **Note:** This is required in each extension

`Read the docs - Extensions <https://hikari-lightbulb.readthedocs.io/en/latest/guides/extensions.html>`_