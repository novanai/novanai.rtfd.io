Part 8 - Command Checks
=======================

For this section, we'll be making a ``purge`` command, which will delete messages in bulk.
You don't want *anyone* to be able to use this command, only those who can delete messages themselves,
so we're gonna need to add some command checks to ensure that!

So, create a new file named ``mod.py`` in the extensions folder.

In it paste the following:

.. code-block:: python
    :linenos:

    import hikari
    import lightbulb

    mod_plugin = lightbulb.Plugin("Mod")


    @mod_plugin.command
    @lightbulb.option(
        "messages", "The number of messages to purge.", type=int, required=True
    )
    @lightbulb.command("purge", "Purge messages.", aliases=["clear"])
    @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
    async def purge_messages(ctx: lightbulb.Context) -> None:
        num_msgs = ctx.options.messages
        channel = ctx.channel_id

        # If the command was invoked using the PrefixCommand, it will create a message
        # before we purge the messages, so we want to delete this message first
        if isinstance(ctx, lightbulb.PrefixContext):
            await ctx.event.message.delete()

        msgs = await ctx.bot.rest.fetch_messages(channel).limit(num_msgs)
        await ctx.bot.rest.delete_messages(channel, msgs)

        await ctx.respond(f"{len(msgs)} messages deleted.", delete_after=5)


    def load(bot: lightbulb.BotApp) -> None:
        bot.add_plugin(mod_plugin)

- **Line 14** - If we don't use ``pass_options=True`` in the command decorator (like with the ``userinfo`` command), we can't pass the options to the function, but their values can still be accessed from ``ctx.options``
- | **Line 22** - Fetch the most recent messages in the channel, limiting it to ``num_msgs``
  | `Read the docs - fetch_messages <https://www.hikari-py.dev/hikari/api/rest.html#hikari.api.rest.RESTClient.fetch_messages>`_
  | `Read the docs - LazyIterator.limit() <https://www.hikari-py.dev/hikari/iterators.html#hikari.iterators.LazyIterator.limit>`_
- **Line 23** - Delete the messages that we fetched

Now this command works fine, but now *everyone* can delete messages using the bot.
We only want people with the ``Manage Messages`` permission to do this, so this is where
`checks <https://hikari-lightbulb.readthedocs.io/en/latest/guides/commands.html#adding-checks-to-commands>`_ come in.

Just below **line 7** (``@mod_plugin.command``), add the following:

.. code-block:: python

    @lightbulb.add_checks(
        lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
        lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    )

This checks if the both the **user** who ran the command and the **bot** has the ``manage messages`` permission in the guild.

If the both the user and bot have permission to run the command, it will work. If they don't, the command will raise
`CheckFailure <https://hikari-lightbulb.readthedocs.io/en/latest/api_references/errors.html#lightbulb.errors.CheckFailure>`_.

But raising an error and the command failing isn't that useful, we want to tell the user what happened.

So, onto error handling!