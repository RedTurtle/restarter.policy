"""Definition of the CompanyStory content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import ICompanyStory, ICompany
from restarter.policy.config import PROJECTNAME

CompanyStorySchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(CompanyStorySchema, moveDiscussion=False)


class CompanyStory(base.ATCTContent):
    """Product's order"""
    implements(ICompanyStory)

    meta_type = "CompanyStory"
    schema = CompanyStorySchema

    def getCompany(self):
        company = self.aq_parent.aq_parent.aq_parent
        if ICompany.providedBy(company):
            return company

atapi.registerType(CompanyStory, PROJECTNAME)
