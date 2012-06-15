"""Definition of the Demand content type
"""

from zope.interface import implements
from plone.indexer.decorator import indexer

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary

from restarter.policy.interfaces import IDemand, ICompany
from restarter.policy.config import PROJECTNAME
from restarter.policy import policyMessageFactory as _


DemandSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('category',
        searchable=0,
        required=True,
        vocabulary=NamedVocabulary('demand_category'),
        widget=atapi.SelectionWidget(
            label=_("Demand category"),
            description=_("Please select your demand category."),
            size=30
            ),
        ),

    atapi.StringField('period',
        searchable=0,
        required=False,
        widget=atapi.StringWidget(
            label=_("Period"),
            description=_("Please provide demand period."),
            size=20
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


@indexer(IDemand)
def product_category(object):
    return object.getCategory()


@indexer(IDemand)
def city(object):
    company = object.getCompany()
    if company:
        return company.getCity()


@indexer(IDemand)
def province(object):
    company = object.getCompany()
    if company:
        return company.getProvince()


@indexer(IDemand)
def company_sectore(object):
    company = object.getCompany()
    if company:
        return company.getCompany_sectore()


class Demand(folder.ATFolder):
    """Demand that can be bought"""
    implements(IDemand)

    meta_type = "Demand"
    schema = DemandSchema

    def getCompany(self):
        company = self.aq_parent.aq_parent
        if ICompany.providedBy(company):
            return company


atapi.registerType(Demand, PROJECTNAME)
