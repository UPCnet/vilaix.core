# -*- coding: utf-8 -*-
from five import grok
from zope import schema

from plone.directives import form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from plone.namedfile.field import NamedFile

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("serveiesports")


class ITramit(form.Schema):
    """Un tràmit
    """

    image = NamedImage(
        title=_(u"Image"),
        description=_(u"Please upload an image"),
        required=False,
    )

    qui = RichText(
        title=_(u"Qui el pot sol·licitar?"),
        description=_(u"Indiqueu qui pot sol·licitar aquest tràmit."),
        required=False,
    )

    documentacio = RichText(
        title=_(u"Documentació que cal aportar"),
        description=_(u"Indiqueu la documentació que cal aportar sol·licitar aquest tràmit."),
        required=False,
    )

    quan = RichText(
        title=_(u"Quan es pot demanar?"),
        description=_(u"Indiqueu quan es pot sol·licitar aquest tràmit."),
        required=False,
    )

    quin = RichText(
        title=_(u"Quin és el temps de tramitació/resolució?"),
        description=_(u"Indiqueu quin és el temps de tramitació/resolució d'aquest tràmit."),
        required=False,
    )

    tipus_silenci = RichText(
        title=_(u"Tipus de silenci"),
        description=_(u"Indiqueu quin és el tipus de silenci per aquest tràmit."),
        required=False,
    )

    preu = RichText(
        title=_(u"Quin preu té la tramitació?"),
        description=_(u"Indiqueu quin preu té la tramitació d'aquest tràmit."),
        required=False,
    )

    pagament = RichText(
        title=_(u"Com puc fer el pagament?"),
        description=_(u"Indiqueu con puc fer el pagament d'aquest tràmit."),
        required=False,
    )

    canals = RichText(
        title=_(u"Quins canals de tramitació té?"),
        description=_(u"Indiqueu els canals de tramitació."),
        required=False,
    )

    responsable = RichText(
        title=_(u"Quin és l'organisme responsable?"),
        description=_(u"Indiqueu quin és l'organisme responsable d'aquest tràmit."),
        required=False,
    )
    
    inici = schema.TextLine(
        title=_(u"Enllaç per iniciar el tràmit electrònicament"),
        description=_(u"Indiqueu l'enllàç per iniciar el tràmit electrònicament."),
        required=False,
    )

    fitxer_inici = NamedFile(
        title=_(u"Fitxer annex per iniciar el tràmit presencialment."),
        description=_(u"Adjunteu el fitxer per iniciar el tràmit presencialment."),
        required=False,
    )