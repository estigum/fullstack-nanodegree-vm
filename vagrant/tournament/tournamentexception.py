"""
This module is a specific exeption for swiss tournament
"""
__author__ = "Erik Stigum"
__copyright__ = "Copyright 2015, Swiss Tournament"
__email__ = "estigum@gmail.com"
__version__ = "1.0"

class TournamentExeption(Exception):
    """
    This class is just a specif exeption for
    swiss tournament.  Will use this when loading
    the configuration
    """

    def __init__(self, message):
        """
        This is the constructor
        :param message:
        :return:
        """

        super(TournamentExeption, self).__init__(message)
        self.message = message

