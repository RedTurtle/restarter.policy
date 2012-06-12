# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter

from restarter.policy.interfaces import IRestarterConfiguration


class RestarterConfig(BrowserView):

    implements(IRestarterConfiguration)

    def isHomePage(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        return portal_state.portal_url() == context_state.canonical_object_url()
