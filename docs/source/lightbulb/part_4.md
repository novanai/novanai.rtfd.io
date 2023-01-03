# Part 4 - BotApp.d - a built-in DataStore

This is a small bit preparation for the next section (Command Groups & Subcommands).

In our `bot.py` file, we'll need to add some "listeners".

Just above `import dotenv` add:

```{code-block} python
import aiohttp
```

Then, just after `bot.load_extensions_from("./extensions/")`, add:

```{code-block} python
:linenos: true

@bot.listen()
async def on_starting(_: hikari.StartingEvent) -> None:
    bot.d.client_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.d.client_session.close()
```

- This creates 2 event listeners, one for when the bot is starting, and one for when the bot is stopping
- When the bot is starting, it creates a new instance of `aiohttp.ClientSession` and stores it under `client_session` in the `bot.d` data store
- When the bot is stopping, it closes the client session

[Read the docs - aiohttp](https://docs.aiohttp.org/en/stable/)
