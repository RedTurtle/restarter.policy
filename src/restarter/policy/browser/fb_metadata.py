from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from sc.social.like.browser.viewlets import SocialMetadataViewlet, SocialLikesViewlet as BaseLikeViewlet
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.interfaces import ILeadImageable

from restarter.policy.interfaces import IProduct, ICompany


class SocialLikesViewlet(BaseLikeViewlet):
    render = ViewPageTemplateFile("templates/sociallikes.pt")


class RestarterMetadataViewlet(SocialMetadataViewlet):

    render = ViewPageTemplateFile("templates/facebook_metadata.pt")

    def getImage(self):
        if not ILeadImageable.providedBy(self.context):
            return '%s/logo_facciamo_column.png' % self.context.portal_url()
        clfield = self.context.getField(IMAGE_FIELD_NAME)
        if clfield is not None:
            value = clfield.get(self.context)
            if value:
                return '%s/leadImage_preview' % self.context.absolute_url()

        dfield = self.context.getField('image')
        if dfield is not None:
            value = dfield.get(self.context)
            if value:
                return '%s/image_mini' % self.context.absolute_url()

        return '%s/logo_facciamo_column.png' % self.context.portal_url()

    @property
    def fb_type(self):
        if IProduct.providedBy(self.context):
            return 'facciamoadesso:product'
        elif ICompany.providedBy(self.context):
            return 'facciamoadesso:company'
        else:
            return 'website'

    def getOthers(self):
        if ICompany.providedBy(self.context):
            return [{'property':'facciamoadesso:address',
                     'content':'%s, %s' % (self.context.getAddress(), self.context.getCity())}]
        return []

    @property
    def canonical_url(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        return context_state.canonical_object_url()

    @property
    def title(self):
        return self.context.title_or_id()

    @property
    def description(self):
        descr = getattr(self.context, 'Description', None)
        if descr and callable(descr):
            descr = descr()
        if not descr:
            descr = u'Facciamo e un portale di comunicazione e scambio per facilitare l\'incontro tra le imprese che hanno bisogno e chi e disposto a contribuire.'
        return descr

