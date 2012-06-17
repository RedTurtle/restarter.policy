from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.browser.viewlets import SocialMetadataViewlet
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from restarter.policy.interfaces import IProduct, ICompany
from collective.contentleadimage.interfaces import ILeadImageable

class RestarterMetadataViewlet(SocialMetadataViewlet):

    render = ViewPageTemplateFile("templates/facebook_metadata.pt")

    def getImage(self):
        import pdb; pdb.set_trace()
        if not ILeadImageable.providedBy(self.context):
            return '%s/logo_facciamo_column.png' % self.context.portal_url()
        clfield = self.context.getField(IMAGE_FIELD_NAME)
        if clfield is not None:
            value = clfield.get(self.context)
            if value:
                return '%s/leadImage_tile' % self.context.absolute_url()

        dfield = self.context.getField('image')
        if dfield is not None:
            value = dfield.get(self.context)
            if value:
                return '%s/image_tile' % self.context.absolute_url()

        return '%s/logo_facciamo_column.png' % self.context.portal_url()

    @property
    def fb_type(self):
        if IProduct.providedBy(self.context):
            return 'facciamoadesso:product'
        elif ICompany.providedBy(self.context):
            return 'facciamoadesso:company'
        else:
            return 'website'

    @property
    def title(self):
        return self.context.title_or_id()

    @property
    def description(self):
        return getattr(self.context, 'Description', '')

