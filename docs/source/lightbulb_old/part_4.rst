Part 4 - BotApp.d - a built-in DataStore
========================================

This is a small bit preparation for the next section (Command Groups & Subcommands).

In our ``bot.py`` file, we'll need to add some "listeners".

Just above ``import dotenv`` add:

.. code-block:: python

    import aiohttp

Then, just after ``bot.load_extensions_from("./extensions/")``, add:

.. code-block:: python
    :linenos:

    @bot.listen()
    async def on_starting(event: hikari.StartingEvent) -> None:
        bot.d.aio_session = aiohttp.ClientSession()

    @bot.listen()
    async def on_stopping(event: hikari.StoppingEvent) -> None:
        await bot.d.aio_session.close()

- This creates 2 event listeners, one for when the bot is starting, and one for when the bot is stopping
- When the bot is starting, it creates a new ``aiohttp.ClientSession`` named ``aio_session`` and stores it in the ``bot.d`` data store
- When the bot is stopping, it closes the ``aio_session`` client session

`Read the docs - aiohttp <https://docs.aiohttp.org/en/stable/>`_