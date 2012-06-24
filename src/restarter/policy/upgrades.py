from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from StringIO import StringIO
from plugin import FacebookUsers


PROFILE_ID='profile-restarter.policy:default'


def add_employee_idx(context):
    catalog = getToolByName(context, 'portal_catalog')
    catalog.addIndex('company_employees', 'KeywordIndex')


def add_company_idx(context):
    catalog = getToolByName(context, 'portal_catalog')
    catalog.addIndex('city', 'FieldIndex')
    catalog.addIndex('province', 'KeywordIndex')
    catalog.addIndex('product_category', 'KeywordIndex')
    catalog.addIndex('company_type', 'KeywordIndex')
    catalog.addIndex('company_sectore', 'KeywordIndex')


def setupInitialStructure(portal):
    if 'aziende' not in portal.objectIds() and 'Aziende' not in portal.objectIds():
        companies = portal[portal.invokeFactory('Companies','aziende')]
        companies.setTitle(u'Aziende')
    if 'notizie' not in portal.objectIds() and 'Notizie' not in portal.objectIds():
        companies = portal[portal.invokeFactory('Folder','notizie')]
        companies.setTitle(u'Notizie')
    if 'il-progetto' not in portal.objectIds():
        companies = portal[portal.invokeFactory('Folder','il-progetto')]
        companies.setTitle(u'Il progetto')
    if 'storie' not in portal.objectIds():
        companies = portal[portal.invokeFactory('Folder','storie')]
        companies.setTitle(u'Storie')
    if 'contatti' not in portal.objectIds():
        companies = portal[portal.invokeFactory('Folder','contatti')]
        companies.setTitle(u'Contatti')

    if 'portal_vocabularies' in portal.objectIds():
        if 'company_type' not in portal.portal_vocabularies.objectIds():
            company_type = portal.portal_vocabularies[portal.portal_vocabularies.invokeFactory('SortedSimpleVocabulary','company_type')]
            company_type.setTitle(u'Company type')
        if 'company_sectore' not in portal.portal_vocabularies.objectIds():
            company_sectore = portal.portal_vocabularies[portal.portal_vocabularies.invokeFactory('SortedSimpleVocabulary','company_sectore')]
            company_sectore.setTitle(u'Company sectore')
        if 'product_category' not in portal.portal_vocabularies.objectIds():
            product_category = portal.portal_vocabularies[portal.portal_vocabularies.invokeFactory('SortedSimpleVocabulary','product_category')]
            product_category.setTitle(u'Product category')


def upgrade_0000_to_0008(context):
    portal = context.portal_url.getPortalObject()
    setupInitialStructure(portal)
    add_employee_idx(portal)
    add_company_idx(portal)


def upgrade_0008_to_0009(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0008_to_0009')


def upgrade_0009_to_0010(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0009_to_0010')
    portal = context.portal_url.getPortalObject()
    if 'offerte' not in portal.objectIds():
        offerte = portal[portal.invokeFactory('Offers','offerte')]
        offerte.setTitle(u'Offerte')

    if 'portal_vocabularies' in portal.objectIds():
        if 'demand_category' not in portal.portal_vocabularies.objectIds():
            voc = portal.portal_vocabularies[portal.portal_vocabularies.invokeFactory('SortedSimpleVocabulary','demand_category')]
            voc.setTitle(u'Demand category')


def upgrade_0010_to_0011(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0010_to_0011')


def upgrade_0011_to_0012(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0011_to_0012')
    portal = context.portal_url.getPortalObject()

    name = 'facebook-users'
    out = StringIO()
    userFolder = portal['acl_users']

    if name not in userFolder:

        plugin = FacebookUsers(name, 'Facebook Users')
        userFolder[name] = plugin

        # Activate all interfaces
        activatePluginInterfaces(portal, name, out)

        # Move plugin to the top of the list for each active interface
        plugins = userFolder['plugins']
        for info in plugins.listPluginTypeInfo():
            interface = info['interface']
            if plugin.testImplements(interface):
                active = list(plugins.listPluginIds(interface))
                if name in active:
                    active.remove(name)
                    active.insert(0, name)
                    plugins._plugins[interface] = tuple(active)

        return out.getvalue()


def upgrade_0012_to_0013(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0012_to_0013')


def upgrade_0013_to_0014(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0013_to_0014')


def upgrade_0014_to_0015(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0014_to_0015')


def upgrade_0015_to_0016(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0015_to_0016')


def upgrade_0016_to_0017(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0016_to_0017')


def upgrade_0017_to_0018(context):
    context.runAllImportStepsFromProfile('profile-restarter.policy:upgrade_0017_to_0018')


