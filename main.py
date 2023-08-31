import os
import sys
import asyncio

from meat import Meat

OPTIONS = [
    "MEAT_MODEL_PATH",
    "MEAT_TRANSLATE_KEY",
    "MEAT_TRANSLATE_REGION",
    "MEAT_TRANSLATE_ENDPOINT",
    "MEAT_CONFIG_PATH",
    "MEAT_SPEAK_DEFAULT",
    "MEAT_SPEAK_CHANNEL",
]


async def main():
    options = {}

    for option in OPTIONS:
        val = os.getenv(option)
        if val is None:
            sys.exit(f"${option} is a required option that is missing")

        if option == "MEAT_SPEAK_CHANNEL":
            options[option] = int(val)
            continue

        options[option] = val

    speak_default = os.getenv("MEAT_SPEAK_DEFAULT")
    if speak_default is not None:
        options["MEAT_SPEAK_DEFAULT"] = True

    client = Meat(options=options)
    async with client:
        token = os.getenv("MEAT_TOKEN")
        if token is None:
            sys.exit("$MEAT_TOKEN is not set")

        await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
