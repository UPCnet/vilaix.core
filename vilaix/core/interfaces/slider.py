# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("vilaix.core")


class ISlider(form.Schema):
    """Un Slider
    """

    image = NamedImage(
        title=_(u"Image"),
        description=_(u"Please upload an image"),
        required=False,
    )

    # URLdesti = schema.TextLine(
    #     title=_(u"URLdesti"),
    #     description=_(u"Afegeix la url que cal obrir"),
    #     required=False,
    # )   

    # Obrirennovafinestra = schema.Bool(
    #     title=_(u"Obrirennovafinestra"),
    #     description=_(u"Open in new window?"),
    #     required=False,
    # )