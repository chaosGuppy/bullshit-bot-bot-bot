# bullshit-bot-bot-bot

A bot (bot bot) for dealing with social media bullshit.

## Running the bot

Copy the `.env.example` file to `.env`

##### In Telegram

- DM @BotFather
- Send `/newbot` command
- Copy the API key into the `.env` file as `TELEGRAM_TOKEN`
- It will also output a link to talk to the bot

##### OpenAI

- Copy your API key to the `.env` file as `OPENAI_API_KEY`

##### Google

- Got to https://console.cloud.google.com/ and create a project
- Generate an API key to use as the `GOOGLE_API_KEY`

##### Root

```sh
poetry install
poetry shell
python bullshit_bot_bot_bot/run.py
```

If you send any `/` commands you should see results from the bot
