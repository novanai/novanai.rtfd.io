# Part 6 - Message Components

Let's add some new code to `fun.py`.

At the very top of the file, import asyncio:

```{code-block}  python
import asyncio
```

Then, insert the following after the `meme` command, but above the `load` function:

```{code-block} python
:linenos:

ANIMALS = {
    "Bird": "🐦",
    "Cat": "🐱",
    "Dog": "🐶",
    "Fox": "🦊",
    "Kangaroo": "🦘",
    "Koala": "🐨",
    "Panda": "🐼",
    "Raccoon": "🦝",
    "Red Panda": "🐼", 
}


@fun_group.child
@lightbulb.command("animal", "Get a fact & picture of a cute animal :3")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def animal_subcommand(ctx: lightbulb.SlashContext) -> None:
    select_menu = (
        ctx.bot.rest.build_message_action_row()
        .add_select_menu(hikari.ComponentType.TEXT_SELECT_MENU, "animal_select")
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
            and e.interaction.component_type == hikari.ComponentType.TEXT_SELECT_MENU,
        )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        async with ctx.bot.d.client_session.get(
            f"https://some-random-api.com/animal/{animal}"
        ) as res:
            if not res.ok:
                await msg.edit(f"API returned a {res.status} status :c", components=[])
                return

            data = await res.json()
            embed = hikari.Embed(description=data["fact"], colour=0x3B9DFF)
            embed.set_image(data["image"])

            animal = animal.replace("_", " ")

            await msg.edit(f"Here's a {animal} for you! :3", embed=embed, components=[])
```

- **Line 1-11** - Create a [dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) containing all the possible endpoints of [some-random-api.com/animal/](https://some-random-api.com/endpoints)
- **Line 14-16** - Set up the slash subcommand
- **Line 18-22** - Create a [message action row](https://www.hikari-py.dev/hikari/api/rest.html#hikari.api.rest.RESTClient.build_action_row)
    - Add a select menu to the action row, with "`animal_select`" as the custom ID
    - Set the placeholder (the text that is seen when no option has been picked) to "`Pick an animal`"
- **Line 24-28** - For all the items in the `ANIMALS` dict,
    - add an option to the select menu ([Read the docs - SelectMenuBuilder.add_option](https://www.hikari-py.dev/hikari/api/special_endpoints.html#hikari.api.special_endpoints.SelectMenuBuilder.add_option)) with
        - the name
        - the value, which is the name of the animal in lowercase with spaces replaced by underscores
    - and set the emoji for the option
- **Line 30-34**
    - Respond to the context with the select menu
    - Fetch the message from the response ([Read the docs - ResponseProxy](https://hikari-lightbulb.readthedocs.io/en/latest/api_references/context.html#lightbulb.context.base.ResponseProxy))
- **Line 36-44** - Wait for an interaction to be created, and check that
    - the interaction is a component interaction
    - the interaction user is the same user who ran the command
    - the interaction message is the same as the message we responded with
    - the interaction component type is a select menu
- **Line 45-46** - If the interaction times out, an `asyncio.TimeoutError` will be raised, and so we can use that to handle the timeout by editing our response and removing the components
- **Line 48** - Get the value of the interaction (the selected option) - [Read the docs - ComponentInteraction.values](https://www.hikari-py.dev/hikari/interactions/component_interactions.html#hikari.interactions.component_interactions.ComponentInteraction.values)
- **Line 49-51** - Make a `GET` request to [some-random-api.com/animal/](https://some-random-api.com/endpoints) with the selected animal as the option
- **Line 52-54** - If the response doesn't have an `ok` status,
    - edit our response and remove the message components
    - `return` so no further code will be run
- **Line 56-62** - If the response was successful,
    - **Line 56** - Get the response's json
    - **Line 57** - Create an embed, setting its title to the animal fact
    - **Line 58** - Set the embed's image to the animal image
    - **Line 60** - Replace the underscore in `animal` with a space
    - **Line 62** - Edit the message to contain the embed, and remove the select menu component

![animal](../_static/lightbulb/animal_1.png)
![animal](../_static/lightbulb/animal_2.png)

And if the menu times out:

![animal](../_static/lightbulb/animal_3.png)

```{note}
[some-random-api.com](https://some-random-api.com/endpoints) has a lot of different endpoints, all fun and useful for a Discord bot. If you want to make more API-centred commands, it's a great API to use!
```

[Read the docs - Components](https://hikari-lightbulb.readthedocs.io/en/latest/hikari_basics/components.html)
