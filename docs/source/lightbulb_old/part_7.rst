Part 7 - Miru, an optional component handler
============================================

`Miru <https://hikari-miru.readthedocs.io/en/latest/index.html>`_ is an optional component handler for hikari, making it *much*
simpler to add components to messages, and to handle component interactions too.

We'll need to edit ``bot.py`` a little bit to get miru working.

At the top of the file, import miru:

.. code-block:: python

    import miru

And just above ``bot.load_extensions_from("./extensions/")`` add:

.. code-block:: python

    miru.load(bot)

Now we need to edit ``fun.py``.

At the top of the file, import miru:

.. code-block:: python

    import miru

And now beneath our ``animal`` command, add the following:

.. code-block:: python
    :linenos:

    class AnimalView(miru.View):
        def __init__(self, author: hikari.User) -> None:
            self.author = author
            super().__init__(timeout=60)

        @miru.select(
            custom_id="animal_select",
            placeholder="Pick an animal",
            options=[
                miru.SelectOption("Dog", "dog", emoji="🐶"),
                miru.SelectOption("Cat", "cat", emoji="🐱"),
                miru.SelectOption("Panda", "panda", emoji="🐼"),
                miru.SelectOption("Fox", "fox", emoji="🦊"),
                miru.SelectOption("Red Panda", "red_panda", emoji="🐼"),
                miru.SelectOption("Koala", "koala", emoji="🐨"),
                miru.SelectOption("Bird", "bird", emoji="🐦"),
                miru.SelectOption("Racoon", "racoon", emoji="🦝"),
                miru.SelectOption("Kangaroo", "kangaroo", emoji="🦘"),
            ],
        )
        async def select_menu(self, select: miru.Select, ctx: miru.Context) -> None:
            animal = select.values[0]
            async with ctx.app.d.aio_session.get(
                f"https://some-random-api.ml/animal/{animal}"
            ) as res:
                if res.ok:
                    res = await res.json()
                    embed = hikari.Embed(description=res["fact"], colour=0x3B9DFF)
                    embed.set_image(res["image"])

                    animal = animal.replace("_", " ")

                    await ctx.edit_response(
                        f"Here's a {animal} for you! :3", embed=embed, components=[]
                    )
                else:
                    await ctx.edit_response(
                        f"API returned a {res.status} status :c", components=[]
                    )

        async def on_timeout(self) -> None:
            await self.message.edit("The menu timed out :c", components=[])

        async def view_check(self, ctx: miru.Context) -> bool:
            return ctx.user.id == self.author.id


    @fun_group.child
    @lightbulb.command("animal2", "Get a fact + picture of a cute animal :3")
    @lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashSubCommand)
    async def animal_subcommand_2(ctx: lightbulb.Context) -> None:
        view = AnimalView(ctx.author)
        resp = await ctx.respond(
            "Pick an animal from the dropdown :3", components=view.build()
        )
        msg = await resp.message()

        view.start(msg)
        await view.wait()

This new ``animal2`` command produces the exact same result as the first ``animal`` command, but it's much easier to read
and understand at a glance, and adding buttons or other select menus would be incredibly easy.

- **Line 1** - Subclass ``miru.View``, to create our custom ``AnimalView`` class
- **Line 4** - Initialise our view with a timeout of 60 seconds
- **Line 6-20** - Create our `select menu <https://hikari-miru.readthedocs.io/en/latest/api_references/select.html>`_, with the same custom ID, placeholder and options as before
- **Line 22-39** - Perform the same request as before, and respond to the interaction with an embed
- | **Line 41-45** - Set our timeout function, and a view check
  | `Read the docs - View Checks & Timeout Handling <https://hikari-miru.readthedocs.io/en/latest/guides/checks_timeout.html>`_
- **Line 48-50** - Create a second animal command, called "``animal2``" 
- **Line 52** - Create an instance of ``AnimalView``
- **Line 53-55** - Respond to the command interaction with our message and components
- **Line 58** - Start the view
- **Line 59** - Wait for the view to finish

.. note::

    If you want to learn how to use buttons and more with Miru, check out the Miru guides, written by Miru's creator:
    https://hikari-miru.readthedocs.io/en/latest/getting-started.html