from logging import getLogger
from telegram.ext import Updater, MessageHandler, Filters

from inquisicion.util.config import Config
from inquisicion.util.nsfw import NSFW

logger = getLogger(__name__)
cfg = Config()


class Bot(object):
    """
    This class implements the handlers for InquisicionBot
    """

    @property
    def _dispatcher(self):
        """
        Return the dispatcher from the Telegram Updater
        """
        return self._updater.dispatcher

    @staticmethod
    def _nsfw_message(nsfw_ratio):
        """
        Returns the interpoled message if the image is NSFW
        """
        return ("🔞 nsfweablity of {} {}Nobody expects the "
                "Spanish Inquisition").format(nsfw_ratio, '\n' * 45)

    @staticmethod
    def _get_bytes(message):
        """
        Get the byte-array from the photo or the sticker
        """
        if len(message.photo):
            return message.photo[1].get_file().download_as_bytearray()
        return message.sticker.get_file().download_as_bytearray()

    @classmethod
    def _image_handler(cls, bot, update):
        """
        This Handler is used to detect image messages. Then the image is
        downloaded as a bytearray, and passed to the NSFW Helper
        """
        logger.debug('Receiving image')
        nsfw = NSFW(cls._get_bytes(update.message))
        nsfw.process()
        if update.effective_chat.type == 'private':
            logger.debug("({}) NSFW ratio of {}".format(
                update.effective_user.name, nsfw.nsfw_ratio))
            bot.send_message(
                chat_id=update.message.chat_id,
                text="NSFW ratio of {}".format(nsfw.nsfw_ratio))
        elif nsfw.is_nsfw():
            logger.debug("({}) NSFW detected of {}".format(
                update.effective_user.name, nsfw.nsfw_ratio))
            bot.send_message(
                chat_id=update.message.chat_id,
                text=cls._nsfw_message(nsfw.nsfw_ratio))

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
        # Handle incoming images
        self._dispatcher.add_handler(
            MessageHandler(Filters.photo | Filters.sticker,
                           self._image_handler))

        # Handle errors
        self._dispatcher.add_error_handler(self._error_handler)

    def start(self):
        """
        Start polling the messages from telegram
        """
        self._updater.start_polling()
        self._updater.idle()

    def __init__(self):
        """
        Constructor for the Bot
        """
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
