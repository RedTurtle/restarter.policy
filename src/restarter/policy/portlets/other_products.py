from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from restarter.policy.interfaces import IProduct


class IOtherProducts(IPortletDataProvider):
    """A portlet which shows other product from the same company
    """


class Assignment(base.Assignment):
    implements(IOtherProducts)

    title = u'Other products'


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('other_products.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

    def show(self):
        return IProduct.providedBy(self.context)

    @property
    def available(self):
        return self.show()

    def update(self):
        company = self.context.aq_inner.getCompany()
        company_path = company.absolute_url_path()
        self.products = self.context.getFolderContents({'portal_type':'Product',
                                                        'path': '%s/prodotti' % company_path},
                                                         b_size=10)
        self.company_title = company.title_or_id()
        self.products_url = '%s/prodotti' % company.absolute_url()


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()

