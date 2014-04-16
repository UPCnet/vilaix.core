# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("vilaix")


class IEquipament(form.Schema):
    """Un equipament
    """

    image = NamedImage(
        title=_(u"Image"),
        description=_(u"Please upload an image"),
        required=False,
    )

    tipus = schema.TextLine(
        title=_(u"Tipus equipament"),
        description=_(u"Afegeix el tipus equipament"),
        required=False,
    )

    adreca_contacte = schema.TextLine(
        title=_(u"Adreça de contacte"),
        description=_(u"Afegeix l'adreça de contacte del responsable de l'equipament"),
        required=True,
    )

    codi_postal = schema.TextLine(
        title=_(u"Codi postal"),
        description=_(u"Afegeix el codi postal"),
        required=False,
    )

    poblacio = schema.TextLine(
        title=_(u"Població"),
        description=_(u"Afegeix la població"),
        required=False,
    )

    geolocalitzacio = schema.TextLine(
        title=_(u"Geolocalitzacio"),
        description=_(u"Afegeix la geolocalitzacio"),
        required=False,
    )

    telefon = schema.TextLine(
        title=_(u"Telèfon"),
        description=_(u"Afegeix el telèfon de contacte del responsable de l'equipament"),
        required=False,
    )

    adreca_correu = schema.TextLine(
        title=_(u"Adreça de correu"),
        description=_(u"Afegeix l'adreça de correu del responsable de l'equipament"),
        required=False,
    )

    horari = schema.TextLine(
        title=_(u"Horari"),
        description=_(u"Horari de contacte del responsable de l'equipament"),
        required=False,
    )

    mes_informacio = RichText(
        title=_(u"Més informació"),
        description=_(u"Afegeix més informació"),
        required=False,
    )

    ubicacio = RichText(
        title=_(u"geoLocalització"),
        description=_(u"Afegeix l'ubicació en el plànol"),
        required=False,
        readonly=True,
    )

    ubicacio_iframe = RichText(
        title=_(u"geoLocalització"),
        description=_(u"Enganxa iframe de google maps si la ubicació no surt correctament"),
        required=False,
    )

