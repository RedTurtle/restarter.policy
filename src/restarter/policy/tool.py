import time
import datetime
import logging

# from zc.queue import Queue
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from BTrees.OOBTree import OOBTree
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import registerToolInterface
from Products.CMFCore.utils import getToolByName
from Globals import DevelopmentMode

from .interfaces import IStatsTool

logger = logging.getLogger("restarter.policy")


class StatsTool(SimpleItem):
    security = ClassSecurityInfo()

    def __init__(self, id=None):
        super(StatsTool, self).__init__(id)
        self.last_update = -1
        self.stats = None

    def _getStats(self):
        # BBB:  !!!
        catalog = getToolByName(self, 'portal_catalog')
        stats = dict([(k, len(catalog(Type=k))) \
            for k in catalog.Indexes['Type'].uniqueValues()])
        stats['last_update'] = getattr(self, 'last_update', -1)
        stats['last_uptime'] = datetime.datetime.now()
        return stats
        
    security.declarePrivate("update")
    def update(self):
        """Update link status."""
        counter = getToolByName(self, 'portal_catalog').getCounter()
        now = datetime.datetime.now()
        timestamp = int(time.mktime(now.timetuple()))
        if counter > getattr(self, 'last_update', -1):        
            self.last_update = counter
            self.stats = self._getStats()
            logger.info("update %s" % timestamp)
            return True
        else:
            logger.debug("no changes %s" % timestamp)
            return False

    security.declarePublic("getStats")
    def getStats(self):
        """ """
        if DevelopmentMode:
            return self._getStats()
        return self.stats
    
InitializeClass(StatsTool)
registerToolInterface('portal_stats', IStatsTool)
