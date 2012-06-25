# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn

from restarter.policy.interfaces import IRestarterConfiguration


class RestarterConfig(BrowserView):

    implements(IRestarterConfiguration)

    def showBigLogo(self):
        if IHidePloneLeftColumn.providedBy(self.context): #always show home page logos on faceted
            return True

    def isHomePage(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        path_check = portal_state.portal_url() == context_state.canonical_object_url()
        url_check = not ISiteRoot.providedBy(self.context)
        return path_check and url_check

    def safe_truncate(self, text, size):
        if len(text) > size:
            elips = '(...)'
        else:
            elips = ''
        return '%s%s' % (text[:size], elips)

    def getMemberInfo(self, memberId=None):
        # Return 'harmless' Memberinfo of any member, such as Full name,
        # Location, etc
        pm = self.context.portal_membership
        if not memberId:
            member = pm.getAuthenticatedMember()
        else:
            member = pm.getMemberById(memberId)

        if member is None:
            return None

        memberinfo = { 'fullname'    : member.getProperty('fullname'),
                       'email'       : member.getProperty('email'),
                       'cellphone'   : member.getProperty('cellphone'),
                     }

        return memberinfo
