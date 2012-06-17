from zope.interface import implements
from zope import schema
import re

from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

from restarter.policy import policyMessageFactory as _


def validateCellphone(value):
    pattern = re.compile('^\+39\d*$')
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

    rpx_identifier = schema.Tuple(
        title=u'rpx identifier',
    )

    facebook_id = schema.TextLine(
        title=u'facebook profile id',
    )

    facebook_token = schema.TextLine(
        title=u'facebook token',
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

    def get_rpx(self):
        return self.context.getProperty('rpx_identifier', '')
    def set_rpx(self, value):
        return self.context.setMemberProperties({'rpx_identifier': value})
    rpx_identifier = property(get_rpx, set_rpx)

    def get_facebook_id(self):
        return self.context.getProperty('facebook_id', '')
    def set_facebook_id(self, value):
        return self.context.setMemberProperties({'facebook_id': value})
    facebook_id = property(get_facebook_id, set_facebook_id)

    def get_facebook_token(self):
        return self.context.getProperty('facebook_token', '')
    def set_facebook_token(self, value):
        return self.context.setMemberProperties({'facebook_token': value})
    facebook_token = property(get_facebook_token, set_facebook_token)

