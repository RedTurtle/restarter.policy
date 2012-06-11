from zope.interface import implements
from zope import schema
import re

from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

from restarter.policy import policyMessageFactory as _


def validateCellphone(value):
    pattern = re.compile('^\+39\d{10}$')
    if pattern.match(value):
        return True
    return False

def validateAccept(value):
    if not value == True:
        return False
    return True



class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        ""
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    cellphone = schema.TextLine(
        title=_(u'label_cellphone', default=u'Cellphone number'),
        description=_(u'help_cellphone',
            default=u"Leave your cell phone number so we can reach you. The correct format is: +391234567890"),
        required=True,
        constraint=validateCellphone,
        )
    accept = schema.Bool(
        title=_(u'label_accept', default=u'Accept terms of use'),
        description=_(u'help_accept',
                      default=u"Tick this box to indicate that you have found,"
                      " read and accepted the terms of use for this site. "),
        required=True,
        constraint=validateAccept,
        )


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """ """
    def get_cellphone(self):
        return self.context.getProperty('cellphone', '')
    def set_cellphone(self, value):
        return self.context.setMemberProperties({'cellphone': value})
    cellphone = property(get_cellphone, set_cellphone)

    def get_accept(self):
        return self.context.getProperty('accept', '')
    def set_accept(self, value):
        return self.context.setMemberProperties({'accept': value})
    accept = property(get_accept, set_accept)


