"""Definition of the Company content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from cioppino.twothumbs.interfaces import ILoveThumbsDontYou

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import ICompany
from restarter.policy.config import PROJECTNAME

CompanySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    CompanySchema,
    folderish=True,
    moveDiscussion=False
)


class Company(folder.ATFolder):
    """restartER company"""
    implements(ICompany, ILoveThumbsDontYou)

    meta_type = "Company"
    schema = CompanySchema


atapi.registerType(Company, PROJECTNAME)
