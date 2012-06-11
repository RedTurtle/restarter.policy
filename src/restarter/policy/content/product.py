"""Definition of the Product content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import IProduct, ICompany
from restarter.policy.config import PROJECTNAME

ProductSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ProductSchema,
    folderish=True,
    moveDiscussion=False
)


class Product(folder.ATFolder):
    """Product that can be bought"""
    implements(IProduct)

    meta_type = "Product"
    schema = ProductSchema

    def getCompany(self):
        company = self.aq_parent.aq_parent
        if ICompany.providedBy(company):
            return company


atapi.registerType(Product, PROJECTNAME)
