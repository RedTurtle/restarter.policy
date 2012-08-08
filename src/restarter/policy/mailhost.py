# -*- coding: utf-8 -*-

from zope.interface import implements
from copy import deepcopy
from email import message_from_string
from email.Message import Message

from Products.MailHost.interfaces import IMailHost
from restarter.policy.events import notify


class CeleryMailHost(object):

    implements(IMailHost)

    def getId(self):
        return 'MailHost'

    def send(self,
             messageText,
             mto=None,
             mfrom=None,
             subject=None,
             encode=None,
             immediate=False,
             charset=None,
             msg_type=None,
            ):

        if isinstance(messageText, Message):
           # We already have a message, make a copy to operate on
           mo = deepcopy(messageText)
        else:
           # Otherwise parse the input message
           mo = message_from_string(messageText)

        subject = subject or mo['Subject'] or ''
        body = mo._payload
        mto = mto or mo['To']

        params = {'email_message': body,
                  'email_subject': subject,
                  'email': mto}
        notify('notify', params)
