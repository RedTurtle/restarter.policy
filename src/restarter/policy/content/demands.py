"""Definition of the Demands content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import IDemands
from restarter.policy.config import PROJECTNAME

DemandsSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    DemandsSchema,
    folderish=True,
    moveDiscussion=False
)


class Demands(folder.ATFolder):
    """Folder that contains products"""
    implements(IDemands)

    meta_type = "Demands"
    schema = DemandsSchema


atapi.registerType(Demands, PROJECTNAME)
