from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite

from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName

_ = MessageFactory('plone')


class WorkflowStatesVocabulary(object):
    """Vocabulary factory for workflow states.
    Fix unicode errors."""

    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        wtool = getToolByName(site, 'portal_workflow', None)
        if wtool is None:
            return SimpleVocabulary([])

        # XXX This is evil. A vocabulary shouldn't be request specific.
        # The sorting should go into a separate widget.

        # we get REQUEST from wtool because context may be an adapter
        request = aq_get(wtool, 'REQUEST', None)

        items = wtool.listWFStatesByTitle(filter_similar=True)
        items_dict = dict([(i[1], translate(_(i[0].decode('utf8','ignore')), context=request)) for i in items])
        items_list = [(k, v) for k, v in items_dict.items()]
        items_list.sort(lambda x, y: cmp(x[1], y[1]))
        terms = [SimpleTerm(k, title=u'%s [%s]' % (v, k)) for k, v in items_list]
        return SimpleVocabulary(terms)

WorkflowStatesVocabularyFactory = WorkflowStatesVocabulary()

