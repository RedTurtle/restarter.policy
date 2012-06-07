import requests
import logging

from zope.interface import implements
from zope.component.interfaces import ObjectEvent
from restarter.policy.interfaces import IDisqusNotify


NOTIFY = 'http://localhost:9441'
TIMEOUT = 2
MESSAGE = 'You have a new order in your company products %s.'
logger = logging.getLogger('restarter.policy')


def order_added(order, event):
    """Every time an order is created - notify company."""
    if event.action != 'request':
        return
    company = order.getCompany()
    if not company:
        return
    params = {'message': MESSAGE % company.absolute_url(),
              'phone': '+3933475345434',
              'email': u'andrew@mleczko.net'}
    try:
        requests.get('%s/notify' % NOTIFY, params=params, timeout=TIMEOUT)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        logger.exception('Encountered an error while handling %s notification' % order.absolute_url())


def company_added(company, event):
    """Every time a company is added - create substructure."""
    products = company[company.invokeFactory('Products','prodotti')]
    products.setTitle(u'Prodotti')
    media = company[company.invokeFactory('Folder','media')]
    media.setTitle(u'Media')
    company.portal_workflow.doActionFor(media,"publish",comment="Published on company creation")


def company_commented(company, event):
    print 'Notify %s for comment: %s' % (company.absolute_url, event.comment_text)


class DisqusNotify(ObjectEvent):
    implements(IDisqusNotify)

    def __init__(self, object, comment_id, comment_text):
        self.object = object
        self.comment_id = comment_id
        self.comment_text = comment_text
