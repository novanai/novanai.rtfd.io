Part 6 - Message Components
====================================

Message components are a relatively new feature on Discord, allowing you to attach buttons and select menus to messages!

Let's add some new code to ``fun.py``.

At the very top of the file, import asyncio:

.. code-block:: python

    import asyncio

Then, insert the following after the ``meme`` command, but above the ``load`` function:

.. code-block:: python
    :linenos:

    ANIMALS = {
        "Dog": "🐶",
        "Cat": "🐱",
        "Panda": "🐼",
        "Fox": "🦊",
        "Red Panda": "🐼",
        "Koala": "🐨",
        "Bird": "🐦",
        "Racoon": "🦝",
        "Kangaroo": "🦘",
    }


    @fun_group.child
    @lightbulb.command("animal", "Get a fact + picture of a cute animal :3")
    @lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
    async def animal_subcommand(ctx: lightbulb.Context) -> None:
        select_menu = (
            ctx.bot.rest.build_action_row()
            .add_select_menu("animal_select")
            .set_placeholder("Pick an animal")
        )

        for name, emoji in ANIMALS.items():
            select_menu.add_option(
                name,  # the label, which users see
                name.lower().replace(" ", "_"),  # the value, which is used by us later
            ).set_emoji(emoji).add_to_menu()

        resp = await ctx.respond(
            "Pick an animal from the dropdown :3",
            component=select_menu.add_to_container(),
        )
        msg = await resp.message()

        try:
            event = await ctx.bot.wait_for(
                hikari.InteractionCreateEvent,
                timeout=60,
                predicate=lambda e: isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU,
            )
        except asyncio.TimeoutError:
            await msg.edit("The menu timed out :c", components=[])
        else:
            animal = event.interaction.values[0]
            async with ctx.bot.d.aio_session.get(
                f"https://some-random-api.ml/animal/{animal}"
            ) as res:
                if res.ok:
                    res = await res.json()
                    embed = hikari.Embed(description=res["fact"], colour=0x3B9DFF)
                    embed.set_image(res["image"])

                    animal = animal.replace("_", " ")

                    await msg.edit(
                        f"Here's a {animal} for you! :3", embed=embed, components=[]
                    )
                else:
                    await msg.edit(f"API returned a {res.status} status :c", components=[])

- **Line 1-11** - Create a `dict <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`_ containing all the possible endpoints of `some-random-api.ml/animal/ <https://some-random-api.ml/endpoints>`_
- **Line 14-16** - Set up prefix and slash subcommands
- **Line 18-22**
    - Create an `action row <https://www.hikari-py.dev/hikari/api/rest.html#hikari.api.rest.RESTClient.build_action_row>`_, which returns an `ActionRowBuilder <https://www.hikari-py.dev/hikari/api/special_endpoints.html#hikari.api.special_endpoints.ActionRowBuilder>`_
    - Add a select menu to the action row, with "``animal_select``" as the custom ID 
    - Set the placeholder (the text that is seen when no option has been picked) to ``Pick an animal``
- **Line 24-28** - For all the items in the ``ANIMALS`` dict, add an option to the select menu (`Read the docs - SelectMenuBuilder.add_option <https://www.hikari-py.dev/hikari/api/special_endpoints.html#hikari.api.special_endpoints.SelectMenuBuilder.add_option>`_) with
    - The name
    - The value, which is the name of the animal but lowercased and with spaces replaced with underscores
    - Setting the emoji to the value of the animal in the ``ANIMALS`` dict
- **Line 30-34**
    - Respond to the context with the select menu
    - Fetch the message from the response (`Read the docs - ResponseProxy <https://hikari-lightbulb.readthedocs.io/en/latest/api_references/context.html#lightbulb.context.base.ResponseProxy>`_)
- **Line 36-44** - Wait for an interaction to be created and
    - Check if the interaction is a component interaction
    - Check that the interaction user is the same who ran the command
    - Check that the interaction message is the same as the message we sent
    - Check that the interaction component type is a select menu
- **Line 45-46** - If the interaction times out, an ``asyncio.TimeoutError`` will be raised, and so we can use that to handle the timeout by editing the message and removing the components
- **Line 48** - Get the value of the interaction (the selected option) - `Read the docs - ComponentInteraction.values <https://www.hikari-py.dev/hikari/interactions/component_interactions.html#hikari.interactions.component_interactions.ComponentInteraction.values>`_
- **Line 49-51** - Make a ``GET`` request to `some-random-api.ml <https://some-random-api.ml/>`_ with the selected animal as the option
- **Line 52** - If the response has an ``ok`` status, then
    - **Line 53** - Get the response's json
    - **Line 54** - Create an embed, setting its title to the animal fact
    - **Line 55** - Set the embed's image to the animal image
    - **Line 57** - Replace the underscore in animal with a space
    - **Line 59-61** - Edit the message to contain the embed, and remove the select menu component
- **Line 62** - Otherwise, if the response was not successful, then
    - **Line 63** - Edit the message to say what status code the API responded with, and remove the select menu component

.. image:: ../_static/animal_1.png

.. image:: ../_static/animal_2.png

.. image:: ../_static/animal_3.png

And if the menu times out:

.. image:: ../_static/animal_4.png

`Read the docs - Components <https://hikari-lightbulb.readthedocs.io/en/latest/hikari_basics/components.html>`_