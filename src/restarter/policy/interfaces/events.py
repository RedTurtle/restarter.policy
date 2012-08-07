from zope.component.interfaces import IObjectEvent


class IDisqusNotify(IObjectEvent):
    """An action happend in disqus comment box"""


class ICompanyShareNotify(IObjectEvent):
    """A user has been added to company employees"""


class IHomepageStoryNotify(IObjectEvent):
    """A company story has been marked for homepage"""
