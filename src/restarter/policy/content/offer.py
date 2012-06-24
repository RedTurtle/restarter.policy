"""Definition of the Offer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.validation.validators.ExpressionValidator import ExpressionValidator
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary

from restarter.policy import policyMessageFactory as _
from restarter.policy.interfaces import IOffer
from restarter.policy.config import PROJECTNAME


OfferSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField('category',
        searchable=0,
        required=True,
        vocabulary=NamedVocabulary('demand_category'),
        widget=atapi.SelectionWidget(
            label=_("Offer category"),
            description=_("Please select your offer category."),
            size=30
            ),
        ),

    atapi.StringField('period',
        searchable=0,
        required=False,
        widget=atapi.StringWidget(
            label=_("Period"),
            description=_("Please provide offer period."),
            size=20
            ),
        ),

    atapi.BooleanField('gratis',
        searchable=0,
        required=True,
        validators=(ExpressionValidator('python: bool(value)', errormsg=_('You must accept the gratis terms.')),),
        widget=atapi.BooleanWidget(
            label=_("This offer is free of charge."),
            description=_("Please accept that this offer is free of charge."),
            size=30
            ),
        ),

))


schemata.finalizeATCTSchema(OfferSchema, moveDiscussion=False)

OfferSchema['location'].widget.visible['view'] = 'invisible'
OfferSchema['location'].widget.visible['edit'] = 'invisible'
OfferSchema['language'].widget.visible['view'] = 'invisible'
OfferSchema['language'].widget.visible['edit'] = 'invisible'
OfferSchema['allowDiscussion'].widget.visible['view'] = 'invisible'
OfferSchema['allowDiscussion'].widget.visible['edit'] = 'invisible'
OfferSchema['contributors'].widget.visible['view'] = 'invisible'
OfferSchema['contributors'].widget.visible['edit'] = 'invisible'
OfferSchema['creators'].widget.visible['view'] = 'invisible'
OfferSchema['creators'].widget.visible['edit'] = 'invisible'
OfferSchema['effectiveDate'].widget.visible['view'] = 'invisible'
OfferSchema['effectiveDate'].widget.visible['edit'] = 'invisible'
OfferSchema['expirationDate'].widget.visible['view'] = 'invisible'
OfferSchema['expirationDate'].widget.visible['edit'] = 'invisible'
OfferSchema['rights'].widget.visible['view'] = 'invisible'
OfferSchema['rights'].widget.visible['edit'] = 'invisible'
OfferSchema['excludeFromNav'].widget.visible['view'] = 'invisible'
OfferSchema['excludeFromNav'].widget.visible['edit'] = 'invisible'
OfferSchema['subject'].widget.visible['view'] = 'invisible'
OfferSchema['subject'].widget.visible['edit'] = 'invisible'
OfferSchema['relatedItems'].widget.visible['view'] = 'invisible'
OfferSchema['relatedItems'].widget.visible['edit'] = 'invisible'
OfferSchema['title'].widget.label = _('Offer name')


class Offer(base.ATCTContent):
    """An offer"""
    implements(IOffer)

    meta_type = "Offer"
    schema = OfferSchema


atapi.registerType(Offer, PROJECTNAME)
