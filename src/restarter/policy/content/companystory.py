"""Definition of the CompanyStory content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata, document

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import ICompanyStory
from restarter.policy.config import PROJECTNAME

CompanyStorySchema = document.ATDocumentSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(CompanyStorySchema, moveDiscussion=False)


class CompanyStory(base.ATCTContent):
    """Product's order"""
    implements(ICompanyStory)

    meta_type = "CompanyStory"
    schema = CompanyStorySchema

atapi.registerType(CompanyStory, PROJECTNAME)
