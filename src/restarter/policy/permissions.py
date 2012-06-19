from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

security = ModuleSecurityInfo('restarter.policy')
security.declarePublic('ManageAssociationLikes')
ManageAssociationLikes = 'restarter.policy: ManageAssociationLikes'
setDefaultRoles(ManageAssociationLikes, ('Association',))
