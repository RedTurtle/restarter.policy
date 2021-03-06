from zope.interface import Interface


class IRestarterConfiguration(Interface):

    def showBigLogo():
        """Return True if the big logo should be displayed"""

    def isHomePage():
        """Return True if we are in homepage"""

    def safe_truncate(text,size):
        """Return truncated text"""

    def getMemberInfo(member_id=None):
        """Return restarter memberinfo """

    def path_from_uid():
        """Return path for request uid params"""
