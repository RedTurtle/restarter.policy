"""Definition of the Company content type
"""

from zope.interface import implements
from zope.annotation.interfaces import IAnnotations, IAnnotatable
from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName
from Products.validation.validators.ExpressionValidator import ExpressionValidator
from Products.validation.validators.RegexValidator import RegexValidator
from Products.validation.validators.BaseValidators import protocols
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from plone.indexer.decorator import indexer
from cioppino.twothumbs.interfaces import ILoveThumbsDontYou
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.interfaces import ILeadImageable

from restarter.policy import policyMessageFactory as _
from restarter.policy.interfaces import ICompany
from restarter.policy.config import PROJECTNAME
from zope.component.event import objectEventNotify
from restarter.policy.events import CompanyShareNotify


PROVINCE = atapi.DisplayList((
             ("", _("-- not selected --")),
             ("Bologna", "Bologna"),
             ("Ferrara", "Ferrara"),
             ("Forli-Cesena", "Forli-Cesena"),
             ("Modena", "Modena"),
             ("Parma", "Parma"),
             ("Piacenza", "Piacenza"),
             ("Ravenna", "Ravenna"),
             ("Reggio Emilia", "Reggio Emilia"),
             ("Rimini", "Rimini")))


NOTIFICATION = atapi.DisplayList((
             ("", _("-- not selected --")),
             ("phone", "SMS"),
             ("email", "email"),
             ("both", _(u"both"))))


CompanySchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.TextField('ragione_sociale',
        required=True,
        widget=atapi.StringWidget(
                    label=_(u'label_ragione_sociale', default=u'Ragione sociale'),
                    description=_(u'help_ragione_sociale',
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
        validators=(RegexValidator('isItalianCellPhone', r'^\+39\d*$', title='', description='', errormsg=_('Cell phone has a wrong format. The proper is +391234567890')),),
        widget=atapi.StringWidget(
            label=_("Cell phone"),
            description=_("Please give us your company cell phone."),
            size=40
            ),
        ),

    atapi.StringField('website',
        searchable=0,
        required=False,
        validators=(RegexValidator('isWebsite', r'(?i)(%s)s?://[^\s\r\n]+' % '|'.join(protocols), title='', description='', errormsg=_('It is not a proper website URL.')),),
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
        validators=(ExpressionValidator('python: bool(value)', errormsg=_('You must accept the Terms of Use.')),),
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


EMPLOYEES_KEY = 'company_employees'


@indexer(ICompany)
def company_employees(object):
    return object.company_employees


@indexer(ICompany)
def city(object):
    return object.getCity()


@indexer(ICompany)
def province(object):
    return object.getProvince()


@indexer(ICompany)
def company_type(object):
    return object.getCompany_type()


@indexer(ICompany)
def company_sectore(object):
    return object.getCompany_sectore()


class Company(folder.ATFolder):
    """restartER company"""
    implements(ICompany, ILoveThumbsDontYou, IAnnotatable, ILeadImageable)

    meta_type = "Company"
    schema = CompanySchema

    def gmap_address(self):
        """Return google map address"""
        return '%s, %s, %s, Italy' % (self.getAddress(),
                                      self.getCity(),
                                      self.getProvince())

    @property
    def company_employees(self):
        anotations = IAnnotations(self)
        if not EMPLOYEES_KEY in anotations:
            anotations[EMPLOYEES_KEY] = []
        return anotations[EMPLOYEES_KEY]

    def manage_setLocalRoles(self, user_id, roles):
        super(Company, self).manage_setLocalRoles(user_id, roles)
        if 'Employee' in roles:
            self.company_employees.append(user_id)
            objectEventNotify(CompanyShareNotify(self, user_id))

    def manage_delLocalRoles(self, userids=[]):
        for user_id in userids:
            try:
                self.company_employees.remove(user_id)
            except ValueError:
                pass
            objectEventNotify(CompanyShareNotify(self, user_id, add_user=False))
        super(Company, self).manage_delLocalRoles(userids=userids)

    def hasContentLeadImage(self):
        field = self.getField(IMAGE_FIELD_NAME)
        if field is not None:
            value = field.get(self)
            return not not value

    def setCity(self, value, **kwargs):
        if value:
            value = value.title()
        self.getField('city').set(self, value, **kwargs)

    def setWebsite(self, value, **kwargs):
        if value:
            value = value.lower()
        self.getField('website').set(self, value, **kwargs)

    def CreatorFullname(self):
        creator = self.Creator()
        membership = getToolByName(self, 'portal_membership')
        author = membership.getMemberInfo(creator)
        return author and author['fullname'] or creator


atapi.registerType(Company, PROJECTNAME)
