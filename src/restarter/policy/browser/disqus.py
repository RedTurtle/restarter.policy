# -*- coding: utf-8 -*-

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
    index = ViewPageTemplateFile("disqus_panel.pt")


class Notify(BrowserView):
    def __call__(self):
        if not self.request.method == 'POST':
            raise NotFound
        elif not self.request.URL.startswith(self.request.get('HTTP_REFERER')):
            raise NotFound
        comment_text = self.request.form.get('comment[text]')
        comment_id = self.request.form.get('comment[id]')
        objectEventNotify(DisqusNotify(self.context, comment_id, comment_text))

