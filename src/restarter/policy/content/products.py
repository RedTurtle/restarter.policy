"""Definition of the Products content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import IProducts
from restarter.policy.config import PROJECTNAME

ProductsSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ProductsSchema,
    folderish=True,
    moveDiscussion=False
)


class Products(folder.ATFolder):
    """Folder that contains products"""
    implements(IProducts)

    meta_type = "Products"
    schema = ProductsSchema


atapi.registerType(Products, PROJECTNAME)
