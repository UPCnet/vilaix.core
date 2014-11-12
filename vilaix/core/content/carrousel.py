# -*- coding: utf-8 -*-
from five import grok
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.indexer.decorator import indexer
from plone.app.contenttypes.utils import replace_link_variables_by_paths

from zope import schema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("vilaix")


class ICarrousel(form.Schema):
    """ A site banner.
    """

    image = NamedBlobImage(
        title=_(u"Picture"),
        description=_(u"Please upload an image"),
        required=False,
    )

    remoteUrl = schema.TextLine(
        title=_(u"url"),
        description=_(u"URL to open"),
        required=False,
    )


@indexer(ICarrousel)
def getRemoteUrl(obj):
    if obj.remoteUrl:
        return replace_link_variables_by_paths(obj, obj.remoteUrl)
grok.global_adapter(getRemoteUrl, name='getRemoteUrl')
