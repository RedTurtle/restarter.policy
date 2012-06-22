import datetime
import logging

from collections import Counter
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
        stats = {}
        stats['products'] = self.__add__products__stats__()
        stats['total_products'] = self.__add__total_products__stats__()
        stats['last_update'] = getattr(self, 'last_update', -1)
        stats['last_uptime'] = datetime.datetime.now()
        return stats

    def __add__total_products__stats__(self):
        catalog = getToolByName(self, 'portal_catalog')
        accepted = catalog.unrestrictedSearchResults(portal_type='Order', review_state='accepted')
        return sum([a.order_value for a in accepted])

    def __add__products__stats__(self):
        """
        The structure:
        {'23457384sdf8s6f7s': {'order_value' : {'new': 54.4, 'rejected': 23.2},
                               'order_items' : {'draft': 12.1, 'rejected': 43.2}
                               }
        }
        """
        catalog = getToolByName(self, 'portal_catalog')
        stats = {}
        products = catalog.unrestrictedSearchResults(portal_type='Product')
        order_brains = catalog.unrestrictedSearchResults(portal_type='Order')
        orders_totals = [('/'.join(a.getPath().split('/')[:-1]), a.review_state, a.order_value, a.order_items) for a in order_brains]
        orders = {}
        for product_path, review_state, order_value, order_items in orders_totals:
            if product_path not in orders:
                orders[product_path] = {'order_value': Counter(),
                                        'order_items': Counter()}
            orders[product_path]['order_value'][review_state] += order_value
            orders[product_path]['order_items'][review_state] += order_items

        for product in products:
            stats[product.UID] = {'order_value': {},
                                  'order_items': {}}
            product_orders = orders.get(product.getPath())
            if product_orders:
                stats[product.UID]['order_value'] = dict(product_orders['order_value'])
                stats[product.UID]['order_items'] = dict(product_orders['order_items'])

        return stats

    security.declarePrivate("update")
    def update(self):
        """Update link status."""
        counter = getToolByName(self, 'portal_catalog').getCounter()
        # now = datetime.datetime.now()
        # timestamp = int(time.mktime(now.timetuple()))
        if counter > getattr(self, 'last_update', -1):
            self.last_update = counter
            self.stats = self._getStats()
            logger.info("update")
            return True
        else:
            logger.debug("no changes")
            return False

    security.declarePublic("getStats")
    def getStats(self):
        """ """
        if DevelopmentMode:
            return self._getStats()
        return self.stats

InitializeClass(StatsTool)
registerToolInterface('portal_stats', IStatsTool)
