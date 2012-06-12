from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.ploneview import Plone as PloneBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ContentActionsViewlet as ContentActionsViewletBase
from plone.app.contentmenu.menu import FactoriesMenu


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
