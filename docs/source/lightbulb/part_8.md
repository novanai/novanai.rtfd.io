# Part 8 - Command Checks

For this section, we'll be making a `purge` command, which will delete messages in bulk.

You don't want just *anyone* to be able to use this command, only those who can delete messages themselves, so we're gonna need to add some command checks to ensure that!

So, create a new file named `mod.py` in the extensions folder.

In it paste the following:

```{code-block} python
:linenos: true

import datetime

import hikari
import lightbulb

mod_plugin = lightbulb.Plugin("Mod")


@mod_plugin.command
@lightbulb.option(
    "sent_by",
    "Only purge messages sent by this user.",
    type=hikari.User,
    required=False,
)
@lightbulb.option(
    "messages",
    "The number of messages to purge.",
    type=int,
    required=True,
    min_value=2,
    max_value=200,
)
@lightbulb.command("purge", "Purge messages.")
@lightbulb.implements(lightbulb.SlashCommand)
async def purge_messages(ctx: lightbulb.SlashContext) -> None:
    num_msgs = ctx.options.messages
    sent_by = ctx.options.sent_by
    channel = ctx.channel_id

    bulk_delete_limit = datetime.datetime.now(
        datetime.timezone.utc
    ) - datetime.timedelta(days=14)
    iterator = (
        ctx.bot.rest.fetch_messages(channel)
        .take_while(lambda msg: msg.created_at > bulk_delete_limit)
        .limit(num_msgs)
    )
    if sent_by:
        iterator = iterator.filter(lambda msg: msg.author.id == sent_by.id)

    count = 0

    async for messages in iterator.chunk(100):
        count += len(messages)
        await ctx.bot.rest.delete_messages(channel, messages)

    await ctx.respond(f"{count} messages deleted.", delete_after=5)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mod_plugin)
```

- **Line 10-23** - Set up the command options
    - For the `messages` option, we've set limits.  
    When bulk deleting messages, Discord says you must have a minimum value of `2` messages. And because we don't want our bot to get rate limited while deleting huge amounts of messages, we also set our own maximum value of `200`.
- **Line 27-28** - If we don't use `pass_options=True` in the command decorator (like with the `userinfo` command), we can't pass the options as function parameters, but their values can still be accessed via `ctx.options`
- **Line 31-33** - Bots can't bulk delete messages older than 2 weeks, so we set a limit to only fetch messages younger than 2 weeks
- **Line 34-38** - Create an iterator which fetches the most recent messages in the channel, taking only the ones younger than 2 weeks and limiting it to `num_msgs`  
    [Read the docs - fetch_messages](https://www.hikari-py.dev/hikari/api/rest.html#hikari.api.rest.RESTClient.fetch_messages)  
    Add `.take_while()` docs
    [Read the docs - LazyIterator.limit()](https://www.hikari-py.dev/hikari/iterators.html#hikari.iterators.LazyIterator.limit)
- **Line 39-40** - If a sent_by user was provided, then filter the iterator to only hold messages sent by that user
- **Line 44-46** - Delete the messages in the iterator, in chunks of 100
    - A maximum of 100 messages can be passed per bulk delete request, so we chunk them into groups of 100 and make multiple requests

This command works fine, but now *everyone* can delete messages using the bot. We only want people with the `Manage Messages` permission to do this, so this is where [checks](https://hikari-lightbulb.readthedocs.io/en/latest/guides/commands.html#adding-checks-to-commands) come in.

Just below **line 9** (`@mod_plugin.command`), add the following:

```{code-block} python
@lightbulb.app_command_permissions(hikari.Permissions.MANAGE_MESSAGES, dm_enabled=False)
@lightbulb.add_checks(
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
)
```
- **Line 1** - Using Discord's app command permissions, we set default permissions of `MANAGE_MESSAGES` for the user, and we disable the command in DMs
- **Line 2-4** - Check the bot also has permission to delete messages in the guild.

If the both the user and bot have permission to run the command, it will work. However if the bot doesn't have the `MANAGE_MESSAGES` permission, the command will raise [CheckFailure](https://hikari-lightbulb.readthedocs.io/en/latest/api_references/errors.html#lightbulb.errors.CheckFailure).

But raising an error and the command failing isn't that useful, we want to tell the user what happened.

So, onto error handling!
