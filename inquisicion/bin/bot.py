from logging import getLogger
from telegram.ext import Updater, MessageHandler, Filters

from inquisicion.util.config import Config
from inquisicion.util.nsfw import NSFW

logger = getLogger(__name__)
cfg = Config()


class Bot(object):
    _EMPTY_TEXT = ".{}.".format('\n' * 40)

    @property
    def _dispatcher(self):
        return self._updater.dispatcher

    @staticmethod
    def _text_handler(bot, update):
        """
        Echoes text to the chat
        """
        logger.debug('Receiving text')
        # update.message.reply_text(update.message.text)

    @classmethod
    def _image_handler(cls, bot, update):
        logger.debug('Receiving image')
        nsfw = NSFW(update.message.photo[1].get_file().download_as_bytearray())
        if nsfw.is_nsfw():
            update.message.reply_text(cls._EMPTY_TEXT)

    @staticmethod
    def _error_handler(bot, update, error):
        """
        Handle error occurred on the bot
        """
        logger.error("Update {} caused error {}".format(update, error))

    def _configure_handlers(self):
        """
        Setup the handlers to be used within the bot
        """
        # Handle incoming text
        self._dispatcher.add_handler(
            MessageHandler(Filters.text, self._text_handler))

        # Handle incoming images
        self._dispatcher.add_handler(
            MessageHandler(Filters.photo, self._image_handler))

        # Handle errors
        self._dispatcher.add_error_handler(self._error_handler)

    def start(self):
        """
        Start polling the messages from telegram
        """
        self._updater.start_polling()
        self._updater.idle()

    def __init__(self):
        logger.debug('Starting Bot')
        self._updater = Updater(cfg.token)
        self._configure_handlers()


def main():
    """
    Main entry point for the application
    """
    Bot().start()


if __name__ == '__main__':
    """
    Helper to run the bot using directly the source instead of using setup 
    tools
    """
    main()
