from plone.app.users.browser.register import RegistrationForm as BaseForm
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


def get_email(self):
    session = self.context.session_data_manager.getSessionData()
    profile = session['facebook_profile']
    return profile.get('email')


def get_fullname(self):
    session = self.context.session_data_manager.getSessionData()
    profile = session['facebook_profile']
    return profile.get('name')


def get_username(self):
    session = self.context.session_data_manager.getSessionData()
    profile = session['facebook_profile']
    return profile.get('username')


class RegistrationForm(BaseForm):
    """ Dynamically get fields from user data, through admin
        config settings.
    """

    @property
    def form_fields(self):
        defaultFields = super(RegistrationForm, self).form_fields
        if not defaultFields:
            return defaultFields
        defaultFields.get('email').get_rendered = get_email
        defaultFields.get('fullname').get_rendered = get_fullname
        defaultFields.get('username').get_rendered = get_username
        defaultFields = defaultFields.omit('rpx_identifier')
        defaultFields = defaultFields.omit('facebook_id')
        defaultFields = defaultFields.omit('facebook_token')
        return defaultFields

    @form.action(_(u'label_register', default=u'Register'), validator='validate_registration', name=u'register')
    def action_join(self, action, data):
        self.handle_join_success(data)
        return self.context.unrestrictedTraverse('rpx_registered')()

    def handle_join_success(self, data):
        registration = getToolByName(self.context, 'portal_registration')
        session = self.context.session_data_manager.getSessionData()
        data['facebook_id'] = session['facebook_profile'].get('id')
        data['facebook_token'] = session['facebook_token']
        data['password'] = registration.generatePassword()
        return super(RegistrationForm, self).handle_join_success(data)

