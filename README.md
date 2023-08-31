# Meat

The half-baked genetic experiment of Shang Tsung. But more importantly, the one who got away. 💔

Made and ran for [SCROTEGANG](https://twitter.com/scrotegang).

# Running
You can run Meat using the provided [Docker image](https://github.com/SCROTEGANG/meat/pkgs/container/meat). However you will have to train your own GPT-2 model. Check out [aitextgen](https://github.com/minimaxir/aitextgen) for more info on doing that.

```sh
# Your Discord bot token
MEAT_TOKEN=wowafake.token
# Path to your trained model
MEAT_MODEL_PATH=/trained_model
# Azure text translation variables so Meat can speak Korean.
# See https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation-overview for more info.
MEAT_TRANSLATE_KEY=wowthisisfake
MEAT_TRANSLATE_REGION=westus2
MEAT_TRANSLATE_ENDPOINT=https://somelink.url
# Path to the Meat's config file
MEAT_CONFIG_PATH=/config/config.json
# Toggles Meat speaking on his own when a config doesn't exist
MEAT_SPEAK_DEFAULT=true
 # The channel to speak in
MEAT_SPEAK_CHANNEL=1111111111112
```

# License
[GPL](LICENSE)