"""Definition of the Companies content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import ICompanies
from restarter.policy.config import PROJECTNAME

CompaniesSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    CompaniesSchema,
    folderish=True,
    moveDiscussion=False
)


class Companies(folder.ATFolder):
    """Folder that contains companies"""
    implements(ICompanies)

    meta_type = "Companies"
    schema = CompaniesSchema


atapi.registerType(Companies, PROJECTNAME)
