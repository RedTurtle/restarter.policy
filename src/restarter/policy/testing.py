from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class RestarterPolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import restarter.policy
        xmlconfig.file('configure.zcml',
                       restarter.policy,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'restarter.policy:default')

RESTARTER_POLICY_FIXTURE = RestarterPolicy()
RESTARTER_POLICY_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(RESTARTER_POLICY_FIXTURE, ),
                       name="RestarterPolicy:Integration")