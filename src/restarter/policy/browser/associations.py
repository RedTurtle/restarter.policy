from zope.annotation.interfaces import IAnnotations
from plone.app.layout.viewlets.common import ViewletBase, BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from restarter.policy import policyMessageFactory as _

ASSOCIATION_KEY = 'restarter.associations'


class ManageViewlet(ViewletBase):
    "Viewlet that manages the association toggle"

    index = ViewPageTemplateFile('templates/manage_association_viewlet.pt')

    def update(self):
        membership = getToolByName(self.context, 'portal_membership')
        self.username = membership.getAuthenticatedMember().getProperty('fullname')


class ListViewlet(ViewletBase):
    "View that just list the associated associations"

    index = ViewPageTemplateFile('templates/list_association_viewlet.pt')

    def update(self):
        annotations = IAnnotations(self.context)
        if not ASSOCIATION_KEY in annotations:
            annotations[ASSOCIATION_KEY] = []
        self.associations = annotations[ASSOCIATION_KEY]


class AssocAproveToogle(BrowserView):
    "BrowserView that handles the toggle"

    def __call__(self):
        annotations = IAnnotations(self.context)
        if not ASSOCIATION_KEY in annotations:
            annotations[ASSOCIATION_KEY] = []
        associated = annotations[ASSOCIATION_KEY]

        membership = getToolByName(self.context, 'portal_membership')
        member = membership.getAuthenticatedMember()
        if member.getId() in associated:
            associated.remove(member.getId())
            IStatusMessage(self.request).addStatusMessage(_(u"Association removed."))
        else:
            IStatusMessage(self.request).addStatusMessage(_(u"Association added."))
            associated.append(member.getId())

        annotations[ASSOCIATION_KEY] = associated
        self.request.response.redirect(self.context.absolute_url())
