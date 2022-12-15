# YDBOT

This is a simple Discord bot that can be run from Docker.

## Requirements

 1. Discord Bot Token [Guide](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot)
 2. Youtube Api Token [Guide](https://blog.hubspot.com/website/how-to-get-youtube-api-key)

## Features

- Can search Youtube videos
- It can show the information of a Youtube video.

## Commands

**!{PREFIX}yvideo _url_:** Show the information of the video

**!{PREFIX}svideo _search text_:** Search and display videos

## Enviroment Variables

ENV | VALUE
--- | ---
_DISCORD_TOKEN_ | Here goes the token of your discord bot
_PREFIX_  | Here goes the prefix that will be used when executing commands
_OWNER_ID_ | Here goes your discord user ID
_DEVELOPER_KEY_  | Here goes your Youtube Api Token

## Installation

### Docker

This repo supplies a Dockerfile for simplified deployment.
First build the docker image.

```console
docker build -t YDBOT .
```

Now you can run your docker image.

```console
docker run -it -e DISCORD_TOKEN=YOUR_BOT_TOKEN \ 
-e PREFIX=YOUR_PREFIX \ 
-e OWNER_ID=YOUR_DISCORD_ID_ACCOUNT \
-e DEVELOPER_KEY=YOUR_YOUTUBE_API_KEY \
-p 8080:8080 discord-bot
```
