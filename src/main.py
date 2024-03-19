from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
from responses import get_response

load_dotenv()

TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
PREFIX: Final[str] = os.getenv("COMMAND_PREFIX")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        (
            await message.author.send(response)
            if is_private
            else await message.channel.send(response)
        )
    except Exception as e:
        print(e)


async def calculate(expression: str) -> float:
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"


async def handle_calculate_command(message: Message, command: str) -> None:
    expression = command[len("calculate") :].strip()
    result = await calculate(expression)
    await send_message(message, str(result))


@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    content: str = message.content
    if content.startswith(PREFIX):
        command = content[len(PREFIX) :].strip()
        if command.startswith("calculate"):
            await handle_calculate_command(message, command)

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
