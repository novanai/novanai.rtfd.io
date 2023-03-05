# Part 7 - Miru, an optional component handler

[Miru](https://hikari-miru.readthedocs.io/en/latest/index.html) is an optional component handler for hikari, making it simpler to add components to messages, and to handle component interactions.

We'll need to edit `bot.py` a little bit to get miru working.

At the top of the file, import miru:

```{code-block} python
import miru
```

And just above `bot.load_extensions_from("./extensions/")` add:

```{code-block} python
miru.load(bot)
```

Now we need to edit `fun.py`.

At the top of the file, import miru:

```{code-block} python
import miru
```

And now beneath our `animal` command, add the following:

```{code-block} python
:linenos:

class AnimalView(miru.View):
    def __init__(self, author: hikari.User) -> None:
        self.author = author
        super().__init__(timeout=60)

    @miru.text_select(
        custom_id="animal_select",
        placeholder="Pick an animal",
        options=[
            miru.SelectOption(name, name.lower().replace(" ", "_"), emoji=emoji)
            for name, emoji in ANIMALS.items()
        ],
    )
    async def select_menu(self, select: miru.TextSelect, ctx: miru.ViewContext) -> None:
        animal = select.values[0]
        async with ctx.app.d.client_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if not res.ok:
                await ctx.edit_response(
                    f"API returned a {res.status} status :c", components=[]
                )
                return

            data = await res.json()
            embed = hikari.Embed(description=data["fact"], colour=0x3B9DFF)
            embed.set_image(data["image"])

            animal = animal.replace("_", " ")

            await ctx.edit_response(
                f"Here's a {animal} for you! :3", embed=embed, components=[]
            )

    async def on_timeout(self) -> None:
        await self.message.edit("The menu timed out :c", components=[])

    async def view_check(self, ctx: miru.ViewContext) -> bool:
        return ctx.user.id == self.author.id


@fun_group.child
@lightbulb.command("animal2", "Get a fact + picture of a cute animal :3")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def animal_subcommand_2(ctx: lightbulb.SlashContext) -> None:
    view = AnimalView(ctx.author)
    resp = await ctx.respond(
        "Pick an animal from the dropdown :3", components=view.build()
    )

    await view.start(resp)
    await view.wait()
```

This new `animal2` command produces the exact same result as the first `animal` command, but it's much easier to read and understand at a glance, and adding buttons or more select menus would be incredibly easy.

- **Line 1** - Subclass `miru.View`, to create our custom `AnimalView` class
- **Line 4** - Initialise our view with a timeout of 60 seconds
- **Line 6-13** - Create our [select menu](https://hikari-miru.readthedocs.io/en/latest/api_references/select.html), with the same custom ID, placeholder and options as before
- **Line 14-33** - Perform the same request as before, and respond to the interaction with an embed
- **Line 35-39** - Set our timeout function, and a view check  
    [Read the docs - View Checks & Timeout Handling](https://hikari-miru.readthedocs.io/en/latest/guides/checks_timeout.html)
- **Line 42-44** - Create a second animal command, called "`animal2`"
- **Line 46** - Create an instance of `AnimalView`
- **Line 47-49** - Respond to the command interaction with our message and components
- **Line 51** - Start the view
- **Line 52** - Wait for the view to finish

```{note}
If you want to learn how to use buttons and more with Miru, check out the Miru guides, written by Miru's creator: <https://hikari-miru.readthedocs.io/en/latest/getting-started.html>
```