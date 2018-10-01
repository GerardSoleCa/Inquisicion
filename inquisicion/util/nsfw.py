from logging import getLogger
from os import write, close, remove
from tempfile import mkstemp
from nsfw import classify
from PIL import Image

logger = getLogger(__name__)


class NSFW(object):
    """
    Manage the Yahoo NSFW Neural Network
    """
    NSFW_RATIO = 0.7

    def process(self):
        """
        Analyze the given image
        """
        try:
            logger.debug('Start analyzing the image')
            img = Image.open(self.file_path)
            img.convert('RGB')
            self.sfw_ratio, self.nsfw_ratio = classify(img)
            logger.debug('Ended analyzing the image')
        except IOError as e:
            logger.error("Exception with PIL Image: {}".format(e.message))
            raise
        finally:
            remove(self.file_path)

    def is_nsfw(self):
        """
        Returns True if image is considered NSFW
        """
        return self.nsfw_ratio > self.NSFW_RATIO

    def __init__(self, image):
        """
        Constructor must be supplied with an image being a byte-array.
        """
        self.file, self.file_path = mkstemp()
        write(self.file, image)
        close(self.file)
        self.sfw_ratio = 0
        self.nsfw_ratio = 0
