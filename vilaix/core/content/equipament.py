# -*- coding: utf-8 -*-
from zope import schema

from plone.directives import form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("vilaix")


class IEquipament(form.Schema):
    """ Un equipament
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

    latitude = schema.TextLine(
        title=_(u"Latitud"),
        description=_(u"Introdueix la latitud. Es fa servir per mostrar l'element al mapa global."),
        required=False,
    )

    longitude = schema.TextLine(
        title=_(u"Longitud"),
        description=_(u"Introdueix la longitud. Es fa servir per mostrar l'element al mapa global."),
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

    ubicacio_iframe = RichText(
        title=_(u"geoLocalització"),
        description=_(u"Enganxa l'iframe de Google Maps amb la ubicació de l'element."),
        required=False,
    )
