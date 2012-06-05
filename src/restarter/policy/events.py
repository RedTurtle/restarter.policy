import requests
import logging
#from Products.CMFCore.utils import getToolByName


NOTIFY = 'http://localhost:6543'
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
