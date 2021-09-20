import discord
import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()
client = discord.Client()
BOT_TOKEN = os.getenv('BOT_TOKEN')


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
            await message.channel.send("Tonight the full moon is upon us :full_moon:")
        elif data["dayssince"] < 4:
            await message.channel.send(
                "Tonight the moon is waning gibbous :waning_gibbous_moon: \n"
                + "The last full moon was "
                + str(data["dayssince"])
                + " days ago"
            )
        elif data["dayssince"] < 8:
            await message.channel.send(
                "Tonight the moon is third quarter :last_quarter_moon: \n"
                + "The last full moon was "
                + str(data["dayssince"])
                + " days ago"
            )
        elif data["dayssince"] < 12:
            await message.channel.send(
                "Tonight the moon is waning crescent :waning_crescent_moon: \n"
                + "The last full moon was "
                + str(data["dayssince"])
                + " days ago"
            )
        elif data["dayssince"] < 16:
            await message.channel.send(
                "Tonight a new moon is forming :new_moon: \n"
                + "It will be full in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] < 20:
            await message.channel.send(
                "Tonight the moon is waxing crescent :waxing_crescent_moon: \n"
                + "The next full moon is in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] < 24:
            await message.channel.send(
                "Tonight the moon is first quarter :first_quarter_moon: \n"
                + "The next full moon is in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] < 28:
            await message.channel.send(
                "Tonight the moon is waxing gibbous :waxing_gibbous_moon: \n"
                + "The next full moon is in "
                + str(data["daystill"])
                + " days"
            )
        elif data["dayssince"] == 28:
            await message.channel.send(
                "The night after next marks the full moon. Beware of chaos magic "
                + ":new_moon_with_face:"
            )


client.run(BOT_TOKEN)
