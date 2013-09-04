# -*- coding: utf-8 -*-
"""Behaviours to assign tags (to ideas).

Includes a form field and a behaviour adapter that stores the data in the
standard Subject field.
"""

from zope.interface import alsoProvides

from plone.directives import form

from zope import schema


class INewDestacada(form.Schema):
    """Add tags to content
    """
   
    destacat = schema.Bool(
        title=u"Destacat",
        description=u"Noticia destacada",
        required=False,
    )

alsoProvides(INewDestacada, form.IFormFieldProvider)
