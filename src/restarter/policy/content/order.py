"""Definition of the Order content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from restarter.policy import policyMessageFactory as _
from restarter.policy.interfaces import IOrder, ICompany, IProduct
from restarter.policy.config import PROJECTNAME

OrderSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.FixedPointField('quantity',
        searchable=0,
        required=True,
        widget=atapi.DecimalWidget(
            label=_("Quantity"),
            description=_("Please provide order quantity."),
            size=10
            ),
        ),

))


schemata.finalizeATCTSchema(OrderSchema, moveDiscussion=False)

OrderSchema['location'].widget.visible['view'] = 'invisible'
OrderSchema['location'].widget.visible['edit'] = 'invisible'
OrderSchema['language'].widget.visible['view'] = 'invisible'
OrderSchema['language'].widget.visible['edit'] = 'invisible'
OrderSchema['allowDiscussion'].widget.visible['view'] = 'invisible'
OrderSchema['allowDiscussion'].widget.visible['edit'] = 'invisible'
OrderSchema['contributors'].widget.visible['view'] = 'invisible'
OrderSchema['contributors'].widget.visible['edit'] = 'invisible'
OrderSchema['creators'].widget.visible['view'] = 'invisible'
OrderSchema['creators'].widget.visible['edit'] = 'invisible'
OrderSchema['effectiveDate'].widget.visible['view'] = 'invisible'
OrderSchema['effectiveDate'].widget.visible['edit'] = 'invisible'
OrderSchema['expirationDate'].widget.visible['view'] = 'invisible'
OrderSchema['expirationDate'].widget.visible['edit'] = 'invisible'
OrderSchema['rights'].widget.visible['view'] = 'invisible'
OrderSchema['rights'].widget.visible['edit'] = 'invisible'
OrderSchema['excludeFromNav'].widget.visible['view'] = 'invisible'
OrderSchema['excludeFromNav'].widget.visible['edit'] = 'invisible'
OrderSchema['title'].widget.visible['view'] = 'visible'
OrderSchema['title'].widget.visible['edit'] = 'invisible'
OrderSchema['subject'].widget.visible['view'] = 'invisible'
OrderSchema['subject'].widget.visible['edit'] = 'invisible'
OrderSchema['relatedItems'].widget.visible['view'] = 'invisible'
OrderSchema['relatedItems'].widget.visible['edit'] = 'invisible'
OrderSchema['description'].widget.label = _('Order comment')
OrderSchema['description'].widget.description = _('Leave your comment for this order.')

OrderSchema.moveField('quantity', before='description')

class Order(base.ATCTContent):
    """Product's order"""
    implements(IOrder)

    meta_type = "Order"
    schema = OrderSchema

    def getProduct(self):
        product = self.aq_parent
        if IProduct.providedBy(product):
            return product

    def getCompany(self):
        company = self.aq_parent.aq_parent.aq_parent
        if ICompany.providedBy(company):
            return company


atapi.registerType(Order, PROJECTNAME)
