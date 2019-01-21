# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form
from plone.indexer.decorator import indexer
from plone.namedfile.field import NamedImage
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("vilaix")


class ISlider(form.Schema):
    """Un Slider
    """

    image = NamedImage(
        title=_(u"Image"),
        description=_(u"Please upload an image"),
        required=False,
    )

    alt = schema.TextLine(
        title=_(u"Alt"),
        description=_(u"Afegeix la descripció que vols que es mostri per temes accessibilitat"),
        required=False,
    )

    remoteUrl = schema.TextLine(
        title=_(u"url"),
        description=_(u"URL to open"),
        required=False,
    )


@indexer(ISlider)
def getRemoteUrl(obj):
    if obj.remoteUrl:
        return replace_link_variables_by_paths(obj, obj.remoteUrl)


grok.global_adapter(getRemoteUrl, name='getRemoteUrl')
