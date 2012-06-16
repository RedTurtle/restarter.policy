from zope.interface import Interface


class IRestarterConfiguration(Interface):

    def isHomePage():
        """Return True if we are in homepage"""

    def safe_truncate(text,size):
        """Return truncated text"""
