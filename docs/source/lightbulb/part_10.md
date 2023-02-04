# Part 10 - Command Cooldowns

Cooldowns are a useful way of making sure people don't spam commands, and also to keep a limit on the number of requests your bot has to make.

In `mod.py`, just below `@mod_plugin.command`, add the following:

```{code-block} python
@lightbulb.add_cooldown(5, 1, lightbulb.UserBucket)
```

This specific command cooldown allows the command to be used **once** every **5 seconds** per **user**.

You could also do:

```{code-block} python
@lightbulb.add_cooldown(10, 2, lightbulb.ChannelBucket)
```

if you wanted the command to only be used **twice** every **10 seconds** per **channel**.

If the command is on cooldown when it is run, lightbulb will raise a `CommandIsOnCooldown` error.

We can add this piece of code to our error handler to handle this new error:

```{code-block} python
:linenos:

elif isinstance(exception, lightbulb.CommandIsOnCooldown):
    await event.context.respond(
        f"This command is on cooldown! You can use it again in {int(exception.retry_after)} seconds."
    )
    return True
```

[Read the docs - CommandIsOnCooldown](https://hikari-lightbulb.readthedocs.io/en/latest/api_references/errors.html#lightbulb.errors.CommandIsOnCooldown)