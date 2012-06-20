from zope.interface import Interface


class IRestarterConfiguration(Interface):

    def showBigLogo():
        """Return True if the big logo should be displayed"""

    def isHomePage():
        """Return True if we are in homepage"""

    def safe_truncate(text,size):
        """Return truncated text"""
