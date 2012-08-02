""" Subtypes interfaces
"""
from zope import schema
from zope.interface import Interface


class IHomeStory(Interface):
    """ Marker interface that tells wheter
        the company story should be displayed on homepage"""


class IHomeStoriesSubtyper(Interface):
    """ Support for homepage stories
    """

    can_enable = schema.Bool(u'Can enable homepage stories',
                             readonly=True)
    can_disable = schema.Bool(u'Can disable homepage stories',
                              readonly=True)

    def enable():
        """ Enable homepage stories
        """

    def disable():
        """Disable homepage stories
        """
