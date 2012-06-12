from zope.interface import Interface
from zope import schema

# from restarter.policy import MessageFactory as _

class IStatsTool(Interface):
    """ Marker """

class IStatsSettings(Interface):
    """    concurrency = schema.Int(
        title=_(u'Concurrency'),
        description=_(u'This decides the number of simultaneous downloads.'),
        required=True,
        default=5,
        )
    """
    
    interval = schema.Int(
        title=u'Update interval',
        required=True,
        default=300,
        )
    """
    expiration = schema.Int(
        title=_(u'Expiration'),
        description=_(u'This decides the link expiration threshold. Enter '
                      u'the number of days that a link should be valid '
                      u'after an appearance in the page output.'),
        required=True,
        default=7,
        )

    transaction_size = schema.Int(
        title=_(u'Transaction size'),
        description=_(u'The number of items pulled out of the worker queue '
                      u'for every transaction.'),
        required=True,
        default=100,
        )

    use_publisher = schema.Bool(
        title=_(u'Use publisher'),
        description=_(u"Select this option to publish internal links "
                      u"that have not been requested, and thus have no "
                      u"recorded response status."),
        required=False,
        default=False,
        )

"""
