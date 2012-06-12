
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

def importVarious(context):
    """Miscellanous steps import handle"""
    if context.readDataFile('restarter.policy-various.txt') is None:
        return
    portal = context.getSite()
    setupInitialStructure(portal)
