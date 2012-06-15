"""Definition of the Demand content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary

# -*- Message Factory Imported Here -*-

from restarter.policy.interfaces import IDemand
from restarter.policy.config import PROJECTNAME
from restarter.policy import policyMessageFactory as _


PRODUCT_CONDITION = atapi.DisplayList((
             ("",_("-- not selected --")),
             ("new", "New"),
             ("used", "Used"),
             ("other", _(u"Other"))))


DemandSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('category',
        searchable=0,
        required=True,
        vocabulary=NamedVocabulary('product_category'),
        widget=atapi.SelectionWidget(
            label=_("Demand category"),
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
            description=_("Please provide product price."),
            size=15
            ),
        ),

    atapi.StringField('product_condition',
        searchable=0,
        required=False,
        vocabulary=PRODUCT_CONDITION,
        widget=atapi.SelectionWidget(
            label=_("Demand condition"),
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

DemandSchema['location'].widget.visible['view'] = 'invisible'
DemandSchema['location'].widget.visible['edit'] = 'invisible'
DemandSchema['language'].widget.visible['view'] = 'invisible'
DemandSchema['language'].widget.visible['edit'] = 'invisible'
DemandSchema['allowDiscussion'].widget.visible['view'] = 'invisible'
DemandSchema['allowDiscussion'].widget.visible['edit'] = 'invisible'
DemandSchema['contributors'].widget.visible['view'] = 'invisible'
DemandSchema['contributors'].widget.visible['edit'] = 'invisible'
DemandSchema['creators'].widget.visible['view'] = 'invisible'
DemandSchema['creators'].widget.visible['edit'] = 'invisible'
DemandSchema['effectiveDate'].widget.visible['view'] = 'invisible'
DemandSchema['effectiveDate'].widget.visible['edit'] = 'invisible'
DemandSchema['expirationDate'].widget.visible['view'] = 'invisible'
DemandSchema['expirationDate'].widget.visible['edit'] = 'invisible'
DemandSchema['rights'].widget.visible['view'] = 'invisible'
DemandSchema['rights'].widget.visible['edit'] = 'invisible'
DemandSchema['nextPreviousEnabled'].widget.visible['view'] = 'invisible'
DemandSchema['nextPreviousEnabled'].widget.visible['edit'] = 'invisible'
DemandSchema['excludeFromNav'].widget.visible['view'] = 'invisible'
DemandSchema['excludeFromNav'].widget.visible['edit'] = 'invisible'
DemandSchema['title'].widget.label = _('Demand name')


schemata.finalizeATCTSchema(
    DemandSchema,
    folderish=True,
    moveDiscussion=False
)
DemandSchema.changeSchemataForField('subject', 'default')
DemandSchema.moveField('subject', after='category')


class Demand(folder.ATFolder):
    """Demand that can be bought"""
    implements(IDemand)

    meta_type = "Demand"
    schema = DemandSchema

atapi.registerType(Demand, PROJECTNAME)
