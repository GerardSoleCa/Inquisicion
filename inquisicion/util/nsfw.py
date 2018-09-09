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

    def is_nsfw(self):
        """
        Analyze the given image and return a boolean depending on the results
        of the neural network
        """
        try:
            logger.debug('Start analyzing the image')
            img = Image.open(self.file_path)
            img.convert('RGB')
            _, nsfw = classify(img)
            return nsfw > 0.7 # Consider NSFW if ratio is higher than 0.7
        except IOError as e:
            logger.error("Exception with PIL Image: {}".format(e.message))
            return False
        finally:
            remove(self.file_path)

    def __init__(self, image):
        """
        Constructor must be supplied with an image being a byte-array.
        """
        self.file, self.file_path = mkstemp()
        write(self.file, image)
        close(self.file)
