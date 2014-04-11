#!/usr/bin/python2.7
# -*-coding:UTF-8-*-
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer , Table 
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch ,cm , mm
from reportlab.lib.colors import white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER ,TA_RIGHT
from reportlab.lib.fonts import tt2ps
from reportlab.lib.pagesizes import A4  
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate  
from reportlab.platypus.flowables import PageBreak, Spacer  
from reportlab.platypus.paragraph import Paragraph  
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle ,StyleSheet1  
from reportlab.lib import colors  
from Models import *
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from Canvas import CanvasText


PromotteursProjectStyle = ParagraphStyle(name='PromotteursProjectStyle',
                                  fontName="Times-Roman",
                                  fontSize=16,
                                  leading=12,
                                  alignment=TA_LEFT)
DescritpionProjectStyle = ParagraphStyle(name='DescritpionProjectStyle',
                                  fontName="Times-Roman",
                                  fontSize=16,
                                  leading=12,
                                  alignment=TA_CENTER)

PhraseProjectStyle = ParagraphStyle(name='PromotteursProjectStyle',
                                  fontName="Times-Roman",
                                  fontSize=35,
                                  leading=12,
                                  alignment=TA_CENTER,
                                  spaceAfter=3)

PlanAffaireProjectStyle = ParagraphStyle(name='PlanAffaireProjectStyle',
                                  fontName="Times-Roman",
                                  fontSize=40,
                                  leading=10,
                                  alignment=TA_CENTER,
                                  spaceAfter=3)

Promotterus2ProjectStyle = ParagraphStyle(name='Promotterus2ProjectStyle',
                                  fontName="Times-Roman",
                                  fontSize=25,
                                  leading=10,
                                  alignment=TA_CENTER,
                                  spaceAfter=3)
PlanAffaireProjectStyle2 = ParagraphStyle(name='PlanAffaireProjectStyle',
                                  fontName="Times-Roman",
                                  fontSize=30,
                                  leading=10,
                                  alignment=TA_CENTER,
                                  spaceAfter=3)

PromotteursProjectStyle2 = ParagraphStyle(name='PromotteursProjectStyle2',
                                  fontName="Times-Roman",
                                  fontSize=32,
                                  leading=10,
                                  alignment=TA_LEFT,
                                  spaceAfter=3)
                   
PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
pageinfo = "platypus example"
e=Etude.getEtude("haussema")
Title = str(e.titre.upper())

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Italic',50)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-200, Title)
    canvas.setFont('Times-Roman',10)
    canvas.drawString(inch, 0.75 * inch,"Genéré par MasterCOM Software - Tous droits réservés")
    canvas.restoreState()
    
def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch,"Page %d " % (doc.page))
    canvas.restoreState()
    
def go(etude , numeroVersion):
    # page de garde ..
    doc = SimpleDocTemplate("projet.pdf")
    Story = [Spacer(1,2*inch)]
    style = styles["Normal"]
    Story.append(Spacer(1,4*cm))
    projet = "Projet"
    p= Paragraph(projet, PhraseProjectStyle)
    Story.append(p)
    Story.append(Spacer(1,1*cm))
    description  = str(etude.description)
    p= Paragraph(description, DescritpionProjectStyle)
    Story.append(p)
    listPromotteurs = etude.listPromotteurs
    k = []
    Story.append(Spacer(1,9*cm))
    pr = "Promotteurs :"
    p= Paragraph(pr, PromotteursProjectStyle)
    Story.append(p)
    for row in listPromotteurs:
        nom= str(row.nom)
        prenom = str(row.prenom)
        np = nom.upper()+ " " +prenom
        p= Paragraph(np, PromotteursProjectStyle)
        Story.append(p)
    # contenu general
    Story.append(Spacer(1,3*cm)) 
    pr = "Plan d'Affaire "
    p= Paragraph(pr, PlanAffaireProjectStyle)
    Story.append(p)
    
    Story.append(Spacer(1,3*cm)) 
    pr = "Promotteurs :  "
    p= Paragraph(pr, PromotteursProjectStyle2)
    Story.append(p)
    Story.append(Spacer(1,3*cm)) 
    for row in listPromotteurs:
        nom= str(row.nom)
        prenom = str(row.prenom)
        np = nom.upper()+ " " +prenom
        p= Paragraph(np, Promotterus2ProjectStyle)
        Story.append(p)
        Story.append(Spacer(1,1*cm))
    Story.append(Spacer(1,3*cm))
    pr = "Societe : " + etude.titre
    p= Paragraph(pr, PromotteursProjectStyle2)
    Story.append(p)
    Story.append(Spacer(1,3*cm))
    cout = 0 
    for row in etude.listInvestissements : 
        cout = cout + row.prixTotal
    Story.append(Spacer(1,3*cm))
    pr = "Cout d'investissement : "
    p= Paragraph(pr, PlanAffaireProjectStyle)
    Story.append(p)
    Story.append(Spacer(1,1*cm))
    pr = str(cout) + " DT"
    p= Paragraph(pr, PlanAffaireProjectStyle)
    Story.append(p)
    Story.append(Spacer(1,5*cm))
    
    style = styles["Heading1"]
    pr = "A-Synthése :"
    p= Paragraph(pr, style)
    Story.append(p)
    
    style = styles["Heading2"]
    pr = "1-PROMOTEUR :"
    p= Paragraph(pr, style)
    Story.append(p)
    style = styles["Normal"]
    pr = "Nom ou Raison Social :"
    p= Paragraph(pr, style)
    Story.append(p)
    for row in listPromotteurs:
        style = styles["Normal"]
        pr = row.nom + "   " + row.prenom
        p= Paragraph(pr, style)
        Story.append(p)
        
    '''
    for i in range(100):
        bogustext = ("Paragraph number %s. " % i) *20
        p = Paragraph(bogustext, style)
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))
    '''
    
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    
if __name__ == "__main__":
    go(e , 1)