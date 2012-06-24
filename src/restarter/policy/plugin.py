import logging
import json
import urlparse
import urllib

from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import (
        IExtractionPlugin,
        IAuthenticationPlugin,
    )

from restarter.policy.browser.facebook_login import FACEBOOK_ACCESS_TOKEN_URL, FACEBOOK_PROFILE_URL


logger = logging.getLogger('restarter.policy')


class AddForm(BrowserView):
    """Add form the PAS plugin
    """

    def __call__(self):

        if 'form.button.Add' in self.request.form:
            name = self.request.form.get('id')
            title = self.request.form.get('title')

            plugin = FacebookUsers(name, title)
            self.context.context[name] = plugin

            self.request.response.redirect(self.context.absolute_url() +
                    '/manage_workspace?manage_tabs_message=Plugin+added.')


class FacebookUsers(BasePlugin):
    """PAS plugin for authentication against facebook.

    Here, we implement a number of PAS interfaces, using a session managed
    by Beaker (via collective.beaker) to temporarily store the values we
    have captured.
    """

    # List PAS interfaces we implement here
    implements(
            IExtractionPlugin,
            IAuthenticationPlugin,
        )

    def __init__(self, id, title=None):
        self.__name__ = self.id = id
        self.title = title

    def __get_access_token__(self, verificationCode):
        registry = getUtility(IRegistry)
        FB_APP_SECRET = registry.get('restarter.policy.browser.facebook_login.IFacebookloginSettings.fb_app_secret').encode()
        FB_APP_ID = registry.get('restarter.policy.browser.facebook_login.IFacebookloginSettings.fb_app_id').encode()
        args = {
                'client_id': FB_APP_ID,
                'redirect_uri': "%s/facebook-login" % self.portal_url(),
            }
        args["client_secret"] = FB_APP_SECRET
        args["code"] = verificationCode

        print 'Getting token from facebook'
        response = urlparse.parse_qs(urllib.urlopen(
                "%s?%s" % (FACEBOOK_ACCESS_TOKEN_URL, urllib.urlencode(args),)
            ).read())

        # Load the profile using the access token we just received
        accessToken = response["access_token"][-1]
        return accessToken

    def extractCredentials(self, request):
        verificationCode = request.form.get("code", None)

        if verificationCode:
            session = self.session_data_manager.getSessionData()
            accessToken = session.get('facebook_token')
            if not accessToken:
                accessToken = self.__get_access_token__(verificationCode)
                session['facebook_token'] = accessToken
            print 'Getting profile from facebook'
            profile = json.load(urllib.urlopen(
                              "%s?%s" % (FACEBOOK_PROFILE_URL, urllib.urlencode({'access_token': accessToken}),)
                        ))
            session['facebook_profile'] = profile
            return {'facebook_id': profile.get('id')}
        return {}

    def authenticateCredentials(self, credentials):
        facebook_id = credentials.get('facebook_id')
        if facebook_id is not None:
            ms_tool = getToolByName(self, 'portal_membership')
            user_id = login = ''
            for member in ms_tool.listMembers():
                member_facebook_id = member.getProperty('facebook_id')
                if facebook_id == member_facebook_id:
                    user_id = login = member.getId()
                    break
            if user_id and login:
                self._getPAS().updateCredentials(self.REQUEST, self.REQUEST.RESPONSE, login, "")
                return (user_id, login)
            else:
                return None
        return None
