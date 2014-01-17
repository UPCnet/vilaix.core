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

    
    portal = context.getSite()
    
    # Delete old AT folders
    # if getattr(portal, 'events', None):
    #     if portal.events.__class__.__name__ == 'Folder':
    #         portal.manage_delObjects(['events'])

    # if getattr(portal, 'news', None):
    #     if portal.news.__class__.__name__ == 'Folder':
    #         portal.manage_delObjects(['news'])

    if getattr(portal, 'Members', None):
        if portal.Members.__class__.__name__ == 'ATFolder':
            portal.manage_delObjects(['Members'])

    # if getattr(portal, 'front-page', None):
    #     if portal['front-page'].__class__.__name__ == 'ATDocument':
    #         portal.manage_delObjects(['front-page'])

    if HAS_DXCT:
        portal = getSite()
        pl = getToolByName(portal, 'portal_languages')
        workflowTool = getToolByName(portal, "portal_workflow")   

        if getattr(portal, 'front-page', False):
            portal.manage_delObjects('front-page')
            frontpage = createContentInContainer(portal, 'Document', title=u"front-page", checkConstraints=False)
            alsoProvides(frontpage, IHomePage)
            frontpage.exclude_from_nav = True
            frontpage.language = pl.getDefaultLanguage()
            workflowTool.doActionFor(frontpage, "publish")
            frontpage.reindexObject()
        # Set the default page to the homepage view
        portal.setDefaultPage('homepage')        
    else:
        return 'This site has no p.a.contenttypes installed.'

    #Crear carpetes i contingut necessari per al funcionament del tema
    urltool = getToolByName(portal, 'portal_url')        
    portal_catalog = getToolByName(portal, 'portal_catalog')
    path = urltool.getPortalPath() 
    portal = getSite()
    obj = []   

    workflowTool = getToolByName(portal, "portal_workflow")   

    # #Actualitat
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/actualitat')
    # # if obj.actual_result_count == 0:                                   
    # #     actualitat = createContentInContainer(portal, 'Folder', title=u"Actualitat", checkConstraints=False)
    # #     actualitat.language = pl.getDefaultLanguage()
    # #     actualitat.exclude_from_nav = True
    # #     workflowTool.doActionFor(actualitat, "publish")
    # #     actualitat.reindexObject()   

    # #Noticias
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/noticies')
    # # if obj.actual_result_count == 0:                                   
    # #     noticies = createContentInContainer(actualitat, 'Folder', title=u"Notícies", checkConstraints=False)
    # #     noticies.language = pl.getDefaultLanguage()
    # #     noticies.exclude_from_nav = True
    # #     workflowTool.doActionFor(noticies, "publish")
    # #     noticies.reindexObject()   

    # #Collection Noticias
    # # obj = portal_catalog.searchResults(portal_type = 'Collection',
    # #                                    path = path + '/noticies/noticies')
    # # if obj.actual_result_count == 0:                                   
    # #     noticies = createContentInContainer(noticies, 'Collection', title=u"Notícies", checkConstraints=False)
    # #     noticies.language = pl.getDefaultLanguage()
    # #     noticies.exclude_from_nav = True
    # #     workflowTool.doActionFor(noticies, "publish")
    # #     noticies.reindexObject()  

    # #esdeveniments
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/esdeveniments')
    # # if obj.actual_result_count == 0:                                   
    # #     esdeveniments = createContentInContainer(actualitat, 'Folder', title=u"Esdeveniments", checkConstraints=False)
    # #     esdeveniments.language = pl.getDefaultLanguage()
    # #     esdeveniments.exclude_from_nav = True
    # #     workflowTool.doActionFor(esdeveniments, "publish")
    # #     esdeveniments.reindexObject()   
    
    # #Collection esdeveniments
    # # obj = portal_catalog.searchResults(portal_type = 'Collection',
    # #                                    path = path + '/esdeveniments/esdeveniments')
    # # if obj.actual_result_count == 0:                                   
    # #     esdeveniments = createContentInContainer(actualitat, 'Collection', title=u"Esdeveniments", checkConstraints=False)
    # #     esdeveniments.language = pl.getDefaultLanguage()
    # #     esdeveniments.exclude_from_nav = True
    # #     workflowTool.doActionFor(esdeveniments, "publish")
    # #     esdeveniments.reindexObject()   
    
    # #Menú principal
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/menu-principal')
    # if obj.actual_result_count == 0:                                   
    #     menu_principal = createContentInContainer(portal, 'Folder', title=u"Menú principal", checkConstraints=False)
    #     menu_principal.language = pl.getDefaultLanguage()
    #     menu_principal.exclude_from_nav = True
    #     workflowTool.doActionFor(menu_principal, "publish")
    #     alsoProvides(menu_principal, IHideFromBreadcrumbs)
    #     menu_principal.reindexObject()
    #     ajuntament = createContentInContainer(menu_principal, 'Folder', title=u"Ajuntament", checkConstraints=False)
    #     ajuntament.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(ajuntament, "publish")
    #     ajuntament.reindexObject()  
    #     informacio_municipal = createContentInContainer(menu_principal, 'Folder', title=u"Informació Municipal", checkConstraints=False)
    #     informacio_municipal.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(informacio_municipal, "publish")
    #     informacio_municipal.reindexObject()  
    #     seu_electronica = createContentInContainer(menu_principal, 'Folder', title=u"Seu electrònica", checkConstraints=False)
    #     seu_electronica.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(seu_electronica, "publish")
    #     seu_electronica.reindexObject()    
    #     guia_de_la_ciutat = createContentInContainer(menu_principal, 'Folder', title=u"Guia de la ciutat", checkConstraints=False)
    #     guia_de_la_ciutat.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(guia_de_la_ciutat, "publish")
    #     guia_de_la_ciutat.reindexObject()    
    #     borsa_de_treball = createContentInContainer(menu_principal, 'Folder', title=u"Borsa de treball", checkConstraints=False)
    #     borsa_de_treball.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(borsa_de_treball, "publish")
    #     borsa_de_treball.reindexObject()

    # #Menú Lateral
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/menu-lateral')
    # if obj.actual_result_count == 0:                                   
    #     menu_lateral = createContentInContainer(portal, 'Folder', title=u"Menú Lateral", checkConstraints=False)
    #     menu_lateral.language = pl.getDefaultLanguage()
    #     menu_lateral.exclude_from_nav = True
    #     workflowTool.doActionFor(menu_lateral, "publish")
    #     alsoProvides(menu_lateral, IHideFromBreadcrumbs) 
    #     menu_lateral.reindexObject()   
    #     la_ciutat_per_temes = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat per temes", checkConstraints=False)
    #     la_ciutat_per_temes.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(la_ciutat_per_temes, "publish")
    #     la_ciutat_per_temes.reindexObject()   
    #     la_ciutat_per_les_persones = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat i les persones", checkConstraints=False)
    #     la_ciutat_per_les_persones.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(la_ciutat_per_les_persones, "publish")
    #     la_ciutat_per_les_persones.reindexObject()
    #     la_ciutat_per_xifres = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat en xifres", checkConstraints=False)
    #     la_ciutat_per_xifres.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(la_ciutat_per_xifres, "publish")
    #     la_ciutat_per_xifres.reindexObject()
    #     la_ciutat_per_districtes = createContentInContainer(menu_lateral, 'Folder', title=u"La ciutat per districtes", checkConstraints=False)
    #     la_ciutat_per_districtes.language = pl.getDefaultLanguage()       
    #     workflowTool.doActionFor(la_ciutat_per_districtes, "publish")
    #     la_ciutat_per_districtes.reindexObject()  

    # #Material multimèdia
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/material-multimedia')
    # if obj.actual_result_count == 0:                                   
    #     material_multimedia = createContentInContainer(portal, 'Folder', title=u"Material multimèdia", checkConstraints=False)
    #     material_multimedia.language = pl.getDefaultLanguage()
    #     material_multimedia.exclude_from_nav = True
    #     workflowTool.doActionFor(material_multimedia, "publish")
    #     material_multimedia.reindexObject()   

    # #Slider
    # # obj = portal_catalog.searchResults(portal_type = 'Folder',
    # #                                    path = path + '/sliders')
    # # if obj.actual_result_count == 0:                                   
    # #     slider = createContentInContainer(material_multimedia, 'Folder', title=u"Sliders", checkConstraints=False)
    # #     slider.language = pl.getDefaultLanguage()
    # #     slider.exclude_from_nav = True
    # #     workflowTool.doActionFor(slider, "publish")
    # #     slider.reindexObject()               

    # #Banners
    # # obj = portal_catalog.searchResults(portal_type = 'Folder',
    # #                                    path = path + '/banners')
    # # if obj.actual_result_count == 0:                                   
    # #     banners = createContentInContainer(material_multimedia, 'Folder', title=u"Banners", checkConstraints=False)
    # #     banners.language = pl.getDefaultLanguage()
    # #     banners.exclude_from_nav = True
    # #     workflowTool.doActionFor(banners, "publish")
    # #     banners.reindexObject()               

    
    # #Carrousel
    # # obj = portal_catalog.searchResults(portal_type = 'Folder',
    # #                                    path = path + '/carrousel')
    # # if obj.actual_result_count == 0:                                   
    # #     carrousel = createContentInContainer(material_multimedia, 'Folder', title=u"Carroussel", checkConstraints=False)
    # #     carrousel.language = pl.getDefaultLanguage()
    # #     carrousel.exclude_from_nav = True
    # #     workflowTool.doActionFor(carrousel, "publish")
    # #     carrousel.reindexObject()   
   
    # #Imatges Capçalera
    # # obj = portal_catalog.searchResults(portal_type = 'Folder',
    # #                                    path = path + '/imatges-capcalera')
    # # if obj.actual_result_count == 0:                                   
    # #     imatges_capcalera = createContentInContainer(material_multimedia, 'Folder', title=u"Imatges capçalera", checkConstraints=False)
    # #     imatges_capcalera.language = pl.getDefaultLanguage()
    # #     imatges_capcalera.exclude_from_nav = True
    # #     workflowTool.doActionFor(imatges_capcalera, "publish")
    # #     imatges_capcalera.reindexObject()  
    
    
    # #Banners dreta
    # obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
    #                                    path = path + '/material-multimedia/banners/banners_dreta')
    # if obj.actual_result_count == 0:  
    #     _createObjectByType('BannerContainer', banners, 'banners_dreta')  
    #     banners['banners_dreta'].setExcludeFromNav(True)
    #     banners['banners_dreta'].setTitle('Banners-dreta')
    #     banners['banners_dreta'].reindexObject()
    #     workflowTool.doActionFor(banners.banners_dreta, "publish")  
    #     # _createObjectByType('Banner', portal['banners_dreta'], 'oficina_virtual')  
    #     # obj = portal['banners_dreta']['oficina_virtual']  
    #     # obj.Title = 'Oficina Virtual'
    #     # obj.Obrirennovafinestra = True
    #     # obj.URLdesti = "http://www.google.es"       
    #     # obj.setImatge = "/vilaix/theme/static/images/oficina_virtual.png"
    #     # workflowTool.doActionFor(obj, "publish")  
        
    # #Banners esquerra
    # obj = portal_catalog.searchResults(portal_type = 'BannerContainer',
    #                                    path = path + '/material-multimedia/banners/banners_esquerra')
    # if obj.actual_result_count == 0:  
    #     _createObjectByType('BannerContainer', banners, 'banners_esquerra')  
    #     banners['banners_esquerra'].setExcludeFromNav(True)
    #     banners['banners_esquerra'].setTitle('Banners-esquerra')
    #     banners['banners_esquerra'].reindexObject()
    #     workflowTool.doActionFor(banners.banners_esquerra, "publish")          
        
    
    # #Documents
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/documents')
    # if obj.actual_result_count == 0:                                   
    #     documents = createContentInContainer(portal, 'Folder', title=u"Documents", checkConstraints=False)
    #     documents.language = pl.getDefaultLanguage()
    #     documents.exclude_from_nav = True
    #     workflowTool.doActionFor(documents, "publish")
    #     documents.reindexObject()     
    
    # #Directori equipaments
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/directori-equipaments')
    # if obj.actual_result_count == 0:                                   
    #     directori_equipaments = createContentInContainer(portal, 'Folder', title=u"Directori equipaments", checkConstraints=False)
    #     directori_equipaments.language = pl.getDefaultLanguage()
    #     directori_equipaments.exclude_from_nav = True
    #     workflowTool.doActionFor(directori_equipaments, "publish")
    #     directori_equipaments.reindexObject()     
                     
    
    # #Tràmits
    # obj = portal_catalog.searchResults(portal_type = 'Folder',
    #                                    path = path + '/tramits')
    # if obj.actual_result_count == 0:                                   
    #     tramits = createContentInContainer(portal, 'Folder', title=u"Tràmits", checkConstraints=False)
    #     tramits.language = pl.getDefaultLanguage()
    #     tramits.exclude_from_nav = True
    #     workflowTool.doActionFor(tramits, "publish")
    #     tramits.reindexObject()
         
    transaction.commit()   