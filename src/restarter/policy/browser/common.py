from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.ploneview import Plone as PloneBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ContentActionsViewlet as ContentActionsViewletBase
from plone.app.contentmenu.menu import FactoriesMenu
from plone.app.workflow.browser.sharing import SharingView as SharingBaseView
from plone.memoize.instance import memoize
from restarter.policy import policyMessageFactory as _


class ContentActionsViewlet(ContentActionsViewletBase):

    index = ViewPageTemplateFile('templates/contentactions.pt')

    def update(self):
        self.actions = FactoriesMenu(self.context).getMenuItems(self.context, self.request)

    def render(self):
        pm = getToolByName(self.context, 'portal_membership')
        if pm.checkPermission('Manage portal', self.context):
            return ''
        else:
            return self.index()


class Plone(PloneBase):

    def showEditableBorder(self):
        pm = getToolByName(self.context, 'portal_membership')
        if pm.checkPermission('Manage portal', self.context):
            return super(Plone, self).showEditableBorder()
        else:
            return False


class CompanySharingView(SharingBaseView):

    template = ViewPageTemplateFile('templates/sharing.pt')

    @memoize
    def roles(self):
        return [{'id': 'Employee', 'title':_('Employee')}]

    @memoize
    def existing_role_settings(self):
        old = super(CompanySharingView, self).existing_role_settings()
        return [a for a in old if a['id']!='AuthenticatedUsers']
