from configparser import ConfigParser
from logging import StreamHandler, getLogger, DEBUG, Formatter
from os import getenv
from os.path import realpath, dirname
from sys import stdout

from inquisicion.util.singleton import Singleton


class Config(Singleton):
    __instance = None

    @property
    def token(self):
        """
        Returns the token from the config file
        """
        return getenv('TOKEN', self._parser.get('credentials', 'token'))

    @staticmethod
    def _development_formatter():
        """
        Configure the development formatter for the logger
        """
        return Formatter(fmt=('%(asctime)s %(levelname)-5.5s '
                              '[%(name)s:%(lineno)d] %(message)s'),
                         datefmt='%Y-%m-%d %H:%M:%S')

    def __logger(self):
        """
        Configure the logger for the application
        """
        logger = getLogger('inquisicion')
        handler = StreamHandler(stdout)
        handler.setFormatter(self._development_formatter())
        logger.setLevel(DEBUG)
        logger.addHandler(handler)

    def init(self):
        """
        Instead of implementing __init__ we implement init, which will be
        called by the singleton upper class.
        """
        self.__logger()
        self._parser = ConfigParser()
        self._parser.read("{}/../config/config.ini".format(
            dirname(realpath(__file__))))
