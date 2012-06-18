import json
import operator

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProductCategoriesPortlet(IPortletDataProvider):
    """A portlet which shows product categories with links to faceted.
    """


class Assignment(base.Assignment):
    implements(IProductCategoriesPortlet)

    title = u'Product categories'


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('product_categories.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

    def show(self):
        return True

    @property
    def available(self):
        return self.show()

    def update(self):
        portal = self.context.portal_url.getPortalObject()
        counter = portal.unrestrictedTraverse('prodotti/@@faceted_counter')
        org_header = self.request.response.getHeader('content-type')
        criteria = counter(cid='c5')
        #faceted force json content-type!!!
        self.request.response.setHeader('content-type', org_header)
        results = json.loads(criteria).items()
        results.sort(key=operator.itemgetter(1))
        results.reverse()

        atvm = portal.portal_vocabularies
        vocabs = atvm.getVocabularyByName('product_category')
        self.categories = []

        for n, result in enumerate(results):
            k, count = result
            if n == 10:
                break
            if count == 0:
                break
            vocab = vocabs.get(k)
            if vocab:
                self.categories.append((vocab.title, k, count))


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()

