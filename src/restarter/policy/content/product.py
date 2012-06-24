"""Definition of the Product content type
"""

from zope.interface import implements
from plone.indexer.decorator import indexer

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.interfaces import ILeadImageable

from restarter.policy.interfaces import IProduct, ICompany
from restarter.policy.config import PROJECTNAME
from restarter.policy import policyMessageFactory as _


PRODUCT_CONDITION = atapi.DisplayList((
             ("", _("-- not selected --")),
             ("new", _("New")),
             ("new_demaged", _("New demaged")),
             ("used", _("Used")),
             ("used_demaged", _("Used dameged")),
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
            label=_("Product quantity"),
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
            description=_("Please provide product price."),
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

    atapi.TextField('shipment',
        searchable=0,
        required=True,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        widget=atapi.TextAreaWidget(
            label=_("Shipment"),
            description=_("Please provide product shipment conditions."),
            ),
        ),

    atapi.TextField('waranty',
        searchable=0,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
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
ProductSchema.moveField('subject', after='category')


@indexer(IProduct)
def product_category(object):
    return object.getCategory()


@indexer(IProduct)
def city(object):
    company = object.getCompany()
    if company:
        return company.getCity()


@indexer(IProduct)
def province(object):
    company = object.getCompany()
    if company:
        return company.getProvince()


@indexer(IProduct)
def company_sectore(object):
    company = object.getCompany()
    if company:
        return company.getCompany_sectore()


@indexer(IProduct)
def product_price(object):
    return object.getPrice()


class Product(folder.ATFolder):
    """Product that can be bought"""
    implements(IProduct, ILeadImageable)

    meta_type = "Product"
    schema = ProductSchema

    def getCompany(self):
        company = self.aq_parent.aq_parent
        if ICompany.providedBy(company):
            return company

    def showNewOrderButton(self):
        wtool = self.portal_workflow
        return wtool.getInfoFor(self, 'review_state', '') == 'published'

    def hasContentLeadImage(self):
        field = self.getField(IMAGE_FIELD_NAME)
        if field is not None:
            value = field.get(self)
            return not not value


atapi.registerType(Product, PROJECTNAME)
