import discord
import datetime
import requests
import os
from dotenv import load_dotenv


client = discord.Client()
load_dotenv()


def get_isitfullmoon_data():
    data = requests.get("http://isitfullmoon.com/api.php?format=json").json()[
        "isitfullmoon"
    ]

    prevmoon = datetime.date.today() - datetime.date.fromtimestamp(data["prev"])
    nextmoon = datetime.date.fromtimestamp(data["next"]) - datetime.date.today()
    data["dayssince"] = prevmoon.days
    data["daystill"] = nextmoon.days

    return data


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!moon"):
        data = get_isitfullmoon_data()
        if data["status"] == "Yes":
            await message.channel.send("The full moon is upon us tonight :full_moon:")
        elif data["dayssince"] < 4:
            await message.channel.send(
                "The moon is waning gibbous tonight :waning_gibbous_moon: \n"
                + "The last full moon was "
                + str(data["dayssince"])
                + " days ago"
            )
        elif data["dayssince"] < 8:
            await message.channel.send(
                "The moon is in third quarter tonight :last_quarter_moon: \n"
                + "The last full moon was "
                + str(data["dayssince"])
                + " days ago"
            )
        elif data["dayssince"] < 12:
            await message.channel.send(
                "The moon is waning crescent tonight :waning_crescent_moon: \n"
                + "The last full moon was "
                + str(data["dayssince"])
                + " days ago"
            )
        elif data["dayssince"] < 16:
            await message.channel.send(
                "A new moon is forming tonight :new_moon: \n"
                + "It will be full in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] < 20:
            await message.channel.send(
                "The moon is waxing crescent tonight :waxing_crescent_moon: \n"
                + "The next full moon is in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] < 24:
            await message.channel.send(
                "The moon is in first quarter tonight :first_quarter_moon: \n"
                + "The next full moon is in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] < 28:
            await message.channel.send(
                "The moon is waxing gibbous tonight :waxing_gibbous_moon: \n"
                + "The next full moon is in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] == 28:
            await message.channel.send(
                "The night after next marks the full moon. Beware of chaos magic "
                + ":new_moon_with_face:"
            )


client.run(os.getenv("BOT_TOKEN"))
