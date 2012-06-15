"""Definition of the Offers content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import IOffers
from restarter.policy.config import PROJECTNAME

OffersSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    OffersSchema,
    folderish=True,
    moveDiscussion=False
)


class Offers(folder.ATFolder):
    """Folder that contains companies"""
    implements(IOffers)

    meta_type = "Offers"
    schema = OffersSchema


atapi.registerType(Offers, PROJECTNAME)
