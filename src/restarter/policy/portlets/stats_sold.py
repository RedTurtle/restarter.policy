from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IStatsSoldPortlet(IPortletDataProvider):
    """A portlet which shows the stats.
    """


class Assignment(base.Assignment):
    implements(IStatsSoldPortlet)

    title = u'Stats sold'


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('stats_sold.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

    def show(self):
        return True

    def stats(self):
        return self.context.portal_stats.getStats().get('total_products',0)

    @property
    def available(self):
        return self.show()

    def update(self):
        pass


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()

