Part 9 - Error Handling
=======================

We're going to add a command-specific error handler to make sure that if the command fails due to insufficient permissions,
we can send a little error message to whoever ran the command.

In ``mod.py`` after our purge_messages command, add the following:

.. code-block:: python
    :linenos:

    @purge_messages.set_error_handler
    async def on_purge_error(event: lightbulb.CommandErrorEvent) -> bool:
        exception = event.exception.__cause__ or event.exception

        if isinstance(exception, lightbulb.MissingRequiredPermission):
            await event.context.respond("You do not have permission to use this command.")
            return True

        elif isinstance(exception, lightbulb.BotMissingRequiredPermission):
            await event.context.respond("I do not have permission to delete messages.")
            return True

        return False

- **Line 1** - Set the decorated function as ``purge_messages``'s error handler
- **Line 2** - The error handler takes one arguement: ``lightbulb.CommandErrorEvent``, and must return a ``boolean``
- **Line 3** - Unwrap the original cause of the error
- **Line 5-6** - If the exception is that the user who ran the command is missing the required permissions, we let them know with a small message.
- **Line 7** - We must return ``True`` if the error has been handled, this way lightbulb knows not to raise the error
- **Line 9-11** - If the exception is that the bot does not have permission to delete messages, we let the user know, and again return ``True``
- **Line 13** - If the error hasn't been handled (it may have been cause by something other than missing permissions), we return ``False``, so lightbulb will raise the error

`Read the docs - Error Handling <https://hikari-lightbulb.readthedocs.io/en/latest/guides/error-handling.html>`_