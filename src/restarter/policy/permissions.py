from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

security = ModuleSecurityInfo('restarter.policy')
security.declarePublic('ManageAssociationLikes')
ManageAssociationLikes = 'restarter.policy: ManageAssociationLikes'
ManageStories = 'restarter.policy: ManageStories'
setDefaultRoles(ManageAssociationLikes, ('Association',))
