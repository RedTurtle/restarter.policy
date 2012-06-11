import requests
import logging
import re

from zope.interface import implements
from zope.component.interfaces import ObjectEvent
from restarter.policy.interfaces import IDisqusNotify
from restarter.policy import policyMessageFactory as _


NOTIFY = 'http://localhost:9441'
TIMEOUT = 2
NEW_ORDER = _('You have a new order in your company products:')
NEW_COMPANY = _('You have just registered new company.')
NEW_USER_MAIL = _('has just registered on FacciamoAdesso. Join us!')
NEW_USER_SMS = _('has just registered on FacciamoAdesso. Join us!')
logger = logging.getLogger('restarter.policy')



class DisqusNotify(ObjectEvent):
    implements(IDisqusNotify)

    def __init__(self, object, comment_id, comment_text):
        self.object = object
        self.comment_id = comment_id
        self.comment_text = comment_text


def notify(endpoint, params):
    """Notify restarter.notify."""
    try:
        requests.post('%s/%s' % (NOTIFY, endpoint), params=params, timeout=TIMEOUT)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        logger.exception('Encountered an error while handling %s notification' % params)


def order_added(order, event):
    """Every time an order is created - notify company."""
    if event.action != 'request':
        return
    company = order.getCompany()
    if not company:
        return

    #BBB: finish notification (email)
    params = {'message': '%s %s' % (NEW_ORDER, company.absolute_url()),
              'email': u'andrew@mleczko.net'}
    notify('notify', params)

    #BBB: finish notification (phone)
    params = {'message': '%s %s' % (NEW_ORDER, company.absolute_url()),
              'phone': '+3933475345434'}
    notify('notify', params)


def company_added(company, event):
    """Every time a company is added - create substructure."""
    products = company[company.invokeFactory('Products','prodotti')]
    products.setTitle(u'Prodotti')
    media = company[company.invokeFactory('Folder','media')]
    media.setTitle(u'Media')
    company.portal_workflow.doActionFor(media, "publish",comment=_("Published on company creation"))

    member = company.portal_membership.getAuthenticatedMember()
    params = {'message': NEW_COMPANY,
              'email': member.getProperty('email')}
    notify('notify', params)

def company_commented(company, event):
    """Event fired when company has been commented."""
    #BBB: finish notification
    print 'Notify %s for comment: %s' % (company.absolute_url(), event.comment_text)


def get_facebook_from_member(member):
    rpxs = member.getProperty('rpx_identifier', '')
    pattern = re.compile('.*facebook.com/profile.php\?id=(?P<id>.*)')
    for rpx in rpxs:
        match = pattern.match(rpx)
        if match:
            return match.group('id')


def user_created(member, event):
    """Event fired when new user has been registered."""
    facebook_id = get_facebook_from_member(member)
    if facebook_id:
        params = {'facebook_id': facebook_id}
        notify('notify/fb/register', params)

    email = member.getProperty('email', '')
    if email:
        params = {'message': NEW_USER_MAIL,
                  'email': email}
        notify('notify', params)

    phone = member.getProperty('cellphone', '')
    if phone:
        params = {'message': NEW_USER_SMS,
                  'phone': phone}
        notify('notify', params)


