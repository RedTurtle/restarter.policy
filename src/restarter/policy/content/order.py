"""Definition of the Order content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import IOrder, ICompany
from restarter.policy.config import PROJECTNAME

OrderSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(OrderSchema, moveDiscussion=False)


class Order(base.ATCTContent):
    """Product's order"""
    implements(IOrder)

    meta_type = "Order"
    schema = OrderSchema

    def getCompany(self):
        company = self.aq_parent.aq_parent.aq_parent
        if ICompany.providedBy(company):
            return company

atapi.registerType(Order, PROJECTNAME)
