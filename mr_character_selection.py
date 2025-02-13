import discord
import mr_api as mr

class RoleView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Please Select a Role!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label = "Vanguard"
            ),
            discord.SelectOption(
                label = "Strategist",
            ),
            discord.SelectOption(
                label = "Duelist"
            )
        ]
    )

    async def characterCallback(self, interaction: discord.Interaction, select):
        if select.values[0] == "Vanguard":
            await interaction.response.send_message(view = VanguardView())
        elif select.values[0] == "Strategist":
            await interaction.response.send_message(view = StrategistView())
        else:
            await interaction.response.send_message(view = DuelistView())


class VanguardView(discord.ui.View):

    @discord.ui.select(
        placeholder = "Please Select a Character!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label = "Bruce Banner"
            ),
            discord.SelectOption(
                label = "Doctor Strange"
            ),
            discord.SelectOption(
                label = "Captain America"
            ),
            discord.SelectOption(
                label = "Groot"
            ),
            discord.SelectOption(
                label = "Venom"
            ),
            discord.SelectOption(
                label = "Magneto"
            ),
            discord.SelectOption(
                label = "Thor"
            ),
            discord.SelectOption(
                label = "Peni Parker"
            ),
        ]
    )

    async def characterCallback(self, interaction: discord.Interaction, select):
        character = mr.character_stats(select.values[0])
        await interaction.response.send_message(character)

class StrategistView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Please Select a Character!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label = "Loki"
            ),
            discord.SelectOption(
                label = "Mantis",
            ),
            discord.SelectOption(
                label = "Rocket Raccoon"
            ),
            discord.SelectOption(
                label = "Cloak & Dagger"
            ),
            discord.SelectOption(
                label = "Luna Snow"
            ),
            discord.SelectOption(
                label = "Adam Warlock"
            ),
            discord.SelectOption(
                label = "Jeff"
            )
        ]
    )

    async def characterCallback(self, interaction: discord.Interaction, select):
        character = mr.character_stats(select.values[0])
        await interaction.response.send_message(character)

class DuelistView(discord.ui.View):

    @discord.ui.select(
        placeholder = "Please Select a Character!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label = "The Punisher"
            ),
            discord.SelectOption(
                label = "Storm"
            ),
            discord.SelectOption(
                label = "Hawkeye"
            ),
            discord.SelectOption(
                label = "Hela"
            ),
            discord.SelectOption(
                label = "Black Panther"
            ),
            discord.SelectOption(
                label = "Magik"
            ),
            discord.SelectOption(
                label = "Moon Knight"
            ),
            discord.SelectOption(
                label = "Squirrel Girl"
            ),
            discord.SelectOption(
                label = "Black Widow"
            ),
            discord.SelectOption(
                label = "Iron Man"
            ),
            discord.SelectOption(
                label = "Spider-man"
            ),
            discord.SelectOption(
                label = "Scarlet Witch"
            ),
            discord.SelectOption(
                label = "Mister Fantastic"
            ),
            discord.SelectOption(
                label = "Winter Soldier"
            ),
            discord.SelectOption(
                label = "Star-lord"
            ),
            discord.SelectOption(
                label = "Namor"
            ),
            discord.SelectOption(
                label = "Pyslocke"
            ),
            discord.SelectOption(
                label = "Wolverine"
            ),
            discord.SelectOption(
                label = "Iron Fist"
            )
        ]
    )

    async def characterCallback(self, interaction: discord.Interaction, select):
        character = mr.character_stats(select.values[0])
        await interaction.response.send_message(character)