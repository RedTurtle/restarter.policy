""" Subtyping support
"""
from zope.interface import implements
from zope.interface import alsoProvides, noLongerProvides
from zope.component.event import objectEventNotify

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from plone.app.layout.viewlets.common import ViewletBase

from restarter.policy.interfaces import IHomeStoriesSubtyper, IHomeStory, ICompanyStory
from restarter.policy import policyMessageFactory as _
from restarter.policy.events import HomepageStoryNotify


class HomeStoriesSubtyper(BrowserView):
    """ Public support for subtyping objects
    """
    implements(IHomeStoriesSubtyper)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _redirect(self, msg=''):
        """ Redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(msg, type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    @property
    def can_enable(self):
        """ See IHomeStoriesSubtyper
        """
        return ICompanyStory.providedBy(self.context) \
               and not IHomeStory.providedBy(self.context)

    @property
    def can_disable(self):
        """ See IHomeStoriesSubtyper
        """
        return ICompanyStory.providedBy(self.context) \
               and IHomeStory.providedBy(self.context)

    def enable(self):
        """ See IHomeStoriesSubtyper
        """
        if not self.can_enable:
            return self._redirect(_('Homestory not supported'))

        alsoProvides(self.context, IHomeStory)
        self.context.reindexObject(['object_provides', ])
        objectEventNotify(HomepageStoryNotify(self.context,))
        self._redirect(_('This is now a homepage story'))

    def disable(self):
        """ See IHomeStoriesSubtyper
        """
        if not self.can_disable:
            return self._redirect(_('Homestory not supported'))

        noLongerProvides(self.context, IHomeStory)
        self.context.reindexObject(['object_provides', ])
        self._redirect(_('This is no longer a homepage story'))


class InfoViewlet(ViewletBase):
    """ View that just tells wheter the company story is marked
     as homepage """

    index = ViewPageTemplateFile('templates/homestory_info_viewlet.pt')

    def update(self):
        self.is_homepage_story = IHomeStory.providedBy(self.context)


class FacesViewlet(ViewletBase):
    """ Viewlet that displays faces in homepage """

    index = ViewPageTemplateFile('templates/viewlet_slider_top_with_faces.pt')

    def update(self):
        self.faces = self.get_faces()

    def get_faces(self):
        """Return equal 4 elements chunks"""

        pc = getToolByName(self.context, 'portal_catalog')
        faces = pc(path='/restarter/storie/facce',
                   portal_type='Link',
                   review_state='published',
                   limit=8)
        for i in xrange(0, len(faces), 4):
            yield faces[i:i+4]

