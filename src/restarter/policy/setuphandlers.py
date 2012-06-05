

def setupInitialStructure(portal):
    if u'aziende' not in portal.objectIds() or u'Aziende' not in portal.objectIds():
        companies = portal[portal.invokeFactory('Companies','aziende')]
        companies.setTitle(u'Aziende')
        portal.portal_workflow.doActionFor(companies, "publish", comment="Published on portal creation")


def importVarious(context):
    """Miscellanous steps import handle"""
    if context.readDataFile('restarter.policy-various.txt') is None:
        return
    portal = context.getSite()
    setupInitialStructure(portal)
