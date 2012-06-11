"""Definition of the Company content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.validation.validators.ExpressionValidator import ExpressionValidator
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from cioppino.twothumbs.interfaces import ILoveThumbsDontYou

from restarter.policy import policyMessageFactory as _
from restarter.policy.interfaces import ICompany
from restarter.policy.config import PROJECTNAME


PROVINCE = atapi.DisplayList((
             ("",_("-- not selected --")),
             ("Bologna","Bologna"),
             ("Ferrara","Ferrara"),
             ("Forli-Cesena","Forli-Cesena"),
             ("Modena","Modena"),
             ("Parma","Parma"),
             ("Piacenza","Piacenza"),
             ("Ravenna","Ravenna"),
             ("Reggio Emilia","Reggio Emilia"),
             ("Rimini","Rimini")))


NOTIFICATION = atapi.DisplayList((
             ("",_("-- not selected --")),
             ("phone", "SMS"),
             ("email", "email"),
             ("both", _(u"both"))))


CompanySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.TextField('ragione_sociale',
        required=True,
        widget = atapi.StringWidget(
                    label = _(u'label_ragione_sociale', default=u'Ragione sociale'),
                    description = _(u'help_ragione_sociale',
                                    default=u"Ragione sociale help.")),
        ),

    atapi.StringField('address',
        searchable=0,
        required=True,
        widget=atapi.StringWidget(
            label=_("Address"),
            description=_("Please give us your company address"),
            size=70
            ),
        ),

    atapi.IntegerField('cap',
        searchable=0,
        required=True,
        widget=atapi.IntegerWidget(
            label="CAP",
            size=10
            ),
        ),
    
    atapi.StringField('city',
        searchable=0,
        required=True,
        widget=atapi.StringWidget(
            label=_("City"),
            description=_("Please give us your company city location."),
            size=40
            ),
        ),

    atapi.StringField('province',
        searchable=0,
        required=True,
        vocabulary=PROVINCE,
        widget=atapi.SelectionWidget(
            label=_("Province"),
            description=_("Please give us your company province location."),
            size=30
            ),
        ),

    atapi.StringField('email',
        searchable=0,
        validators=('isEmail',),
        required=True,
        widget=atapi.StringWidget(
            label=_("Email address"),
            description=_("Please give us your company email address."),
            size=40
            ),
        ),

    atapi.StringField('cellphone',
        searchable=0,
        required=True,
        widget=atapi.StringWidget(
            label=_("Cell phone"),
            description=_("Please give us your company cell phone."),
            size=40
            ),
        ),

    atapi.StringField('website',
        searchable=0,
        required=False,
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=_("Company website"),
            description=_("Please give us your company website url."),
            size=40
            ),
        ),

    atapi.StringField('piva',
        searchable=0,
        required=True,
        widget=atapi.StringWidget(
            label=_("CF/P.IVA"),
            description=_("Please give us your company CF or P.IVA."),
            size=40
            ),
        ),

    atapi.StringField('company_type',
        searchable=0,
        required=True,
        vocabulary=NamedVocabulary('company_type'),
        widget=atapi.SelectionWidget(
            label=_("Company type"),
            description=_("Please select your company type."),
            size=30
            ),
        ),

    atapi.StringField('company_sectore',
        searchable=0,
        required=True,
        vocabulary=NamedVocabulary('company_sectore'),
        widget=atapi.SelectionWidget(
            label=_("Company sectore"),
            description=_("Please select your company sectore."),
            size=30
            ),
        ),


    atapi.BooleanField('terms_of_use',
        searchable=0,
        required=True,
        validators = (ExpressionValidator('python: bool(value)', errormsg=_('You must accept the Terms of Use.')),),
        widget=atapi.BooleanWidget(
            label=_("Accept terms of use"),
            description=_("Please accept terms of use."),
            size=30
            ),
        ),

    atapi.StringField('notification',
        searchable=0,
        vocabulary=NOTIFICATION,
        required=True,
        widget=atapi.SelectionWidget(
            label=_("Notification type"),
            description=_("Please select how we should notify your company."),
            size=30
            ),
        ),


))


schemata.finalizeATCTSchema(
    CompanySchema,
    folderish=True,
    moveDiscussion=False
)

CompanySchema['subject'].widget.visible['view'] = 'invisible'
CompanySchema['subject'].widget.visible['edit'] = 'invisible'
CompanySchema['location'].widget.visible['view'] = 'invisible'
CompanySchema['location'].widget.visible['edit'] = 'invisible'
CompanySchema['language'].widget.visible['view'] = 'invisible'
CompanySchema['language'].widget.visible['edit'] = 'invisible'
CompanySchema['allowDiscussion'].widget.visible['view'] = 'invisible'
CompanySchema['allowDiscussion'].widget.visible['edit'] = 'invisible'
CompanySchema['contributors'].widget.visible['view'] = 'invisible'
CompanySchema['contributors'].widget.visible['edit'] = 'invisible'
CompanySchema['creators'].widget.visible['view'] = 'invisible'
CompanySchema['creators'].widget.visible['edit'] = 'invisible'
CompanySchema['effectiveDate'].widget.visible['view'] = 'invisible'
CompanySchema['effectiveDate'].widget.visible['edit'] = 'invisible'
CompanySchema['expirationDate'].widget.visible['view'] = 'invisible'
CompanySchema['expirationDate'].widget.visible['edit'] = 'invisible'
CompanySchema['rights'].widget.visible['view'] = 'invisible'
CompanySchema['rights'].widget.visible['edit'] = 'invisible'
CompanySchema['nextPreviousEnabled'].widget.visible['view'] = 'invisible'
CompanySchema['nextPreviousEnabled'].widget.visible['edit'] = 'invisible'
CompanySchema['excludeFromNav'].widget.visible['view'] = 'invisible'
CompanySchema['excludeFromNav'].widget.visible['edit'] = 'invisible'
CompanySchema['title'].widget.label = _('Company name')
CompanySchema['description'].widget.maxlength = 200


class Company(folder.ATFolder):
    """restartER company"""
    implements(ICompany, ILoveThumbsDontYou)

    meta_type = "Company"
    schema = CompanySchema


atapi.registerType(Company, PROJECTNAME)
