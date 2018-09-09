# Inquisición

Spanish Inquisition is back!

This Telegram Bot will stalk your group messages, and if it detects an inapropriate
image, it will send a blank message just to move away the picture.

## Information

This bot has been built using:
 
 * Yahoo's NSFW Neural Network: https://github.com/yahoo/open_nsfw
 * Python's Telegram Bot: https://github.com/python-telegram-bot/python-telegram-bot
 
## Dev Dependencies

* Python3
* pip == 9.0.3 (higher versions will break the build scripts)
* Caffe (caffe-cpu package will work)

## Docker

An image docker is supplied so you can avoid all the issues to install caffe and python.

```bash
docker pull gerardsoleca/inquisicion
docker run -d --env TOKEN=<here-your-bot-token> --name InquisicionBot gerardsoleca/inquisicion
```