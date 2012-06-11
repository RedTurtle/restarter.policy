
def setupInitialStructure(portal):
    if 'aziende' not in portal.objectIds() and 'Aziende' not in portal.objectIds():
        companies = portal[portal.invokeFactory('Companies','aziende')]
        companies.setTitle(u'Aziende')

    if 'portal_vocabularies' in portal.objectIds():
        if 'company_type' not in portal.portal_vocabularies.objectIds():
            company_type = portal.portal_vocabularies[portal.portal_vocabularies.invokeFactory('SortedSimpleVocabulary','company_type')]
            company_type.setTitle(u'Company type')
        if 'company_sectore' not in portal.portal_vocabularies.objectIds():
            company_sectore = portal.portal_vocabularies[portal.portal_vocabularies.invokeFactory('SortedSimpleVocabulary','company_sectore')]
            company_sectore.setTitle(u'Company sectore')

def importVarious(context):
    """Miscellanous steps import handle"""
    if context.readDataFile('restarter.policy-various.txt') is None:
        return
    portal = context.getSite()
    setupInitialStructure(portal)
