from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from cioppino.twothumbs.browser.like import LikeWidgetView as Base


class LikeWidgetView(Base):
    """ Display the like/unlike widget. """
    render = ViewPageTemplateFile('templates/thumbs.pt')
