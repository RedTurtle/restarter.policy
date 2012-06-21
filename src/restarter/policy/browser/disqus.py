# -*- coding: utf-8 -*-
import urllib

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.interfaces import NotFound
from zope.component.event import objectEventNotify

from collective.disqus.viewlets.content import DisqusViewlet as ViewletBase
from restarter.policy.events import DisqusNotify


class DisqusViewlet(ViewletBase):
    """
    Viewlet that for DISQUS comment system.
    """
    index = ViewPageTemplateFile("templates/disqus_panel.pt")

    @property
    def authenticated_email(self):
        user = self.context.portal_membership.getAuthenticatedMember()
        if user:
            return urllib.quote(user.getProperty('email',''))
        else:
            return ''

    @property
    def authenticated_fullname(self):
        user = self.context.portal_membership.getAuthenticatedMember()
        if user:
            return user.getProperty('fullname')
        else:
            return ''


class DisqusOfferViewlet(DisqusViewlet):

    def update(self):
        super(DisqusOfferViewlet, self).update()
        wtool = self.context.portal_workflow
        self.is_discussion_allowed = wtool.getInfoFor(self.context, 'review_state', '') == 'published'


class DisqusDemandViewlet(DisqusViewlet):

    def update(self):
        super(DisqusDemandViewlet, self).update()
        wtool = self.context.portal_workflow
        self.is_discussion_allowed = wtool.getInfoFor(self.context, 'review_state', '') == 'published'


class Notify(BrowserView):
    def __call__(self):
        if not self.request.method == 'POST':
            raise NotFound(self, 'disqus-not-found')
        elif not self.request.URL.startswith(self.request.get('HTTP_REFERER')):
            raise NotFound(self, 'disqus-not-found')
        comment_text = self.request.form.get('comment[text]')
        comment_id = self.request.form.get('comment[id]')
        objectEventNotify(DisqusNotify(self.context, comment_id, comment_text))

