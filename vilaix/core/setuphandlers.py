# -*- coding: utf-8 -*-
from zope.interface import alsoProvides

from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.site import ISiteSchema

from genweb.core.interfaces import IHomePage
from Products.CMFPlone.utils import _createObjectByType

import logging
import transaction
import pkg_resources

from genweb.core.interfaces import IHomePage
from zope.component.hooks import getSite

from zope.interface import alsoProvides 
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs

from datetime import datetime


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_DXCT = False
else:
    HAS_DXCT = True
    from plone.dexterity.utils import createContentInContainer

# def createOrGetObject(self, context, newid, title, type_name):
#     if newid in context.contentIds():
#         obj = context[newid]
#     else:
#         obj = createContentInContainer(context, type_name, title=title, checkConstrains=False)
#         transaction.savepoint()
#         if obj.id != newid:
#             context.manage_renameObject(obj.id, newid)
#         obj.reindexObject()
#     return obj
    
# def newFolder(self, context, newid, title, type_name=u'Folder'):
#     return self.createOrGetObject(context, newid, title, type_name)

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    #import ipdb; ipdb.set_trace()

    if context.readDataFile('vilaix.core_various.txt') is None:
        return

    # Add additional setup code here
    #
    # portal = context.getSite()
    # logger = logging.getLogger(__name__)
    # transforms = getToolByName(portal, 'portal_transforms')
    # transform = getattr(transforms, 'safe_html')
    # valid = transform.get_parameter_value('valid_tags')
    # nasty = transform.get_parameter_value('nasty_tags')
    #import ipdb; ipdb.set_trace()

    if HAS_DXCT:
        portal = getSite()
        pl = getToolByName(portal, 'portal_languages')
        if getattr(portal, 'front-page', False):
            portal.manage_delObjects('front-page')
            frontpage = createContentInContainer(portal, 'Document', title=u"front-page", checkConstraints=False)
            alsoProvides(frontpage, IHomePage)
            frontpage.exclude_from_nav = True
            frontpage.language = pl.getDefaultLanguage()
            frontpage.reindexObject()
        # Set the default page to the homepage view
        portal.setDefaultPage('homepage')        
    else:
        return 'This site has no p.a.contenttypes installed.'

    #Crear carpetes i contingut necessari per al funcionament del tema
    urltool = getToolByName(portal, 'portal_url')        
    portal_catalog = getToolByName(portal, 'portal_catalog')
    path = urltool.getPortalPath() 
    obj = []
    
    workflowTool = getToolByName(portal, "portal_workflow")   

    #Menú Lateral
    obj = portal_catalog.searchResults(portal_type = 'Folder',
                                       path = path + '/menu-lateral')
    if obj.actual_result_count == 0:                                   
        menu_lateral = createContentInContainer(portal, 'Folder', title=u"Menú Lateral", checkConstraints=False)
        menu_lateral.language = pl.getDefaultLanguage()
        menu_lateral.exclude_from_nav = True
        workflowTool.doActionFor(menu_lateral, "publish")
        alsoProvides(menu_lateral, IHideFromBreadcrumbs) 
        menu_lateral.reindexObject()   
        la_ciutat_per_temes = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat per temes", checkConstraints=False)
        la_ciutat_per_temes.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(la_ciutat_per_temes, "publish")
        la_ciutat_per_temes.reindexObject()   
        la_ciutat_per_les_persones = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat i les persones", checkConstraints=False)
        la_ciutat_per_les_persones.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(la_ciutat_per_les_persones, "publish")
        la_ciutat_per_les_persones.reindexObject()
        la_ciutat_per_xifres = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat en xifres", checkConstraints=False)
        la_ciutat_per_xifres.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(la_ciutat_per_xifres, "publish")
        la_ciutat_per_xifres.reindexObject()
        la_ciutat_per_districtes = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat per districtes", checkConstraints=False)
        la_ciutat_per_districtes.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(la_ciutat_per_districtes, "publish")
        la_ciutat_per_districtes.reindexObject()  

    #Menú principal
    obj = portal_catalog.searchResults(portal_type = 'Folder',
                                       path = path + '/menu-principal')
    if obj.actual_result_count == 0:                                   
        menu_principal = createContentInContainer(portal, 'Folder', title=u"Menú principal", checkConstraints=False)
        menu_principal.language = pl.getDefaultLanguage()
        menu_principal.exclude_from_nav = True
        workflowTool.doActionFor(menu_principal, "publish")
        alsoProvides(menu_principal, IHideFromBreadcrumbs)
        menu_principal.reindexObject()
        ajuntament = createContentInContainer(menu_principal, 'Folder', title=u"Ajuntament", checkConstraints=False)
        ajuntament.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(ajuntament, "publish")
        ajuntament.reindexObject()  
        informacio_municipal = createContentInContainer(menu_principal, 'Folder', title=u"Informació Municipal", checkConstraints=False)
        informacio_municipal.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(informacio_municipal, "publish")
        informacio_municipal.reindexObject()  
        seu_electronica = createContentInContainer(menu_principal, 'Folder', title=u"Seu electrònica", checkConstraints=False)
        seu_electronica.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(seu_electronica, "publish")
        seu_electronica.reindexObject()    
        guia_de_la_ciutat = createContentInContainer(menu_principal, 'Folder', title=u"Guia de la ciutat", checkConstraints=False)
        guia_de_la_ciutat.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(guia_de_la_ciutat, "publish")
        guia_de_la_ciutat.reindexObject()    
        borsa_de_treball = createContentInContainer(menu_principal, 'Folder', title=u"Borsa de treball", checkConstraints=False)
        borsa_de_treball.language = pl.getDefaultLanguage()       
        workflowTool.doActionFor(borsa_de_treball, "publish")
        borsa_de_treball.reindexObject()


    #Carrousel
    obj = portal_catalog.searchResults(portal_type = 'Folder',
                                       path = path + '/carrousel')
    if obj.actual_result_count == 0:                                   
        carrousel = createContentInContainer(portal, 'Folder', title=u"Carrousel", checkConstraints=False)
        carrousel.language = pl.getDefaultLanguage()
        carrousel.exclude_from_nav = True
        workflowTool.doActionFor(carrousel, "publish")
        carrousel.reindexObject()   
   
    #Imatges Capçalera
    obj = portal_catalog.searchResults(portal_type = 'Folder',
                                       path = path + '/imatges-capcalera')
    if obj.actual_result_count == 0:                                   
        imatges_capcalera = createContentInContainer(portal, 'Folder', title=u"Imatges Capçalera", checkConstraints=False)
        imatges_capcalera.language = pl.getDefaultLanguage()
        imatges_capcalera.exclude_from_nav = True
        workflowTool.doActionFor(imatges_capcalera, "publish")
        imatges_capcalera.reindexObject()  
    
    #Banners dreta
    obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
                                       path = path + '/banners_dreta')
    if obj.actual_result_count == 0:  
        _createObjectByType('BannerContainer', portal, 'banners_dreta')  
        portal['banners_dreta'].setExcludeFromNav(True)
        portal['banners_dreta'].setTitle('Banners-dreta')
        portal['banners_dreta'].reindexObject()
        workflowTool.doActionFor(portal.banners_dreta, "publish")  
        # _createObjectByType('Banner', portal['banners_dreta'], 'oficina_virtual')  
        # obj = portal['banners_dreta']['oficina_virtual']  
        # obj.Title = 'Oficina Virtual'
        # obj.Obrirennovafinestra = True
        # obj.URLdesti = "http://www.google.es"       
        # obj.setImatge = "/vilaix/theme/static/images/oficina_virtual.png"
        # workflowTool.doActionFor(obj, "publish")  
        
    #Banners esquerra
    obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
                                       path = path + '/banners_esquerra')
    if obj.actual_result_count == 0:  
        _createObjectByType('BannerContainer', portal, 'banners_esquerra')  
        portal['banners_esquerra'].setExcludeFromNav(True)
        portal['banners_esquerra'].setTitle('Banners-esquerra')
        portal['banners_esquerra'].reindexObject()
        workflowTool.doActionFor(portal.banners_esquerra, "publish")    
        
    #Slider
    obj = portal_catalog.searchResults(portal_type = 'Folder',
                                       path = path + '/slider')
    if obj.actual_result_count == 0:                                   
        carrousel = createContentInContainer(portal, 'Folder', title=u"Slider", checkConstraints=False)
        carrousel.language = pl.getDefaultLanguage()
        carrousel.exclude_from_nav = True
        workflowTool.doActionFor(carrousel, "publish")
        carrousel.reindexObject()                                  
       
    transaction.commit()   