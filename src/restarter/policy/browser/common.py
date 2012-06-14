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

    def group_search_results(self):
        """Return search results for a query to add new groups.
        Returns an empty list. We don't want to search groups.
        """
        def search_for_principal(hunter, search_term):
            return []

        def get_principal_by_id(group_id):
            portal_groups = getToolByName(self.context, 'portal_groups')
            return portal_groups.getGroupById(group_id)

        def get_principal_title(group, _):
            return group.getGroupTitleOrName()

        return self._principal_search_results(search_for_principal,
            get_principal_by_id, get_principal_title, 'group', 'groupid')

