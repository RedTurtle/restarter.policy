from zope.interface import Interface

class IRestarterConfiguration(Interface):
    def isHomePage():
        """Return True if we are in homepage"""
