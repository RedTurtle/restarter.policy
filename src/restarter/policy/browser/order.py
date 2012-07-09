from zope.publisher.browser import BrowserView

class OrderView(BrowserView):

    def __call__(self):
        """Redirect if user has permission"""
        return self.request.RESPONSE.redirect(self.context.absolute_url())
