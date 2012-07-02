import urllib
import time

from zope import schema
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName
from zope.publisher.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from restarter.policy import policyMessageFactory as _

FACEBOOK_AUTH_URL         = "https://graph.facebook.com/oauth/authorize"
FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
FACEBOOK_PROFILE_URL      = "https://graph.facebook.com/me"


class IFacebookloginSettings(Interface):
    fb_app_id = schema.TextLine(title=_(u'App ID/API Key'), 
                                description=_(u'The App ID/API Key you got when creating the app at https://developers.facebook.com/apps'))
    fb_app_secret = schema.TextLine(title=_(u'App Secret'), 
                                    description=_(u'The App Secret Key you got when creating the app at https://developers.facebook.com/apps'))


class FacebookLogin(BrowserView):
    """
    Taken from https://raw.github.com/codesyntax/cs.auth.facebook/master/cs/auth/facebook/login.py
    
    This view implements the Facebook OAuth 2.0 login protocol.

    The user may access the view via a link in an action or elsewhere. He
    will then be immediately redirected to Facebook, which will ask him to
    authorize this as an application.

    Assuming that works, Facebook will redirect the user back to this same
    view, with a code in the request.
    """
    
    def __call__(self):
        registry = getUtility(IRegistry)
        FB_APP_ID = registry.get('restarter.policy.browser.facebook_login.IFacebookloginSettings.fb_app_id','').encode()
        if not FB_APP_ID:
            IStatusMessage(self.request).add(_(u"Facebook not configurated."), type="error")
            self.request.response.redirect(self.context.absolute_url())
            return u""

        verificationCode = self.request.form.get("code", None)
        errorReason      = self.request.form.get("error_reason", None)

        args = {
                'client_id': FB_APP_ID,
                'scope': 'publish_actions,email',
                #'redirect_uri': "%s/%s?came_from=%s" % (self.context.absolute_url(), self.__name__, self.request.get('came_from')),
                'redirect_uri': "%s/%s" % (self.context.absolute_url(), self.__name__,),
            }

        # Did we get an error back after a Facebook redirect?
        if errorReason is not None:
            IStatusMessage(self.request).add(_(u"Facebook authentication denied"), type="error")
            self.request.response.redirect(self.context.absolute_url())
            return u""

        # If there is no code, this is probably the first request, so redirect
        # to Facebook

        if verificationCode is None:
            self.request.response.redirect(
                    "%s?%s" % (FACEBOOK_AUTH_URL, urllib.urlencode(args),)
                )
            return u""

        if self.portal_membership.isAnonymousUser():
            self.request.RESPONSE.redirect('%s/@@facebook_register' % self.portal.absolute_url())
        else:
            url = self.request.get('came_from')
            if url is not None:
                self.request.RESPONSE.redirect(url[0])
            else:
                self.request.RESPONSE.redirect('%s?ts=%s' % (self.portal.absolute_url(),time.time()))

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


