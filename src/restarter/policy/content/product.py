"""Definition of the Product content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import IProduct, ICompany
from restarter.policy.config import PROJECTNAME
from restarter.policy import policyMessageFactory as _


PRODUCT_CONDITION = atapi.DisplayList((
             ("",_("-- not selected --")),
             ("new", "New"),
             ("used", "Used"),
             ("other", _(u"Other"))))


ProductSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('category',
        searchable=0,
        required=True,
        vocabulary=NamedVocabulary('product_category'),
        widget=atapi.SelectionWidget(
            label=_("Product category"),
            description=_("Please select your product category."),
            size=30
            ),
        ),

    atapi.FixedPointField('quantity',
        searchable=0,
        required=True,
        widget=atapi.DecimalWidget(
            label=_("Quantity"),
            description=_("Please provide product quantity."),
            size=5
            ),
        ),

    atapi.StringField('unit',
        searchable=0,
        required=True,
        widget=atapi.StringWidget(
            label=_("Quantity unit"),
            description=_("Please provide product quantity unit."),
            size=10
            ),
        ),

    atapi.FixedPointField('price',
        searchable=0,
        required=True,
        widget=atapi.DecimalWidget(
            label=_("Price"),
            description=_("Please provide product quantity."),
            size=15
            ),
        ),

    atapi.StringField('product_condition',
        searchable=0,
        required=False,
        vocabulary=PRODUCT_CONDITION,
        widget=atapi.SelectionWidget(
            label=_("Product condition"),
            description=_("Please provide product condition state."),
            size=10
            ),
        ),

    atapi.StringField('availability',
        searchable=0,
        required=False,
        widget=atapi.StringWidget(
            label=_("Availability"),
            description=_("Please provide product availability."),
            size=20
            ),
        ),

    atapi.TextField('shipment',
        searchable=0,
        required=False,
        widget=atapi.TextAreaWidget(
            label=_("Shipment"),
            description=_("Please provide product shipment conditions."),
            ),
        ),

    atapi.TextField('waranty',
        searchable=0,
        required=False,
        widget=atapi.TextAreaWidget(
            label=_("Waranty"),
            description=_("Please provide product waranty conditions."),
            ),
        ),



))

ProductSchema['location'].widget.visible['view'] = 'invisible'
ProductSchema['location'].widget.visible['edit'] = 'invisible'
ProductSchema['language'].widget.visible['view'] = 'invisible'
ProductSchema['language'].widget.visible['edit'] = 'invisible'
ProductSchema['allowDiscussion'].widget.visible['view'] = 'invisible'
ProductSchema['allowDiscussion'].widget.visible['edit'] = 'invisible'
ProductSchema['contributors'].widget.visible['view'] = 'invisible'
ProductSchema['contributors'].widget.visible['edit'] = 'invisible'
ProductSchema['creators'].widget.visible['view'] = 'invisible'
ProductSchema['creators'].widget.visible['edit'] = 'invisible'
ProductSchema['effectiveDate'].widget.visible['view'] = 'invisible'
ProductSchema['effectiveDate'].widget.visible['edit'] = 'invisible'
ProductSchema['expirationDate'].widget.visible['view'] = 'invisible'
ProductSchema['expirationDate'].widget.visible['edit'] = 'invisible'
ProductSchema['rights'].widget.visible['view'] = 'invisible'
ProductSchema['rights'].widget.visible['edit'] = 'invisible'
ProductSchema['nextPreviousEnabled'].widget.visible['view'] = 'invisible'
ProductSchema['nextPreviousEnabled'].widget.visible['edit'] = 'invisible'
ProductSchema['excludeFromNav'].widget.visible['view'] = 'invisible'
ProductSchema['excludeFromNav'].widget.visible['edit'] = 'invisible'
ProductSchema['title'].widget.label = _('Product name')


schemata.finalizeATCTSchema(
    ProductSchema,
    folderish=True,
    moveDiscussion=False
)
ProductSchema.changeSchemataForField('subject', 'default')


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
