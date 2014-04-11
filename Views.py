#!/usr/bin/python2.7
# -*-coding:UTF-8-*-
'''
Created on 10 mars 2014

@author: Haussem
'''

from PyQt4 import QtGui,QtCore,uic
from Models import *
import psycopg2
import sys
from PyQt4.QtSql import * 
from time import time,sleep
from PyQt4.QtGui import QMessageBox
import struct,datetime
from PyQt4.QtCore import QObject, SIGNAL, Qt, QLocale, QLibraryInfo, QTranslator
from ctypes.macholib import framework


class PaletteTableModel(QtCore.QAbstractTableModel):
    def __init__(self,element = [[]],headers =[],parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._element=element
        self._headers=headers

     
    def rowCount(self,parent): 
        try: 
            return len(self._element)
        except:
            return 0
    def columnCount(self,parent):
        try:
            return len(self._element[0])
        except :
            return 0
    
    def headerData(self,section,orientation,role):
        if role==QtCore.Qt.DisplayRole:
            if orientation==QtCore.Qt.Horizontal:
                return self._headers[section]  
            #else:
                #return QtCore.QString("Credit %1").arg(section+1) 
            
    def data(self,index,role):
        if role==QtCore.Qt.ToolTipRole:
            row=index.row
            return "Crédit"
        if role==QtCore.Qt.EditRole:
            row=index.row()
            column=index.column()
            return self._element[row][column]
        if role==QtCore.Qt.DisplayRole:
            row=index.row()
            column=index.column()
            value=self._element[row][column]
            return value 
        if role == Qt.BackgroundRole:
            if index.row() % 2 == 0:
                return QtGui.QBrush(Qt.blue)
            else:
                return QtGui.QBrush(Qt.gray)
        if role==QtCore.Qt.FontRole:
            font=QtGui.QFont("Segoe UI gras ")
            font.setPixelSize(15)
            
            return font
        if role == QtCore.Qt.ForegroundRole:
            brush = QtGui.QBrush()
            
            brush.setColor(QtGui.QColor("black"))
            return brush    
             
    def setData(self,index,value,role=QtCore.Qt.EditRole):
        if role==QtCore.Qt.EditRole:
            row =index.row()
            column=index.column()
            ch=(value)
            
            self._element[row][column]=ch
            self.dataChanged.emit(index,index)
            return True
                
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable

        


class Node(object):
    
    def __init__(self,name,parent=None):
        self._name=name
        self._children=[]
        self._parent=parent
         
        if parent is not None:
            parent.addChild(self)
             
    def addChild(self,child):
        self._children.append(child)
          
    def name(self):
        return self._name
    def child(self,row): 
        return self._children[row]
    def childCount(self):
        return len(self._children)
     
    def parent(self):
        return self._parent
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
         
    def log(self,tabLevel=-1):
        output=""
        tabLevel+=1
         
        for i in range(tabLevel):
            output+="\t"
             
        output +="|---------"+ self._name+"\n"   
        for child in self._children:
            output += child.log(tabLevel) 
             
        tabLevel-=1
        output+="\n"
        return output      
    def __repr__(self):
        return self.log()
class SceneGraphModel(QtCore.QAbstractItemModel):
    def __init__(self,root,parent=None):
        super(SceneGraphModel,self).__init__(parent)
        self._rootNode=root
    def rowCount(self,parent):
        if not parent.isValid():
            parentNode=self._rootNode
        else :
            parentNode=parent.internalPointer()
            
        return parentNode.childCount()        
            
    def columnCount(self,parent):
        return 1
    
    def data(self,index,role):
        if not index.isValid():
            return None
        node=index.internalPointer()
        if role==QtCore.Qt.DisplayRole:
            return node.name()
        if role==QtCore.Qt.FontRole:
            font=QtGui.QFont("Segoe UI gras ")
            font.setPixelSize(20)
            
            return font
        if role == QtCore.Qt.ForegroundRole:
            brush = QtGui.QBrush()
            
            brush.setColor(QtGui.QColor("black"))
            return brush
        
    
    def headerData(self,section,orientation,role):
        return "Haussem"
    
    def flags(self,index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def parent(self,index):
        node=index.internalPointer()
        parentNode=node.parent()
        if parentNode==self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)
    def index(self,row,column,parent):
        if not parent.isValid():
            parentNode= self._rootNode
        else :
            parentNode=parent.internalPointer()
            
        childItem =parentNode.child(row)   
                     
        if childItem:
            return self.createIndex(row, column, childItem)
        else :
            return QtCore.QModelIndex()


class sourceModels(QtCore.QAbstractListModel):
    ComboIdRole = QtCore.Qt.UserRole + 1
    def __init__(self,colors = [],parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors=colors
         
        
    def rowCount(self,parent):
        return len(self.__colors)
    def data(self,index,role):
        if role==QtCore.Qt.EditRole:
            return self.__colors[index.row()].name()
        if role ==QtCore.Qt.ToolTipRole:
            return "Mex code: "+self.__colors[index.row()].name()
        
        if role==QtCore.Qt.DisplayRole:
            row=index.row()
            value=self.__colors[row]
            return value
        
        



     
        

class PaletteListModel(QtCore.QAbstractListModel):
    def __init__(self,colors = [[]],headers =[],parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__colors=colors
       
    def columnCount(self,parent): 
        return 0

     
    def rowCount(self,parent): 
        return len(self.__colors)
    
    
    
    
    
    

            
            
   # def insertRows(self,position,rows,parent=QtCore.QModelIndex()):
     #   self.beginInsertRows(parent,position,position+rows-1)
     #   for i in range(rows):
       #     defaultValues=[QtGui.QColor("#000000") for j in range(self.columnCount(None))]
        #    self.__colors.insert(position, defaultValues)
       # self.endInsertRows()
       # return True  
    
   # def insertColumns(self,position,columns,parent=QtCore.QModelIndex()):
      #  self.beginInsertColumns(parent,position,position+rows-1)
      #  rowCount=len(self._colors)
       # for i in range(columns):
         #   for j in range(rowCount): 
          #      self.__colors[j].insert(position, QtGui.QColor("#000000"))
      #  self.endInsertColumns()
       # return True  
    
         
    def data(self,index,role):
        if role==QtCore.Qt.EditRole:
            row=index.row()
            

            return self.__colors[row]
        if role==QtCore.Qt.FontRole:
            font=QtGui.QFont("Segoe UI gras")
            font.setPixelSize(20)
            
            return font
        if role == QtCore.Qt.ForegroundRole:
            brush = QtGui.QBrush()
            
            brush.setColor(QtGui.QColor("black"))
            return brush    
        if role ==QtCore.Qt.ToolTipRole:
            row=index.row()
            
            return "Etude: "+self.__colors[row]
        
        if role==QtCore.Qt.DisplayRole:
            row=index.row()
            column=index.column()
            value=self.__colors[row]
            return value 
        if role==QtCore.Qt.DecorationRole:
            
            
            pixmap=QtGui.QPixmap(26,26)
            pixmap.load("E:\\Users\\HA\\workspace\\Projet\\copy-icon.png")
            icon=QtGui.QIcon(pixmap)
            return icon 
    def setData(self,index,value,role=QtCore.Qt.EditRole):
        if role==QtCore.Qt.EditRole:
            row =index.row()
           
            color=value
            
            self.__colors[row]=color
            self.dataChanged.emit(index,index)
                
            return False
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable
#|QtCore.Qt.ItemIsEditable


InterfaceEtudeBase, InterfaceEtudeForm = uic.loadUiType('interfaceEtude.ui')
class interfaceEtude(InterfaceEtudeBase,InterfaceEtudeForm):
    
    """
    - Si UiMaFenetre, importe depuis le designer a ete construit comme QMainWindow, 
        alors MaFenetre doit heriter de QMainWindow
    - si UiMafFenetre est construit dans designer comme un QWidget, alors MaFenetre doit     
        heriter de QWidget"""
    def __init__(self, parent=None):
        super(InterfaceEtudeBase,self).__init__(parent)
        self.setupUi(self)
        global etude
        
       
        etude=Etude.getEtude(Nom)
        global version
        version=Version.getVersion(NomVersion,etude.idEtude)
        
        
        self.Titre.setText(etude.titre)
        self.Type.setText(etude.type)
        self.Secteur.setText(etude.secteur)
        self.Duree.setText(str(etude.dureeEtude))
        investissement=WidgetInvestissement()
        self.verticalLayout_2.addWidget(investissement)
        QObject.connect(self.uiOuvrir,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiOuvrir,SIGNAL("released()"),self.buttonPressed)
        QObject.connect(self.uiOuvrir,SIGNAL("clicked()"),self.ouvrir)
        QObject.connect(self.uiModifier,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifier,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier,SIGNAL("clicked()"),self.modifier)
        QObject.connect(self.uiRapporter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiRapporter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimer)
        QObject.connect(self.uiQuitter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiQuitter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiQuitter,SIGNAL("released()"),self.quitter)
        QObject.connect(self.uiAccueil,SIGNAL("pressed()"),self.iconPressed)
        QObject.connect(self.uiAccueil,SIGNAL("released()"),self.iconReleased)
        QObject.connect(self.uiAccueil,SIGNAL("clicked()"),self.accueil)
        QObject.connect(self.uiInvestissement,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiInvestissement,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiFinancement,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiFinancement,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiPromotteur,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiPromotteur,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiInvestissement,SIGNAL("clicked()"),self.inserer1)
        QObject.connect(self.uiFinancement,SIGNAL("clicked()"),self.inserer2)
        QObject.connect(self.uiPromotteur,SIGNAL("clicked()"),self.inserer3)
        self.uiInvestissement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiPrevision,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiPrevision,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.Valider)
        QObject.connect(self.uiPrevision,SIGNAL("clicked()"),self.Prevision)
        QObject.connect(self.uiArticle,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiArticle,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiProduit,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiProduit,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiCharge,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiCharge,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiArticle,SIGNAL("clicked()"),self.inserer4)
        QObject.connect(self.uiProduit,SIGNAL("clicked()"),self.inserer5)
        QObject.connect(self.uiCharge,SIGNAL("clicked()"),self.inserer6)
        
        
        
            
        
   
    def ouvrir(self):
        Ouvrir=ouvrirEtude()
        Ouvrir.exec_()
    def quitter(self):
        reply=QMessageBox.information(self,"Quitter","voulez-vous vraiment quitter l'application ?",QMessageBox.Yes,QMessageBox.No)
        if reply==QtGui.QMessageBox.Yes:
            
            window.close()
     
    def accueil(self):
        reply=QMessageBox.information(self,"Quitter","voulez-vous vraiment quitter cet Etude ?",QMessageBox.Yes,QMessageBox.No)
        if reply==QtGui.QMessageBox.Yes:
            self.aficher_p = MaWidget(self)
            window.setCentralWidget(self.aficher_p)
         
        
    def supprimer(self):
        reply=QMessageBox.information(self,"Suppression","voulez-vous vraiment supprimer cet Etude ?",QMessageBox.Yes,QMessageBox.No)
        if reply==QtGui.QMessageBox.Yes:
            b=etude.supprimer()
        if (b==True):
            QMessageBox.information(self,"Suppression","l'Etude est supprimé avec succée !",QMessageBox.Ok)
            self.aficher_p = MaWidget(self)
            window.setCentralWidget(self.aficher_p)
        
           
                
    def Valider(self):
        fi=etude.financement
        inv=etude.listInvestissements
        p=etude.listPromotteurs

        
        if (fi.idFinancement!=0 and len(inv)!=0 and len(p)!=0):
            montantTotalFi=fi.montantPropre
            fin=Financement(fi.idFinancement,fi.montantPropre,etude.idEtude)
            cre=fin.listCredits
            print fin.montantPropre
            for c in cre:
                print c.montant
                
                montantTotalFi=montantTotalFi+c.montant
            print "montantFinancement="+str(montantTotalFi)
            montantTotalInv=0
            
            for i in inv:
                
                montantTotalInv=montantTotalInv+float(i.prixTotal)
            print "montantInvestissement="+str(montantTotalInv)
            if montantTotalFi==montantTotalInv:
                
                if self.uiValider.text()=="Valider":
                    self.uiArticle.setEnabled(True)
                    self.uiProduit.setEnabled(True)
                    self.uiCharge.setEnabled(True)
                    self.uiPrevision.setEnabled(True)  
                    self.inserer4()
                    self.uiProduit.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
                    self.uiCharge.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
                    self.uiPrevision.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
                    self.uiInvestissement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
                    self.uiFinancement.setStyleSheet(" background-color:rgb(51, 51, 51);")
                    self.uiPromotteur.setStyleSheet(" background-color:rgb(51, 51, 51);")
                    self.uiInvestissement.setStyleSheet(" background-color:rgb(51, 51, 51);")
                    self.uiInvestissement.setEnabled(False)
                    self.uiFinancement.setEnabled(False)
                    self.uiPromotteur.setEnabled(False)
                    self.uiValider.setText("Modifier")
                    self.uiValider.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(170, 0, 0);")
                else :
                    self.inserer1()
                    self.uiArticle.setEnabled(False)
                    self.uiProduit.setEnabled(False)
                    self.uiCharge.setEnabled(False)
                    self.uiPrevision.setEnabled(False)  
                    self.uiInvestissement.setEnabled(True)
                    self.uiFinancement.setEnabled(True)
                    self.uiPromotteur.setEnabled(True)
                    self.uiArticle.setStyleSheet("background-color:rgb(51, 51, 51);")
                    self.uiProduit.setStyleSheet("background-color:rgb(51, 51, 51);")
                    self.uiCharge.setStyleSheet("background-color:rgb(51, 51, 51);")
                    self.uiPrevision.setStyleSheet("background-color:rgb(51, 51, 51);")
                    self.uiInvestissement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
                    self.uiFinancement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
                    self.uiPromotteur.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
                    self.uiValider.setText(str("Valider"))
                    self.uiValider.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(0, 170, 0);")
                
            else :
                QMessageBox.information(self,"verifivation","le montant finale de votre financements n'est pas egale au montant finale de votre investissements",QMessageBox.Ok)
        
        
        elif (len(inv)==0):
            QMessageBox.information(self,"verifivation","il faut avoir au  moins un invetissement",QMessageBox.Ok)    
        elif (fi.idFinancement==0):
            QMessageBox.information(self,"verifivation","il faut avoir au  moins un moyen de financement",QMessageBox.Ok)
        elif (len(p)==0):
            QMessageBox.information(self,"verifivation","il faut avoir au  moins un promotteur",QMessageBox.Ok)                 
        
        
 
            
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
                    
    def modifier(self):
        modifierEtude=WidgetModifierEtude()
        modifierEtude.exec_()
        self.Titre.setText(etude.titre)
        self.Type.setText(etude.type)
        self.Secteur.setText(etude.secteur)
        self.Duree.setText(str(etude.dureeEtude))
        
                        
    def inserer1(self):
        self.uiInvestissement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        investissement=WidgetInvestissement()
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(investissement) 
        self.uiFinancement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiPromotteur.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")   
        self.uiInvestissement.Enable=False
    def inserer2(self):
        self.uiFinancement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        financement=WidgetFinancement()
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(financement)
        self.uiInvestissement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiPromotteur.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")       
        self.uiFinancement.Enable=False 
        
    def inserer3(self):
        self.uiPromotteur.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        promotteur=WidgetPromotteur()
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(promotteur)
        self.uiFinancement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiInvestissement.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")        
        self.uiPromotteur.Enable=False
        
    def inserer4(self):
        self.uiArticle.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        article=WidgetArticle()
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(article)
        self.uiProduit.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiCharge.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiPrevision.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")        
        self.uiArticle.Enable=False 
        
    def inserer5(self):
        self.uiProduit.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        produit=WidgetProduit()
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(produit)
        self.uiArticle.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiCharge.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiPrevision.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")        
        self.uiProduit.Enable=False 
        
    def inserer6(self):
        self.uiCharge.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        charge=WidgetCharge()
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(charge)
        self.uiArticle.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiProduit.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiPrevision.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")        
        self.uiCharge.Enable=False  
    def Prevision(self):
        self.uiPrevision.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(168, 168, 168);")
        prevision=WidgetPrevision()
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(prevision)
        self.uiArticle.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiProduit.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")
        self.uiCharge.setStyleSheet("color: rgb(255, 255, 255); border:rgb(255, 255, 255); background-color:rgb(51, 51, 51);")        
        self.uiPrevision.Enable=False
                              
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font) 
     
    def iconPressed(self):
        #a=QtGui.QAbstractButton
        s=QtCore.QSize(20,20)
        self.uiAccueil.setIconSize(s)
        
    def iconReleased(self):
        s=QtCore.QSize(26,26)
        self.uiAccueil.setIconSize(s)


previsionBase, previsionForm = uic.loadUiType('intercafeprevision.ui')
class WidgetPrevision(previsionBase,previsionForm):
    indexes1=-1
    indexes2=-1
    indexes3=-1
    def __init__(self, parent=None):
        super(previsionBase,self).__init__(parent)
        self.setupUi(self)
        
        QObject.connect(self.uiAjouterA,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouterA,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouterA,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimerA,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimerA,SIGNAL("released()"),self.buttonReleased)
        #QObject.connect(self.uiSupprimerA,SIGNAL("clicked()"),self.supprimerInvestissement)
        QObject.connect(self.uiModifierA,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifierA,SIGNAL("released()"),self.buttonReleased)
        #QObject.connect(self.uiModifierA,SIGNAL("clicked()"),self.modifierInvestissement)
        QObject.connect(self.uiAjouterV,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouterV,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouterV,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimerV,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimerV,SIGNAL("released()"),self.buttonReleased)
        #QObject.connect(self.uiSupprimerV,SIGNAL("clicked()"),self.supprimerInvestissement)
        QObject.connect(self.uiModifierV,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifierV,SIGNAL("released()"),self.buttonReleased)
        #QObject.connect(self.uiModifierV,SIGNAL("clicked()"),self.modifierInvestissement)
        QObject.connect(self.uiAjouterP,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouterP,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouterP,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimerP,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimerP,SIGNAL("released()"),self.buttonReleased)
        #QObject.connect(self.uiSupprimerP,SIGNAL("clicked()"),self.supprimerInvestissement)
        QObject.connect(self.uiModifierA,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifierA,SIGNAL("released()"),self.buttonReleased)
        #QObject.connect(self.uiModifierP,SIGNAL("clicked()"),self.modifierInvestissement)
        self.achatArtice.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.venteArticle.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.personnel.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        version.listProduitsFinis=version.getListProduitsFinis()
        self.remplissageAchatArtice()
        self.remplissageVenteArticle()
        self.remplissagePersonnel()
        self.achatArtice.setColumnWidth(1,  132)
        self.achatArtice.setColumnWidth(2,  132)
        self.achatArtice.setColumnWidth(3,  132)
        self.achatArtice.setColumnWidth(4,  132)
        self.achatArtice.setColumnWidth(5,  132)
        self.venteArticle.setColumnWidth(1,  132)
        self.venteArticle.setColumnWidth(2,  132)
        self.venteArticle.setColumnWidth(3,  132)
        self.venteArticle.setColumnWidth(4,  132)
        self.venteArticle.setColumnWidth(5,  132)
        self.personnel.setColumnWidth(1,  124)
        self.personnel.setColumnWidth(2,  124)
        QObject.connect(self.achatArtice,SIGNAL("clicked(QModelIndex)"),self.clic)
        QObject.connect(self.venteArticle,SIGNAL("clicked(QModelIndex)"),self.clic)
        QObject.connect(self.personnel,SIGNAL("clicked(QModelIndex)"),self.clic)
            
    def clic(self,index):
        
        if self.sender().objectName()=="achatArtice":
            self.indexes1= index.row()
            global ind1
            ind1=self.indexes1
            self.indexes2=-1
            self.indexes3=-1
            print "indexes1=" + str(self.indexes1)
            print "indexes2=" + str(self.indexes2)
            print "indexes3=" + str(self.indexes3)
            
            
            global ar
            ar=version.listAritcles[self.indexes1]
            #ar=Article(row[0],row[1], row[2], row[3], row[4], row[5],row[6])  
            
        elif self.sender().objectName()=="venteArticle":
            self.indexes2= index.row()
            global ind2
            ind2=self.indexes2
            
            self.indexes1=-1
            self.indexes3=-1
            print "indexes2=" + str(self.indexes2)
            print "indexes1=" + str(self.indexes1)
            print "indexes3=" + str(self.indexes3)
            
            global pro
            pro=version.listProduitsFinis[self.indexes2]
            #pro=Article(row[0],row[1], row[2], row[3], row[4], row[5],row[6]) 
            
        elif self.sender().objectName()=="personnel":
            self.indexes3= index.row()
            global ind3
            ind3=self.indexes3
            
            self.indexes1=-1
            self.indexes2=-1
            print "indexes2=" + str(self.indexes2)
            print "indexes1=" + str(self.indexes1)
            print "indexes3=" + str(self.indexes3)
            
            #row=version.listChargePersonnel[self.indexes3]
            global personnel
            personnel=version.listChargePersonnel[self.indexes3]
            #personnel=ChargePersonnel(row[0],row[1], row[2],row[3]) 
               
    def inserer(self):
        if (self.indexes1>-1 and len(self.achatArtice.selectedIndexes())!=0):
            
            
            previsionA=previsionAchat()
            previsionA.exec_()
            
        elif (self.indexes2>-1 and len(self.venteArticle.selectedIndexes())!=0):
            
            
            previsionV=previsionVente()
            previsionV.exec_()
        elif (self.indexes3>-1 and len(self.personnel.selectedIndexes())!=0):
            
            
            previsionP=previsionPersonnel()
            previsionP.exec_()     
                
        
    def  remplissageAchatArtice(self):
            
            
        headers=["designation", "type","fournisseur","prix d'achat","unite de mesure"]
        #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
        k=[]
        for row in version.listAritcles :
            s=(row.designation,row.type,row.fournisseur,row.prixAchat,row.uniteMesure)
            k.append(s)
        model =PaletteTableModel(k,headers)     
        self.achatArtice.setModel(model)
            
    def  remplissageVenteArticle(self):
            
            
        headers=["designation", "type","fournisseur","prix de vente","unite de mesure"]
        #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
        k=[]
        for row in version.listProduitsFinis :
            s=(row.designation,row.type,row.fournisseur,row.prixVente,row.uniteMesure)
            k.append(s)
        model =PaletteTableModel(k,headers)
        self.venteArticle.setModel(model)

            
    def  remplissagePersonnel(self):
        headers=["Poste", "Salaire"]
        k=[]
        for row in version.listChargePersonnel :
            s=(row.designation,row.salaire)
            k.append(s)
        model =PaletteTableModel(k,headers)    
        self.personnel.setModel(model)
        
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    


previsionAchatBase, previsionAchatForm = uic.loadUiType('previsionAchat.ui')
class previsionAchat(previsionAchatBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(previsionAchatBase,self).__init__(parent)
        self.setupUi(self)
        self.uiDesignation.setText(ar.designation)
        self.uiType.setText(ar.type)
        self.uiFournisseur.setText(ar.fournisseur)
        self.uiPrix.setText(str(ar.prixAchat))
        self.uiUnite.setText(str(ar.uniteMesure))
        self.uiValeur1.setEnabled(False)
        self.uiValeur2.setEnabled(False)
        self.uiTaux.setEnabled(False)
        self.tableView.setEnabled(False)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.close)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        QObject.connect(self.radioButton_1,SIGNAL("clicked()"),self.activer)
        QObject.connect(self.radioButton_2,SIGNAL("clicked()"),self.activer)
        QObject.connect(self.radioButton_3,SIGNAL("clicked()"),self.activer)
    def activer(self):
        if self.radioButton_1.isChecked() :
            self.uiValeur1.setEnabled(True)
            self.uiValeur2.setEnabled(False)  
            self.uiTaux.setEnabled(False)
            self.tableView.setEnabled(False)       
        elif self.radioButton_2.isChecked() :
            self.uiValeur1.setEnabled(False)
            self.uiValeur2.setEnabled(True)  
            self.uiTaux.setEnabled(True)
            self.tableView.setEnabled(False) 
        elif self.radioButton_3.isChecked() :
            self.uiValeur1.setEnabled(False)
            self.uiValeur2.setEnabled(False)  
            self.uiTaux.setEnabled(False)
            self.tableView.setEnabled(True)       
            
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
     
previsionVenteBase, previsionVenteForm = uic.loadUiType('previsionVente.ui')
class previsionVente(previsionVenteBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(previsionVenteBase,self).__init__(parent)
        self.setupUi(self)
        self.uiDesignation.setText(pro.designation)
        self.uiType.setText(pro.type)
        self.uiPrix.setText(str(pro.prixVente))
        if pro.type=="Fini":
            self.uiFournisseur.setText(pro.fournisseur)
            self.uiUnite.setText(pro.uniteMesure)
        self.uiValeur1.setEnabled(False)
        self.uiValeur2.setEnabled(False)
        self.uiTaux.setEnabled(False)
        self.tableView.setEnabled(False)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.close)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        QObject.connect(self.radioButton_1,SIGNAL("clicked()"),self.activer)
        QObject.connect(self.radioButton_2,SIGNAL("clicked()"),self.activer)
        QObject.connect(self.radioButton_3,SIGNAL("clicked()"),self.activer)
    def activer(self):
        if self.radioButton_1.isChecked() :
            self.uiValeur1.setEnabled(True)
            self.uiValeur2.setEnabled(False)  
            self.uiTaux.setEnabled(False)
            self.tableView.setEnabled(False)       
        elif self.radioButton_2.isChecked() :
            self.uiValeur1.setEnabled(False)
            self.uiValeur2.setEnabled(True)  
            self.uiTaux.setEnabled(True)
            self.tableView.setEnabled(False) 
        elif self.radioButton_3.isChecked() :
            self.uiValeur1.setEnabled(False)
            self.uiValeur2.setEnabled(False)  
            self.uiTaux.setEnabled(False)
            self.tableView.setEnabled(True)       
            
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)  
        
previsionPersonnelBase, previsionPersonnelForm = uic.loadUiType('previsionPersonnel.ui')
class previsionPersonnel(previsionPersonnelBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(previsionPersonnelBase,self).__init__(parent)
        self.setupUi(self)
        self.uiPoste.setText(personnel.designation)
        self.uiSalaire.setText(str(personnel.salaire))
        self.uiValeur1.setEnabled(False)
        self.uiValeur2.setEnabled(False)
        self.uiTaux.setEnabled(False)
        self.tableView.setEnabled(False)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.close)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        QObject.connect(self.radioButton_1,SIGNAL("clicked()"),self.activer)
        QObject.connect(self.radioButton_2,SIGNAL("clicked()"),self.activer)
        QObject.connect(self.radioButton_3,SIGNAL("clicked()"),self.activer)
    def activer(self):
        if self.radioButton_1.isChecked() :
            self.uiValeur1.setEnabled(True)
            self.uiValeur2.setEnabled(False)  
            self.uiTaux.setEnabled(False)
            self.tableView.setEnabled(False)       
        elif self.radioButton_2.isChecked() :
            self.uiValeur1.setEnabled(False)
            self.uiValeur2.setEnabled(True)  
            self.uiTaux.setEnabled(True)
            self.tableView.setEnabled(False) 
        elif self.radioButton_3.isChecked() :
            self.uiValeur1.setEnabled(False)
            self.uiValeur2.setEnabled(False)  
            self.uiTaux.setEnabled(False)
            self.tableView.setEnabled(True)       
            
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)              
            
avantBase, avantForm = uic.loadUiType('avant_de_commencer.ui')
class avantCommencer(avantBase,avantForm):
    
    def __init__(self, parent=None):
        super(avantBase,self).__init__(parent)
        self.setupUi(self)
        
pourquoiBase, pourquoiForm = uic.loadUiType('pourquoi.ui')
class pourquoi(pourquoiBase,pourquoiForm):
    
    def __init__(self, parent=None):
        super(pourquoiBase,self).__init__(parent)
        self.setupUi(self)    
        

                  




        

      

               
            
        
    

investissementBase, investissementForm = uic.loadUiType('investissement.ui')
class WidgetInvestissement(investissementBase,investissementForm):
    indexes=-1
    def __init__(self, parent=None):
        super(investissementBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimerInvestissement)
        QObject.connect(self.uiModifier,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifier,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier,SIGNAL("clicked()"),self.modifierInvestissement)
        
        self.remplissageTableView()
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        QObject.connect(self.tableView,SIGNAL("clicked(QModelIndex)"),self.clic)
        QObject.connect(self.tableView,SIGNAL("doubleClicked(QModelIndex)"),self.afficherTableauAm)
        
        
    def afficherTableauAm(self,index):
        self.indexes= index.row()
       
        global inv
        
        inv=etude.listInvestissements[self.indexes]
        
             
        tableau=tableauAmortissement()
        tableau.exec_()
     
        
    def clic(self,index):
        
        self.indexes= index.row()
        
        global ind
        ind=self.indexes
    
    
    def  remplissageTableView(self):
            
            
            headers=["Designation", "Type","Fournisseur","Prix","Pays","Quantite","Prix total","Type amortissement","Dure vie","Taux amortissement","date d'achat"]
            #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
            row = []
            for nod in etude.listInvestissements :
                
                s =(nod.designation,nod.type,nod.fournisseur,nod.prix,nod.pays,nod.quantite,nod.prixTotal,nod.typeAmortissement,nod.dureVie,nod.tauxAmortissement,nod.dateAchat)
                row.append(s)
            
            model =PaletteTableModel(row,headers)     
            self.tableView.setModel(model)
            
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font) 
        
    def inserer(self):
        ajout=AjoutInvestissement()
        ajout.exec_()
        self.remplissageTableView()
        
        
    def modifierInvestissement(self):
        
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            #print self.indexes
            global inv
            inv=etude.listInvestissements[self.indexes]
            modifier=ModifierInvestissement()
            modifier.exec_()
            self.remplissageTableView()
            
    def supprimerInvestissement(self):
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            #print self.indexes
            
            inv=etude.listInvestissements[self.indexes]
            reply=QMessageBox.information(self,"Suppression","voulez-vous vraiment supprimer l'invetissement : "+ str(inv.idInvestissement)+" ?",QMessageBox.Yes,QMessageBox.No)
            if reply==QtGui.QMessageBox.Yes:
                del etude.listInvestissements[self.indexes]
                inv.supprimer()
                QMessageBox.information(self,"Suppression","l'investissement est supprimé avec succée",QMessageBox.Ok)
                self.remplissageTableView()          
            
AjoutInVBase, AjoutInVForm = uic.loadUiType('ajoutInvestissement.ui')
class AjoutInvestissement(AjoutInVBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutInVBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        QObject.connect(self.uiPrix,SIGNAL("valueChanged(double)"),self.calculPrixTotal1)
        QObject.connect(self.uiQuantite,SIGNAL("valueChanged(int)"),self.calculPrixTotal2)
        QObject.connect(self.uiDureVie,SIGNAL("valueChanged(int)"),self.addItem)
        QObject.connect(self.uiTypeAmortissement,SIGNAL("currentIndexChanged(QString)"),self.calculTaux)
        item=["","type1","type2","type3"]
        self.uiType.addItems(item)
        
        
    def calculPrixTotal1(self,value):
        
        c=value*self.uiQuantite.value()
        self.uiPrixTotal.setText(str(c))
    def calculPrixTotal2(self,value):
        
        c=value*self.uiPrix.value()
        self.uiPrixTotal.setText(str(c)) 
        
    def addItem(self,value):
        list1 = [
            self.tr("lineaire")
            ]
        list2 = [
            self.tr(""),
            self.tr("lineaire"),
            self.tr("degressif")
            ]
        
        if (value<3):
            self.uiTaux.setEnabled(False)
            c=100/value
            self.uiTaux.setText(str(c))
            self.uiTypeAmortissement.clear()
            self.uiTypeAmortissement.addItems(list1)
           
        else :
            self.uiTaux.setEnabled(True)
            self.uiTaux.setText("") 
            self.uiTypeAmortissement.clear()
            self.uiTypeAmortissement.addItems(list2)
            
            
                   
    def calculTaux(self):
        
        if self.uiTypeAmortissement.currentText()=="lineaire":
            print "lol"
            self.uiTaux.setEnabled(False)
            c=100/self.uiDureVie.value()
            self.uiTaux.setText(str(c))
        elif self.uiTypeAmortissement.currentText()=="degressif" :
            self.uiTaux.setEnabled(True)
            self.uiTaux.setText("")                  
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiType.currentText()=="" or self.uiDesignation.text()=="" or self.uiPrix.value()==0 or self.uiFournisseur.text()=="" or self.uiPays.text()=="" or self.uiQuantite.value()==0 or self.uiTypeAmortissement.currentText()=="" or self.uiDureVie.value()==0 or self.dateEdit.date()<datetime.datetime.now().date()):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            
            
            investissement=Investissement(None,str(self.uiDesignation.text()),str(self.uiType.currentText()),str(self.uiFournisseur.text()),str(self.uiPays.text()),self.uiPrix.value(),etude.idEtude,self.uiQuantite.value(),float(self.uiPrixTotal.text()),str(self.uiTypeAmortissement.currentText()),self.uiDureVie.value(),float(self.uiTaux.text()),str(self.dateEdit.date().toString("MM/dd/yyyy")))
                
            if (Investissement.verifier(investissement)==True):
                self.uiErreur.setText("la designation existe")
            else:

                investissement.ajouter()
                investissement.getIdInv()
                
                etude.listInvestissements.append(investissement)
                investissement.calculRemboursement()
                self.close()
                
                
ModifierInVBase, ModifierInVForm = uic.loadUiType('modifierInvestissement.ui')
class ModifierInvestissement(ModifierInVBase,QtGui.QDialog,):
    
    def __init__(self, parent=None):
        super(ModifierInVBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        QObject.connect(self.uiPrix,SIGNAL("valueChanged(double)"),self.calculPrixTotal1)
        QObject.connect(self.uiQuantite,SIGNAL("valueChanged(int)"),self.calculPrixTotal2)
        QObject.connect(self.uiDureVie,SIGNAL("valueChanged(int)"),self.addItem)
        QObject.connect(self.uiTypeAmortissement,SIGNAL("currentIndexChanged(QString)"),self.calculTaux)
        self.uiDesignation.setText(inv.designation)
        self.uiFournisseur.setText(inv.fournisseur)
        self.uiPays.setText(inv.pays)
        self.uiPrix.setValue(inv.prix)
        self.uiQuantite.setValue(inv.quantite)
        self.uiPrixTotal.setText(str(inv.prixTotal))
        self.uiDureVie.setValue(inv.dureVie)
        item=["","type1","type2","type3"]
        self.uiType.addItems(item)
        index=item.index(inv.type)
        self.uiType.setCurrentIndex(index)
        if inv.dureVie <3:
            self.uiTypeAmortissement.setCurrentIndex(2)
        else :
            item=["","lineaire","degressif"]
            
            index=item.index(inv.typeAmortissement)
            self.uiTypeAmortissement.setCurrentIndex(index)    
        self.uiTaux.setText(str(inv.tauxAmortissement))
        
           
    def calculPrixTotal1(self,value):
        
        c=value*self.uiQuantite.value()
        self.uiPrixTotal.setText(str(c))
    def calculPrixTotal2(self,value):
        
        c=value*self.uiPrix.value()
        self.uiPrixTotal.setText(str(c)) 
        
    def addItem(self,value):
        list1 = [
            self.tr("Lineaire")
            ]
        list2 = [
            self.tr(""),
            self.tr("lineaire"),
            self.tr("degressif")
            ]
        
        if (value<3):
            self.uiTaux.setEnabled(False)
            c=100/value
            self.uiTaux.setText(str(c))
            self.uiTypeAmortissement.clear()
            self.uiTypeAmortissement.addItems(list1)
           
        else :
            self.uiTaux.setEnabled(True)
            self.uiTaux.setText("") 
            self.uiTypeAmortissement.clear()
            self.uiTypeAmortissement.addItems(list2)
            
            
                   
    def calculTaux(self):
        
        if self.uiTypeAmortissement.currentText()=="lineaire":
            print "lol"
            self.uiTaux.setEnabled(False)
            c=100/self.uiDureVie.value()
            self.uiTaux.setText(str(c))
        elif self.uiTypeAmortissement.currentText()=="degressif" :
            self.uiTaux.setEnabled(True)
            self.uiTaux.setText("")                  
    
                   
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
         
    def inserer(self):
        
        if (self.uiType.currentText()=="" or self.uiDesignation.text()=="" or self.uiPrix.value()==0 or self.uiFournisseur.text()=="" or self.uiPays.text()=="" or self.uiQuantite.value()==0 or self.uiTypeAmortissement.currentText()=="" or self.uiDureVie.value()==0 or self.dateEdit.date()<datetime.datetime.now().date()):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            
            investissement=Investissement(inv.idInvestissement,str(self.uiDesignation.text()),str(self.uiType.currentText()),str(self.uiFournisseur.text()),str(self.uiPays.text()),self.uiPrix.value(),etude.idEtude,self.uiQuantite.value(),str(self.uiPrixTotal.text()),str(self.uiTypeAmortissement.currentText()),self.uiDureVie.value(),float(self.uiTaux.text()),str(self.dateEdit.date().toString("MM/dd/yyyy")))
            if (inv.designation != investissement.designation): 
                
                print investissement.designation 
                print investissement.idEtude 
                if (Investissement.verifier(investissement)==True):
                    self.uiErreur.setText("la designation existe")
                else:
                    #rowAncien=[inv.idInvestissement,inv.designation,inv.type,inv.fournisseur,inv.prix,inv.idEtude,inv.pays,inv.quantite,inv.prixTotal,inv.typeAmortissement,inv.dureVie,inv.tauxAmortissement]
                    
                    investissement.suppRem() 
                    investissement.calculRemboursement() 
                    del etude.listInvestissements[ind]
                    etude.listInvestissements.insert(ind,investissement)
                    investissement.modifier()
                    self.close() 
            else:
                   
                    del etude.listInvestissements[ind]
                    etude.listInvestissements.insert(ind,investissement)
                    investissement.modifier()
                    self.close()
                    investissement.suppRem() 
                    investissement.calculRemboursement() 
                    
tableauAmBase, tableauAmForm = uic.loadUiType('tableauAmortissement.ui')
class tableauAmortissement(tableauAmBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(tableauAmBase,self).__init__(parent)
        self.setupUi(self)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        headers=["id_amortissement","id_investissement","annee","base", "annuite","annuite_cumulees","vnc","nombre années restant","taux lineaire"]
        #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
        row = []
        print inv.idInvestissement
        print len(inv.listsAmortissement)
        for nod in inv.listsAmortissement :
                s =(nod.idAmortissement,nod.idInvestissement,nod.annee,nod.base,nod.annuite,nod.annuiteCumulees,nod.vnc,nod.nbrAnneeRestants,nod.tauxLineaire)
                
                row.append(s)
        
        model =PaletteTableModel(row,headers)     
        self.tableView.setModel(model)
        self.tableView.hideColumn(0)
        self.tableView.hideColumn(1)
        if inv.typeAmortissement=="lineaire" :
            self.tableView.hideColumn(7) 
            self.tableView.hideColumn(8)                                               
        
        
financementBase, financementForm = uic.loadUiType('financement.ui')
class WidgetFinancement(financementBase,financementForm):
    indexes=-1
    def __init__(self, parent=None):
        super(financementBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.insererCredit)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimerCredit)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.iconPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.iconReleased)
        QObject.connect(self.uiModifier,SIGNAL("pressed()"),self.iconPressed)
        QObject.connect(self.uiModifier,SIGNAL("released()"),self.iconReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.valider)
        QObject.connect(self.uiModifier,SIGNAL("clicked()"),self.modifierMontant)
        QObject.connect(self.uiModifier_2,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifier_2,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier_2,SIGNAL("clicked()"),self.modifierCredit)
        self.Montant.setText("0")
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        QObject.connect(self.tableView,SIGNAL("clicked(QModelIndex)"),self.clic)
        
        self.r=etude.financement
        print self.r.montantPropre
        
       
        #f=Financement(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        if self.r.idFinancement==0:
            self.Montant.setText("0")
            global f
            f=Financement(int(etude.idEtude),float(0),int(etude.idEtude))
            etude.financement.append(f)
            f.ajouter()
            
            
            
        else:
            
            
            
           
            
            self.Montant.setText(str(self.r.montantPropre))
            self.Montant.setEnabled(False)
            global f
            f=Financement(self.r.idFinancement,float(0),int(etude.idEtude))
            self.remplissageTableView()
            
        
        QObject.connect(self.tableView,SIGNAL("doubleClicked(QModelIndex)"),self.afficherTableauRm)
        
        
    def afficherTableauRm(self,index):
        self.indexes= index.row()
        
        global cre
        cre=f.listCredits[self.indexes]
        
        tableau=tableauRemboursement()
        tableau.exec_()
        
        
    def clic(self,index):
        
        self.indexes= index.row()
        
        global ind
        ind=self.indexes
          
    def  remplissageTableView(self):
        if self.r.idFinancement!=0:
            
        
            headers=["id_credit","Type","Nom du Banque","  delais de remboursement  ","taux d'interet","delais de grace","id_financement","montant"]
            row = []
            for nod in f.listCredits :
                s =(nod.idCredit,nod.type,nod.nomBanque,nod.delaisRem,nod.tauxInteret,nod.delaisGrace,nod.idFinancement,nod.montant)
                row.append(s)
            model =PaletteTableModel(row,headers)     
            self.tableView.setModel(model)
            self.tableView.hideColumn(0)
            self.tableView.hideColumn(6)
            
           
        
            
           
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font) 
        
    def valider(self):
        self.Montant.setEnabled(False)
         
        f.montantPropre=float(self.Montant.text())
        etude.financement.montantPropre=f.montantPropre
          
        f.modifier()
       
                     
              
    def modifierMontant(self):
        self.Montant.setEnabled(True)        
    def insererCredit(self):
        
        ajout=AjoutCredit()
        ajout.exec_()
        
        self.remplissageTableView()
    def modifierCredit(self):
        #x=self.clic(self.tableView.selectionModel().index.row())
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
           
            global cr
            cr=f.listCredits[self.indexes]
            modifier=ModifierCredit()
            modifier.exec_()
            self.remplissageTableView() 
            
    def supprimerCredit(self):
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            #print self.indexes
            
            cr=f.listCredits[self.indexes]
            reply=QMessageBox.information(self,"Suppression","voulez-vous vraiment supprimer ce credit ?",QMessageBox.Yes,QMessageBox.No)
            if reply==QtGui.QMessageBox.Yes:
                cr.supprimer()
                del f.listCredits[self.indexes]
                QMessageBox.information(self,"Suppression","le credit est supprimé avec succée",QMessageBox.Ok)
                self.remplissageTableView()                 
       
    def iconPressed(self):
        s=QtCore.QSize(10,10)
        self.sender().setIconSize(s)
    def iconReleased(self):
        s=QtCore.QSize(16,16)
        self.sender().setIconSize(s)
                    

AjoutCreditVBase, AjoutCreditVForm = uic.loadUiType('ajoutCredit.ui')
class AjoutCredit(AjoutCreditVBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutCreditVBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        item=["","credit1","credit2","credit3"]
        self.uiType.addItems(item)
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        
        
        if (self.uiType.currentText()=="" or self.uiNomBanque.text()=="" or self.uiDelaiR.value()==0 or self.uiTaux.value()==0 or self.uiMontant.value()==0):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            credit=Credit(None,str(self.uiType.currentText()),str(self.uiNomBanque.text()),self.uiDelaiR.value(),self.uiTaux.value(),self.uiDelaiG.value(),f.idFinancement,self.uiMontant.value())
            
            credit.ajouter()
            credit.getIdCre()
            
            f.listCredits.append(credit)
            credit.calculRemboursement()
            
            self.close()
            
        
 
 
modifierCreditVBase, modifierCreditVForm = uic.loadUiType('modifierCredit.ui')
class ModifierCredit(modifierCreditVBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(modifierCreditVBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.modifier)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        
        
        self.uiMontant.setValue(cr.montant)
        self.uiNomBanque.setText(cr.nomBanque)
        self.uiDelaiR.setValue(cr.delaisRem)
        self.uiTaux.setValue(cr.tauxInteret)
        self.uiDelaiG.setValue(cr.delaisGrace)
        item=["","credit1","credit2","credit3"]
        self.uiType.addItems(item)
        index=item.index(cr.type)
        self.uiType.setCurrentIndex(index)  
        
        
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def modifier(self):
        
        
        if (self.uiType.currentText()=="" or self.uiNomBanque.text()=="" or self.uiDelaiR.value()==0 or self.uiTaux.value()==0 or self.uiMontant.value()==0):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            credit=Credit(str(cr.idCredit),str(self.uiType.currentText()),str(self.uiNomBanque.text()),self.uiDelaiR.value(),self.uiTaux.value(),self.uiDelaiG.value(),f.idFinancement,self.uiMontant.value())
            #row=[credit.idCredit,credit.type,credit.nomBanque,credit.delaisRem,credit.tauxInteret,credit.delaisGrace,credit.idFinancement,credit.montant]
            del f.listCredits[ind]
            f.listCredits.insert(ind,credit)
            credit.modifier()
            credit.suppRem()
            credit.calculRemboursement() 
            self.close()
            
tableauReBase, tableauReForm = uic.loadUiType('tableauRemboursement.ui')
class tableauRemboursement(tableauReBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(tableauReBase,self).__init__(parent)
        self.setupUi(self)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        headers=["id_amortissement","id_investissement","annee","capitale restant", "interet","amortissement","interets cumules","annuite"]
        #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
        row = []
        for nod in cre.listsRemboursement :
            s =(nod.idRem,nod.idCredit,nod.annee,nod.capitalRestant,nod.interet,nod.amortissement,nod.interetsCumules,nod.annuite)
            row.append(s)
        
        model =PaletteTableModel(row,headers)     
        self.tableView.setModel(model)
        self.tableView.hideColumn(0)
        self.tableView.hideColumn(1)
                              
        
        
promotteurtBase, promotteurForm = uic.loadUiType('promotteur.ui')
class WidgetPromotteur(promotteurtBase,promotteurForm):
    indexes=-1
    def __init__(self, parent=None):
        super(promotteurtBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifier,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier,SIGNAL("clicked()"),self.modifierPromotteur)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimerPromotteur)
        self.remplissageTableView()
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        QObject.connect(self.tableView,SIGNAL("clicked(QModelIndex)"),self.clic)
        
        
        
    def clic(self,index):
        
        self.indexes= index.row()
        
        
        
        global ind
        ind=self.indexes
        
    
    
    def  remplissageTableView(self):
            
            
            headers=["Cin","Nom", "Prenom","Telephone","Adresse","Presentation","idEtude"]
            #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
            row = []
            for nod in etude.listPromotteurs :
                s =(nod.cin,nod.nom,nod.prenom,nod.telephone,nod.adresse,nod.presentation)
                row.append(s)
        
            model =PaletteTableModel(row,headers)     
            self.tableView.setModel(model)
            self.tableView.hideColumn(6)
            
    def modifierPromotteur(self):
        
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            #print self.indexes
            global pro
            pro=etude.listPromotteurs[self.indexes]
            modifier=ModifierPromotteur()
            modifier.exec_()
            self.remplissageTableView()
            
    def supprimerPromotteur(self):
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            
            pro=etude.listPromotteurs[self.indexes]
            reply=QMessageBox.information(self,"Suppression","voulez-vous vraiment supprimer le Promotteur : "+ str(pro.prenom)+" ?",QMessageBox.Yes,QMessageBox.No)
            if reply==QtGui.QMessageBox.Yes:
                row=PromotteurParEtude.verifierP(pro)
                
                if (row==True):
                    promotteurParEtude=PromotteurParEtude(etude.idEtude,str(pro.cin))
                    promotteurParEtude.supprimer()        
                else :
                    pro.supprimer()
                
                
                
                del etude.listPromotteurs[self.indexes]
                rs = "le promotteur est supprimé avec succée"
                QMessageBox.information(self,"Suppression",str(rs),QMessageBox.Ok)
                self.remplissageTableView()     
    
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def inserer(self):
        ajout=AjoutPromotteur()
        ajout.exec_()
        self.remplissageTableView()    
    
AjoutProVBase, AjoutProVForm = uic.loadUiType('ajoutPromotteur.ui')
class AjoutPromotteur(AjoutProVBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutProVBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)

        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        QObject.connect(self.uiRecherche,SIGNAL("clicked()"),self.verifier)
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        """
    def verifCIN(self,cin):
        for c in cin :
            if (c in["0","1",]):  
        """
    def verifier(self):
        if (self.uiCin.text()=="" or len(self.uiCin.text())!=8 ):
            self.uiErreur.setText("numero CIN invalide")
           
        else :
           
            promotteur=Promotteur(str(self.uiCin.text()),None,None,None,None,None)
            if (PromotteurParEtude.verifierPE(promotteur,etude)==True):
                self.uiErreur.setText("ce promotteur existe")
            elif (Promotteur.verifier(promotteur)==True):
                row=Promotteur.getPromotteur(promotteur.cin)
                self.uiCin.setText(str(row.cin))
                self.uiNom.setText(row.nom)
                self.uiPrenom.setText(row.prenom) 
                self.uiTelephone.setText(row.telephone)
                self.uiAdresse.setText(row.adresse)
                self.uiPresentation.setText(row.presentation)
                    
                     
            else :
                self.uiCin.setEnabled(True)
                self.uiNom.setEnabled(True)
                self.uiPrenom.setEnabled(True) 
                self.uiTelephone.setEnabled(True)
                self.uiAdresse.setEnabled(True)
                self.uiPresentation.setEnabled(True)
                    
                
    def inserer(self):
        if (self.uiCin.text()=="" or self.uiNom.text()=="" or self.uiPrenom.text()=="" or self.uiTelephone.text()=="" or self.uiAdresse.text()=="" ):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        elif (len(self.uiCin.text())!=8 ):
            self.uiErreur.setText("numero CIN invalide")    
        else :
           
            promotteur=Promotteur(str(self.uiCin.text()),str(self.uiNom.text()),str(self.uiPrenom.text()),str(self.uiTelephone.text()),str(self.uiAdresse.text()),str(self.uiPresentation.toPlainText ()))
            if (PromotteurParEtude.verifierPE(promotteur,etude)==True):
                self.uiErreur.setText("ce promotteur existe")
            elif (Promotteur.verifier(promotteur)==True):
                reply=QMessageBox.information(self,"Affectation",str(promotteur.prenom)+" existe dans une autre etude! voulez vous l'affecter a cette etude ?",QMessageBox.Yes,QMessageBox.No)
                if reply==QtGui.QMessageBox.Yes:
                    promotteurParEtude=PromotteurParEtude(etude.idEtude,str(promotteur.cin))
                    
                    etude.listPromotteurs.append(promotteur) 
                    promotteurParEtude.ajouter()
                    print etude.listPromotteurs[0]
                    self.close()
                    
                     
            else :    
                promotteur.ajouter()
                promotteurParEtude=PromotteurParEtude(etude.idEtude,str(promotteur.cin))
                
                etude.listPromotteurs.append(promotteur)
                promotteurParEtude.ajouter()
                QMessageBox.information(self,"Ajouter","le promotteur est affecter avec succée",QMessageBox.Ok)
                self.close()
                
                
                  
                
ModifierProVBase, ModifierProVForm = uic.loadUiType('modifierPromotteur.ui')
class ModifierPromotteur(ModifierProVBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(ModifierProVBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)

        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.inserer)
        self.uiCin.setText(pro.cin)
        self.uiNom.setText(pro.nom)
        self.uiPrenom.setText(pro.prenom)
        self.uiTelephone.setText(pro.telephone)
        self.uiAdresse.setText(pro.adresse)
        self.uiPresentation.setText(pro.presentation)
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
      
        
    def inserer(self):
        if (self.uiCin.text()=="" or self.uiNom.text()=="" or self.uiPrenom.text()=="" or self.uiTelephone.text()=="" or self.uiAdresse.text()=="" ):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        elif (len(self.uiCin.text())!=8):
            self.uiErreur.setText("numero CIN invalide")    
        else :
            print ind
            promotteur=Promotteur(str(self.uiCin.text()),str(self.uiNom.text()),str(self.uiPrenom.text()),str(self.uiTelephone.text()),str(self.uiAdresse.text()),str(self.uiPresentation.toPlainText ()))
            if (pro.cin != promotteur.cin):    
                if (Promotteur.verifier(promotteur)==True):
                    self.uiErreur.setText("ce promotteur  existe")
                else:
                    
                    del etude.listPromotteurs[ind]
                    etude.listPromotteurs.insert(ind,promotteur)
                    Promotteur.modifier(promotteur,pro.cin)
                    
                    self.close() 
            else:
                    del etude.listPromotteurs[ind]
                    etude.listPromotteurs.insert(ind,promotteur)
                    promotteur.modifier(promotteur,pro.cin)
                    self.close()
           
                            
        
articleBase, articleForm = uic.loadUiType('articles.ui')
class WidgetArticle(articleBase,articleForm):
    indexes=-1
    
    def __init__(self, parent=None):
        super(articleBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimerArticle)
        QObject.connect(self.uiModifier,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifier,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier,SIGNAL("clicked()"),self.modifierArticle)
        self.remplissageTableView()
        self.tableView.setColumnWidth(1,  123);
        self.tableView.setColumnWidth(2,  123);
        self.tableView.setColumnWidth(3,  123);
        self.tableView.setColumnWidth(4,  123);
        self.tableView.setColumnWidth(5,  123);
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        QObject.connect(self.tableView,SIGNAL("clicked(QModelIndex)"),self.clic)
        
        
        
    def clic(self,index):
        
        self.indexes= index.row()
        
        
        
        global ind
        ind=self.indexes
        
    
    
    def  remplissageTableView(self):
            
            
            headers=["id","designation", "type","fournisseur","prix d'achat","prix de vente","unite de mesure"]
            #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
            row = []
            for nod in version.listAritcles :
                s =(nod.idArticle,nod.designation,nod.type,nod.fournisseur,nod.prixAchat,nod.prixVente,nod.uniteMesure)
                row.append(s)
        
            model =PaletteTableModel(row,headers)     
            self.tableView.setModel(model)
            self.tableView.hideColumn(0)
        
        
    def inserer(self):
        ajout=AjoutArticle()
        ajout.exec_()   
        self.remplissageTableView() 
        
    def modifierArticle(self):
        #x=self.clic(self.tableView.selectionModel().index.row())
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            #print self.indexes
            global ar
            ar=version.listAritcles[self.indexes]
            modifier=ModifierArticle()
            modifier.exec_()
            self.remplissageTableView() 
            
    def supprimerArticle(self):
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            
            ar=version.listAritcles[self.indexes]
            reply=QMessageBox.information(self,"Suppression","voulez vous vraiment supprimer cet article : "+ str(ar.designation)+" ?",QMessageBox.Yes,QMessageBox.No)
            if reply==QtGui.QMessageBox.Yes:
                row=ArticleParVersion.verifierArticle(ar)
                
                if (row==True):
                    articleParVersion=ArticleParVersion(ar.idArticle,version.idVersion)
                    articleParVersion.supprimer()        
                else :
                    ar.supprimer()
                
                
                
                del version.listAritcles[self.indexes]
                #rs = "l'article est supprimé avec succée"
                #QMessageBox.information(self,"Suppression",str(rs),QMessageBox.Ok)
                self.remplissageTableView()            
    
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
        
        
AjoutArBase, AjoutArForm = uic.loadUiType('ajoutArticle.ui')
class AjoutArticle(AjoutArBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutArBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        self.uiPrixVente.setEnabled(False)
        item1=["","Fini","Consommable","Matiere premiere"]
        self.uiType.addItems(item1)
        QObject.connect(self.uiType,SIGNAL("currentIndexChanged (const QString&)"),self.activer)
        item2=["","M","M²","Cm","Cm²","g","Kg"]
        self.uiUnite.addItems(item2)
        
    def activer(self,ch):
        if ch=="Fini":
            self.uiPrixVente.setEnabled(True)
        else :
            self.uiPrixVente.setEnabled(False)    
                
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiType.currentText()=="" or self.uiDesignation.text()=="" or self.uiPrixAchat.value()==0 or self.uiFournisseur.text()=="" or self.uiUnite.currentText()=="" ):
            
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            if self.uiType.currentText()=="Fini" and self.uiPrixVente.value()==0:
                self.uiErreur.setText("veuillez bien remplir le formulaire")
            else :    
            
            
                article=Article(None,str(self.uiDesignation.text()),str(self.uiType.currentText()),str(self.uiFournisseur.text()),self.uiPrixAchat.value(),self.uiPrixVente.value(),str(self.uiUnite.currentText()))
                   
                if (Article.verifier(article,version.idVersion)==True):
                    self.uiErreur.setText("la designation existe")
                else:
    
                    article.ajouter()
                    article.getIdArticle()
                    version.listAritcles.append(article)
                    articleParVersion=ArticleParVersion(article.idArticle,version.idVersion)
                    articleParVersion.ajouter()
                    
                    self.close()                         
                  
                  
ModifierArBase, ModifierArForm = uic.loadUiType('modifierArticle.ui')
class ModifierArticle(ModifierArBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(ModifierArBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        self.uiDesignation.setText(ar.designation)
        self.uiFournisseur.setText(ar.fournisseur)
        print "-----"
        print ar.prixAchat
        print ar.prixVente
        print "-----"
        self.uiPrixAchat.setValue(ar.prixAchat)
        self.uiPrixVente.setValue(ar.prixVente)
        item1=["","Fini","Consommable","Matière première"]
        self.uiType.addItems(item1)
        QObject.connect(self.uiType,SIGNAL("currentIndexChanged (const QString&)"),self.activer)
        index=item1.index(ar.type)
        self.uiType.setCurrentIndex(index)
        item2=["","M","M²","Cm","Cm²","g","Kg"]
        self.uiUnite.addItems(item2)
        index=item2.index(ar.uniteMesure)
        self.uiUnite.setCurrentIndex(index)
        
    def activer(self,ch):
        if ch=="Fini":
            self.uiPrixVente.setEnabled(True)
        else :
            self.uiPrixVente.setEnabled(False)    
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        
        
        if (self.uiType.currentText()=="" or self.uiDesignation.text()=="" or self.uiPrixAchat.value()==0 or self.uiFournisseur.text()=="" or self.uiUnite.currentText()=="" ):
            if self.uiType.currentText()=="Fini" and self.uiPrixVente.value()==0:
                self.uiErreur.setText("veuillez bien remplir le formulaire")
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            if self.uiType.currentText()=="Fini" and self.uiPrixVente.value()==0:
                self.uiErreur.setText("veuillez bien remplir le formulaire")
            else :
            
            
                article=Article(ar.idArticle,str(self.uiDesignation.text()),str(self.uiType.currentText()),str(self.uiFournisseur.text()),self.uiPrixAchat.value(),self.uiPrixVente.value(),str(self.uiUnite.currentText()))
                if (ar.designation != article.designation):    
                    if (Article.verifier(article,version.idVersion)==True):
                        self.uiErreur.setText("la designation existe")
                    else:
                        #rowAncien=[inv.idInvestissement,inv.designation,inv.type,inv.fournisseur,inv.prix,inv.idEtude,inv.pays,inv.quantite,inv.prixTotal,inv.typeAmortissement,inv.dureVie,inv.tauxAmortissement]
                        
         
                        del version.listAritcles[ind]
                        version.listAritcles.insert(ind,article)
                        article.modifier()
                        self.close() 
                else:
                        del version.listAritcles[ind]
                        version.listAritcles.insert(ind,article)
                        article.modifier()
                        self.close()
                   
        
        

                  

produitBase, produitForm = uic.loadUiType('produits.ui')
class WidgetProduit(produitBase,produitForm):
    indexes=-1
    def __init__(self, parent=None):
        super(produitBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimerProduit)
        QObject.connect(self.uiModifier,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifier,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier,SIGNAL("clicked()"),self.modifierProduit)
        self.remplissageTableView()
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        QObject.connect(self.tableView,SIGNAL("clicked(QModelIndex)"),self.clic)
        
        
        
    def clic(self,index):
        
        self.indexes= index.row()
        global ind
        ind=self.indexes
        global produit
        produit=version.listProduits[self.indexes]
        headers=["Designation","Quantite"]
        row = []
        for nod in produit.listNomenclature :
            s =(nod.designation)
            row.append(s)
        model =PaletteTableModel(row,headers)     
        self.tableViewN.setModel(model)
        self.tableViewN.setColumnWidth(0,  140)
        self.tableViewN.setColumnWidth(1,  141)
        
        
        
    
    
    def  remplissageTableView(self):
            headers=["Designation","Prix de vente"]
            #tableData0=[[str(row[i]) for i in range(len(row))] for row in financement.listCredit]
            row = []
            for nod in version.listProduits :
                s =(nod.designation,nod.prixVente)
                row.append(s)
            model =PaletteTableModel(row,headers)     
            self.tableView.setModel(model)
            self.tableView.setColumnWidth(0,  105)
            self.tableView.setColumnWidth(1,  105)
        
        
    def inserer(self):
        ajout=AjoutArticleProduit()
        ajout.exec_()
        self.remplissageTableView() 
    def modifierProduit(self):
        
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            #print self.indexes
            #self.tableViewN.clearSpans()
            modifier=ModifierArticleProduit()
            modifier.exec_()
            self.remplissageTableView()
            
    def supprimerProduit(self):
        if (self.indexes>-1 and len(self.tableView.selectedIndexes())!=0):
            
            
            reply=QMessageBox.information(self,"Suppression","voulez-vous vraiment supprimer le Produit : "+ str(produit.designation)+" ?",QMessageBox.Yes,QMessageBox.No)
            if reply==QtGui.QMessageBox.Yes:
                produit.supprimer()
                del version.listProduits[self.indexes]
                #rs = "le promotteur est supprimé avec succée"
                #QMessageBox.information(self,"Suppression",str(rs),QMessageBox.Ok)
                self.remplissageTableView()            
           
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)   
        
AjoutArPBase, AjoutArPForm = uic.loadUiType('ajoutArticleProduit.ui')
class AjoutArticleProduit(AjoutArPBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutArPBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.iconPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.iconReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.iconPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.iconReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimer)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.insererLigne)
        self.tableWidget.setColumnCount(3) #rows and columns of table
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0,  15)
        self.tableWidget.setColumnWidth(1,  190)
        self.tableWidget.setColumnWidth(2,  170)
        item = QtGui.QTableWidgetItem()
        item.setText("Article")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setText("Quantite")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
         
    
        
    def supprimer(self):
        indexes=[]
        for i in range(self.tableWidget.rowCount()):
            checkBox=self.tableWidget.cellWidget(i,0);
            if checkBox.isChecked() :
                indexes.append(i)  
        print len(indexes)    
        for j in range(len(indexes)):
            self.tableWidget.removeRow(indexes[j-1])
            
        
                
        
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiDesignation.text()=="" or self.tableWidget.rowCount()==0 or self.uiPrixVente.value()==0):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            
            
            article=Article(None,str(self.uiDesignation.text()),"produit",None,None,self.uiPrixVente.value(),None)
               
            if (Article.verifier(article,version.idVersion)==True):
                self.uiErreur.setText("la designation existe")
            else: 
                v=True
                for i in range(self.tableWidget.rowCount()):
                    designation =self.tableWidget.cellWidget(i,1);
                    quantite = self.tableWidget.cellWidget(i,2);
                    if quantite.value()==0 :
                        v=False
                    
                if v==False:
                    self.uiErreur.setText("la quantite doit etre differents de 0")
                else:
                    v1=True
                    i=0
                    while ((i<self.tableWidget.rowCount()/2) and( v1==True)) : 
                        designation =self.tableWidget.cellWidget(i,1);
                        j=i+1
                        
                        while ((j<self.tableWidget.rowCount()) and (v1==True)) : 
                            
                            designation2=self.tableWidget.cellWidget(j,1);
                            if designation.itemText(designation.currentIndex())==designation2.itemText(designation2.currentIndex()):
                                
                                v1=False
                            j=j+1   
                        i=i+1
                    if (v1==False):
                        self.uiErreur.setText("une nomenclature exite plusieurs fois")  
                    else :
                        article.ajouter()
                        article.getIdArticle()
                        version.listProduits.append(article)
                        articleParVersion=ArticleParVersion(article.idArticle,version.idVersion)
                        articleParVersion.ajouter()
                        
                        
                        for i in range(self.tableWidget.rowCount()):
                            designation =self.tableWidget.cellWidget(i,1);
                            a=Article(None,str(designation.itemText(designation.currentIndex())),None,None,None,None,None)
                            a.getIdArticle()
                            
                            quantite = self.tableWidget.cellWidget(i,2);
                            print article.idArticle
                            print a.idArticle
                            print quantite.value()
                            nomenclature=Nomenclature(article.idArticle,a.idArticle,quantite.value())
                            nomenclature.ajouter()
                            row=[designation.itemText(designation.currentIndex()),quantite.value]
                            
                            
                            
                            
                            
                            
                            self.close()
                                

        
          
        
    def iconPressed(self):
        s=QtCore.QSize(10,10)
        self.sender().setIconSize(s)
        
    def iconReleased(self):
        s=QtCore.QSize(16,16)
        self.sender().setIconSize(s)    
        
    def insererLigne(self):
        i=self.tableWidget.rowCount()
        i=i+1
        self.tableWidget.setRowCount(i)
        checkBox=QtGui.QCheckBox()
        designation = QtGui.QComboBox()
        quantite= QtGui.QDoubleSpinBox()
        quantite.setMaximum(1000000)
        nod=[]
        for row in Article.getListNomenclatures(version.idVersion):
            nod.append(row.designation)
        for row in nod:    
            designation.addItems(row)
            
            
        self.tableWidget.setCellWidget(i-1,0,checkBox)
        self.tableWidget.setCellWidget(i-1,1, designation)
        self.tableWidget.setCellWidget(i-1,2, quantite)
        QObject.connect(quantite,SIGNAL("valueChanged(double)"),self.calculTotal)
        QObject.connect(designation,SIGNAL("currentIndexChanged (const QString&)"),self.calculTotal)
    def calculTotal(self,double):
        t=0.0
        for i in range(self.tableWidget.rowCount()):
            designation=self.tableWidget.cellWidget(i,1);
            prix=Article.getPrix(designation.itemText(designation.currentIndex()))
            
            quantite = self.tableWidget.cellWidget(i,2);
            t=t+(prix[0][0]*quantite.value())
            
        self.uiPrixTotal.setText(str(t))        


ModifierArPBase, ModifierArPForm = uic.loadUiType('modifierArticleProduit.ui')
class ModifierArticleProduit(ModifierArPBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(ModifierArPBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.iconPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.iconReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.iconPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.iconReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimer)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.insererLigne)
        self.uiDesignation.setText(produit.designation)
        self.uiPrixVente.setValue(produit.prixVente)
        self.tableWidget.setColumnCount(3) #rows and columns of table
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0,  15)
        self.tableWidget.setColumnWidth(1,  190)
        self.tableWidget.setColumnWidth(2,  170);
        item = QtGui.QTableWidgetItem()
        item.setText("Article")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setText("Quantite")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
          
        
        
        for row in produit.listNomenclature:
            
            i=self.tableWidget.rowCount()
            i=i+1
            self.tableWidget.setRowCount(i)
            checkBox=QtGui.QCheckBox()
            designation = QtGui.QComboBox()
            quantite= QtGui.QDoubleSpinBox()
            quantite.setMaximum(1000000)
            
            quantite.setValue(row.quantite)
            j=-1
            nod=[]
            for r in Article.getListNomenclatures(version.idVersion):
                j=j+1
                nod.append(row)
                if r[0]==row[0]:
                    index=j
            for r in nod :
                designation.addItems(r)
            
            designation.setCurrentIndex(index) 
            self.tableWidget.setCellWidget(i-1,0, checkBox)   
            self.tableWidget.setCellWidget(i-1,1, designation)
            self.tableWidget.setCellWidget(i-1,2, quantite)
            QObject.connect(quantite,SIGNAL("valueChanged(double)"),self.calculTotal)
            QObject.connect(designation,SIGNAL("currentIndexChanged (const QString&)"),self.calculTotal)
            self.calculTotal(None)
             
    
        
    def supprimer(self):
        indexes=[]
        for i in range(self.tableWidget.rowCount()):
            checkBox=self.tableWidget.cellWidget(i,0);
            if checkBox.isChecked() :
                indexes.append(i)  
        print len(indexes)    
        for j in range(len(indexes)):
            self.tableWidget.removeRow(indexes[j-1])
                
        
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiDesignation.text()=="" or self.tableWidget.rowCount()==0):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            
            
            article=Article(produit.idArticle,str(self.uiDesignation.text()),"produit",None,None,None)
            if article.designation != produit.designation :
                   
                if (Article.verifier(article,version.idVersion)==True):
                    self.uiErreur.setText("la designation existe")
                else:
                    
                    
                    v=True
                    for i in range(self.tableWidget.rowCount()):
                        designation =self.tableWidget.cellWidget(i,1);
                        quantite = self.tableWidget.cellWidget(i,2);
                        if quantite.value()==0 :
                            v=False
                        
                    if v==False:
                        self.uiErreur.setText("la quantite doit etre differents de 0")
                    else:
                        v1=True
                        i=0
                        while ((i<self.tableWidget.rowCount()/2) and( v1==True)) : 
                            designation =self.tableWidget.cellWidget(i,1);
                            j=i+1
                            
                            while ((j<self.tableWidget.rowCount()) and (v1==True)) : 
                                
                                designation2=self.tableWidget.cellWidget(j,1);
                                if designation.itemText(designation.currentIndex())==designation2.itemText(designation2.currentIndex()):
                                    
                                    v1=False
                                j=j+1   
                            i=i+1
                        if (v1==False):
                            self.uiErreur.setText("une nomenclature exite plusieurs fois")  
                        else :
                        
                            article.modifier()
                            
                            
                            del version.listProduits [ind]
                            version.listProduits.insert(ind,article)
                            del article.listNomenclature[:]
                            article.supprimeListNomenclatureParArticle()
                            
                            
                            for i in range(self.tableWidget.rowCount()):
                                designation =self.tableWidget.cellWidget(i,1);
                                a=Article(None,str(designation.itemText(designation.currentIndex())),None,None,None,None)
                                a.getIdArticle()
                                
                                quantite = self.tableWidget.cellWidget(i,2);
                                print article.idArticle
                                print a.idArticle
                                print quantite.value()
                                nomenclature=Nomenclature(article.idArticle,a.idArticle,quantite.value())
                                nomenclature.ajouter()
                                
                                self.close()
                                
            else :
                del article.listNomenclature[:]
                article.supprimeListNomenclatureParArticle()
                for i in range(self.tableWidget.rowCount()):
                    designation =self.tableWidget.cellWidget(i,1);
                    a=Article(None,str(designation.itemText(designation.currentIndex())),None,None,None,None)
                    a.getIdArticle()
                    
                    quantite = self.tableWidget.cellWidget(i,2);
                    print article.idArticle
                    print a.idArticle
                    print quantite.value()
                    nomenclature=Nomenclature(article.idArticle,a.idArticle,quantite.value())
                    nomenclature.ajouter()
                    
                    self.close()

        
          
        
    def iconPressed(self):
        s=QtCore.QSize(10,10)
        self.sender().setIconSize(s)
        
    def iconReleased(self):
        s=QtCore.QSize(16,16)
        self.sender().setIconSize(s)    
        
    def insererLigne(self):
        i=self.tableWidget.rowCount()
        i=i+1
        self.tableWidget.setRowCount(i)
        checkBox=QtGui.QCheckBox()
        designation = QtGui.QComboBox()
        quantite= QtGui.QDoubleSpinBox()
        quantite.setMaximum(1000000)
        
        nod=[]
        for row in Article.getListNomenclatures(version.idVersion):
            nod.append(row.designation)
        for row in nod:    
            designation.addItems(row)
        self.tableWidget.setCellWidget(i-1,0, checkBox)    
        self.tableWidget.setCellWidget(i-1,1, designation)
        self.tableWidget.setCellWidget(i-1,2, quantite)
        QObject.connect(quantite,SIGNAL("valueChanged(double)"),self.calculTotal)
        QObject.connect(designation,SIGNAL("currentIndexChanged (const QString&)"),self.calculTotal)

    def calculTotal(self,double):
        t=0.0
        for i in range(self.tableWidget.rowCount()):
            designation=self.tableWidget.cellWidget(i,1);
            prix=Article.getPrix(designation.itemText(designation.currentIndex()))
            
            quantite = self.tableWidget.cellWidget(i,2);
            t=t+(prix[0][0]*quantite.value())
            
        self.uiPrixTotal.setText(str(t))    


            
        
    

chargeBase, chargeForm = uic.loadUiType('charges.ui')
class WidgetCharge(chargeBase,chargeForm):
    indexes1=-1
    indexes2=-1
    def __init__(self, parent=None):
        super(chargeBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiSupprimer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiSupprimer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiSupprimer,SIGNAL("clicked()"),self.supprimerCharge)
        QObject.connect(self.uiModifier,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiModifier,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiModifier,SIGNAL("clicked()"),self.modifierCharge)
        self.remplissageTableViewPer()
        self.remplissageTableViewFrais()
        
        self.tableViewPer.setColumnWidth(1,  168);
        self.tableViewPer.setColumnWidth(2,  168);
        self.tableViewFrais.setColumnWidth(1,  143)
        self.tableViewFrais.setColumnWidth(2,  143);
        self.tableViewPer.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewFrais.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        QObject.connect(self.tableViewPer,SIGNAL("clicked(QModelIndex)"),self.clic)
        QObject.connect(self.tableViewFrais,SIGNAL("clicked(QModelIndex)"),self.clic)    
    def clic(self,index):
        
        if self.sender().objectName()=="tableViewPer":
            self.indexes1= index.row()
            global ind1
            ind1=self.indexes1
            self.indexes2=-1
            print "indexes1=" + str(self.indexes1)
            print "indexes2=" + str(self.indexes2)
            global personel
            personel=version.listChargePersonnel[self.indexes1] 
        else :
            self.indexes2= index.row()
            global ind2
            ind2=self.indexes2
            
            self.indexes1=-1
            print "indexes2=" + str(self.indexes2)
            print "indexes1=" + str(self.indexes1)
            global fraisG
            fraisG=version.listFraisGeneraux[self.indexes2]    
    
    
    def  remplissageTableViewPer(self):
            
            
        headers=["id","Poste", "Salaire","id_version"]
        row = []
        for nod in version.listChargePersonnel :
            s =(nod.idCharge,nod.designation,nod.salaire,nod.idVersion)
            row.append(s)
        model =PaletteTableModel(row,headers)     
        self.tableViewPer.setModel(model)
        self.tableViewPer.hideColumn(0)
        self.tableViewPer.hideColumn(3)
        
    def  remplissageTableViewFrais(self):
            
            
        headers=["id","Designation", "Montant","id_version"]
        row = []
        for nod in version.listFraisGeneraux :
            s =(nod.idCharge,nod.designation,nod.montant,nod.idVersion)
            row.append(s)
        model =PaletteTableModel(row,headers)     
        self.tableViewFrais.setModel(model)
        self.tableViewFrais.hideColumn(0)
        self.tableViewFrais.hideColumn(3)    
        
    def inserer(self):
        global ajout
        ajout=AjoutCharge()
        ajout.exec_() 
        self.remplissageTableViewPer()
        self.remplissageTableViewFrais()   
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)        
        
    def modifierCharge(self):
        
        if (self.indexes1>-1 and len(self.tableViewPer.selectedIndexes())!=0):
            #print self.indexes
            
            modifier=ModifierChargePersonnel()
            modifier.exec_()
            self.remplissageTableViewPer()
        elif (self.indexes2>-1 and len(self.tableViewFrais.selectedIndexes())!=0):    
            #print self.indexes
            
            modifier=ModifierFrais()
            modifier.exec_()
            self.remplissageTableViewFrais()
    def supprimerCharge(self):
        if (self.indexes1>-1 and len(self.tableViewPer.selectedIndexes())!=0):
            reply=QMessageBox.information(self,"Suppression","voulez-vous vraiment supprimer cette charge : "+ str(personel.designation)+" ?",QMessageBox.Yes,QMessageBox.No)
            if reply==QtGui.QMessageBox.Yes:
                
                charge=Charge(personel.idCharge,personel.designation,personel.idVersion)
                charge.supprimer()
                del version.listChargePersonnel[self.indexes1]
                rs = "la charge est supprimé avec succée"
                QMessageBox.information(self,"Suppression",str(rs),QMessageBox.Ok)
                self.remplissageTableViewPer()   
        if (self.indexes2>-1 and len(self.tableViewFrais.selectedIndexes())!=0):
            reply=QMessageBox.information(self,"Suppression","voulez-vous vraiment supprimer ce frais : "+ str(fraisG.designation)+" ?",QMessageBox.Yes,QMessageBox.No)
            if reply==QtGui.QMessageBox.Yes:
                
                charge=Charge(fraisG.idCharge,fraisG.designation,fraisG.idVersion)
                charge.supprimer()
                del version.listFraisGeneraux[self.indexes2]
                rs = "le frais est supprimé avec succée"
                QMessageBox.information(self,"Suppression",str(rs),QMessageBox.Ok)
                self.remplissageTableViewFrais()    
   
AjoutChargePBase, AjoutChargePForm = uic.loadUiType('chargepersonnel.ui')
class AjoutChargePersonnel(AjoutChargePBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutChargePBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),ajout.close)
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiPoste.text()=="" or self.uiSalaire.value()==0 ):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            charge=Charge(None,str(self.uiPoste.text()),version.idVersion)
            #chargePersonnel=ChargePersonnel(str(self.uiPoste.text()),self.uiSalaire.value(),self.uiNombre.value(),version.idVersion)
                
            if (Charge.verifier(charge)==True):
                self.uiErreur.setText("la designation existe")
            else:
                
                charge.ajouter()
                id=Charge.getId(charge)
                chargePersonnel=ChargePersonnel(id,str(self.uiPoste.text()),self.uiSalaire.value(),version.idVersion)
                chargePersonnel.ajouter()
                
                
                version.listChargePersonnel.append(chargePersonnel)
                ajout.close()
        



        
AjoutFraisBase, AjoutFraisForm = uic.loadUiType('fraisGeneraux.ui')
class AjoutFrais(AjoutFraisBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutFraisBase,self).__init__(parent)
        self.setupUi(self) 
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),ajout.close)
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiDesignation.text()=="" or self.uiMontant.value()==0 ):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            
            charge=Charge(None,str(self.uiDesignation.text()),version.idVersion)
           
                
            if (Charge.verifier(charge)==True):
                self.uiErreur.setText("la designation existe")
            else:
                charge.ajouter()
                id=Charge.getId(charge)
                frais=FraisGeneraux(id,str(self.uiDesignation.text()),self.uiMontant.value(),version.idVersion)
                frais.ajouter()
                version.listFraisGeneraux.append(frais)
                ajout.close()             
               
        
AjoutChargeBase, AjoutChargeForm = uic.loadUiType('ajoutCharge.ui')
class AjoutCharge(AjoutChargeBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(AjoutChargeBase,self).__init__(parent)
        self.setupUi(self)
        
        QObject.connect(self.comboBox,SIGNAL("currentIndexChanged(int)"),self.afficher)
        
   
        
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())    
        
    
    def afficher(self):
        if( self.comboBox.itemText(self.comboBox.currentIndex())=="Charge Personnel"):
            self_ajout=AjoutChargePersonnel(self)
            self.clearLayout(self.verticalLayout_2)
            self.verticalLayout_2.addWidget(self_ajout)
        elif ( self.comboBox.itemText(self.comboBox.currentIndex())=="Frais General"):     
            self_ajout=AjoutFrais(self)
            self.clearLayout(self.verticalLayout_2)
            self.verticalLayout_2.addWidget(self_ajout)
        else:
            self.clearLayout(self.verticalLayout_2)
            print self.comboBox.itemText(self.comboBox.currentIndex())        

ModifierChargePBase, ModifierChargePForm = uic.loadUiType('chargepersonnel.ui')
class ModifierChargePersonnel(ModifierChargePBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(ModifierChargePBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        self.uiPoste.setText(personel.designation)
        self.uiSalaire.setValue(personel.salaire)
        self.uiNombre.setValue(personel.nombre)
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiPoste.text()=="" or self.uiSalaire.value()==0 or self.uiNombre.value()==0):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            charge=Charge(personel.idCharge,str(self.uiPoste.text()),version.idVersion)
            #chargePersonnel=ChargePersonnel(personel.idCharge,str(self.uiPoste.text()),self.uiSalaire.value(),self.uiNombre.value(),version.idVersion)
            if (charge.designation != personel.designation):
                    
                if (Charge.verifier(charge)==True):
                    self.uiErreur.setText("la designation existe")
                else:
                    charge.modifier(personel.designation)
                    chargePersonnel=ChargePersonnel(personel.idCharge,str(self.uiPoste.text()),self.uiSalaire.value(),self.uiNombre.value(),version.idVersion)
                    chargePersonnel.modifier()
                    
                    
                    del version.listChargePersonnel[ind1]
                    version.listChargePersonnel.insert(ind1,chargePersonnel)
                    
                    self.close()
            else :
                chargePersonnel=ChargePersonnel(personel.idCharge,str(self.uiPoste.text()),self.uiSalaire.value(),self.uiNombre.value(),version.idVersion)
                chargePersonnel.modifier()
                    
                
                del version.listChargePersonnel[ind1]
                version.listChargePersonnel.insert(ind1,chargePersonnel)
                print ind1
                
                
                self.close()
                        

        
ModifierFraisBase, ModifierFraisForm = uic.loadUiType('fraisGeneraux.ui')
class ModifierFrais(ModifierFraisBase,QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(ModifierFraisBase,self).__init__(parent)
        self.setupUi(self) 
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiAnnuler,SIGNAL("clicked()"),self.close)
        self.uiDesignation.setText(fraisG.designation)
        self.uiMontant.setValue(fraisG.montant)
        
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
        
    def inserer(self):
        if (self.uiDesignation.text()=="" or self.uiMontant.value()==0 ):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
        else :
            
            charge=Charge(fraisG.idCharge,str(self.uiDesignation.text()),version.idVersion)
            #frais=FraisGeneraux(str(self.uiDesignation.text()),self.uiMontant.value(),version.idVersion)
            if charge.designation != fraisG.designation :
                    
                if (Charge.verifier(charge)==True):
                    self.uiErreur.setText("la designation existe")
                else:
                    
                    charge.modifier(fraisG.designation)
                    frais=FraisGeneraux(fraisG.idCharge,str(self.uiDesignation.text()),self.uiMontant.value(),version.idVersion)
                    frais.modifier()
                    del version.listFraisGeneraux[ind2]
                    version.listFraisGeneraux.insert(ind2,frais)
                    self.close()        
            else :
                    frais=FraisGeneraux(fraisG.idCharge,str(self.uiDesignation.text()),self.uiMontant.value(),version.idVersion)
                    frais.modifier()
                    del version.listFraisGeneraux[ind2]
                    version.listFraisGeneraux.insert(ind2,frais)
                    self.close()
            
PresentationBase, PresentationForm = uic.loadUiType('presentation.ui')

class WidgetPresentation(PresentationBase,PresentationForm):
    """
    - Si UiMaFenetre, importe depuis le designer a ete construit comme QMainWindow, 
        alors MaFenetre doit heriter de QMainWindow
    - si UiMafFenetre est construit dans designer comme un QWidget, alors MaFenetre doit     
        heriter de QWidget"""
    def __init__(self, parent=None):
        super(PresentationBase,self).__init__(parent)
        self.setupUi(self)
        avantC=avantCommencer()
        self.verticalLayout.addWidget(avantC)
        self.uiAvantCommencer.setEnabled(False)
        QObject.connect(self.uiAvantCommencer,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAvantCommencer,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiPourquoi,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiPourquoi,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAvantCommencer,SIGNAL("clicked()"),self.inserer1)
        QObject.connect(self.uiPourquoi,SIGNAL("clicked()"),self.inserer2)
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font) 
    
        
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())    
        
    def inserer1(self):
        
        avantC=avantCommencer()
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(avantC)
        self.uiAvantCommencer.setEnabled(False)
        self.uiPourquoi.setEnabled(True) 
        
    def inserer2(self):
        
        pourquoiP=pourquoi()
        self.clearLayout(self.verticalLayout)
        self.verticalLayout.addWidget(pourquoiP)
        self.uiPourquoi.setEnabled(False)
        self.uiAvantCommencer.setEnabled(True)               

modifierEtudeBase, modifierEtudeForm = uic.loadUiType('modifierEtude.ui')
class WidgetModifierEtude(modifierEtudeBase,QtGui.QDialog):
    
    """
    - Si UiMaFenetre, importe depuis le designer a ete construit comme QMainWindow, 
        alors MaFenetre doit heriter de QMainWindow
    - si UiMafFenetre est construit dans designer comme un QWidget, alors MaFenetre doit     
        heriter de QWidget"""
    def __init__(self, parent=None):
        
        super(modifierEtudeBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        self.uiTitre.setText(etude.titre)
        #self.uiType.setEditText(etude.type)
        self.uiDescription.setText(etude.description)
        self.uiDuree.setValue(int(etude.dureeEtude))
        self.uiMarche.setText(etude.marche)
        self.uiSecteur.setText(etude.secteur)
        self.uiSociete.setText(etude.societe)
        self.uiProduits.setText(etude.produits)
        self.uiNature.setText(etude.nature)
        
        
    def inserer(self):
        ch=etude.titre
        etude2=Etude(None,str(self.uiTitre.text()),str(self.uiDescription.toPlainText()),str(self.uiType.currentText()),self.uiDuree.value(),str(self.uiNature.text()),str(self.uiSecteur.text()),str(self.uiProduits.toPlainText()),str(self.uiMarche.text()),str(self.uiSociete.text()))
        
         
        if (etude2.titre=="" or etude2.type=="" or etude2.description=="" or etude2.dureeEtude==0 or etude2.nature=="" or etude2.secteur=="" or etude2.produits=="" or etude2.marche=="" or etude2.societe==""):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
            #QMessageBox.warning(self,"erreur","veuillez bien remplir le formulaire",QMessageBox.Ok)
             
        elif (ch!=etude2.titre):
            
            if(Etude().verifier(etude2)):
                
                etude.titre=etude2.titre
                etude.description=etude2.description
                etude.type=etude2.type
                etude.nature=etude2.nature
                etude.secteur=etude2.secteur
                etude.marche=etude2.marche
                etude.societe=etude2.societe
                etude.dureeEtude=etude2.dureeEtude
                etude.produits=etude2.produits  
                etude.modifier() 
                self.close()
                 
                
            else :
                #QMessageBox.warning(self,"erreur","le nom de projet existe",QMessageBox.Ok)
                self.uiErreur.setText("le nom de projet existe")
        else :
            etude.titre=etude2.titre
            etude.description=etude2.description
            etude.type=etude2.type
            etude.nature=etude2.nature
            etude.secteur=etude2.secteur
            etude.marche=etude2.marche
            etude.societe=etude2.societe
            etude.dureeEtude=etude2.dureeEtude
            etude.produits=etude2.produits
            etude.modifier() 
            self.close()
           
                   
    
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        

ajoutEtudeBase, ajoutEtudeForm = uic.loadUiType('ajoutEtude.ui')
class WidgetAjout(ajoutEtudeBase,ajoutEtudeForm):
    """
    - Si UiMaFenetre, importe depuis le designer a ete construit comme QMainWindow, 
        alors MaFenetre doit heriter de QMainWindow
    - si UiMafFenetre est construit dans designer comme un QWidget, alors MaFenetre doit     
        heriter de QWidget"""
    def __init__(self, parent=None):
        
        super(ajoutEtudeBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.inserer)
        
    def inserer(self):
        
        etude=Etude(None,str(self.uiTitre.text()),str(self.uiDescription.toPlainText()),str(self.uiType.currentText()),self.uiDuree.value(),str(self.uiNature.text()),str(self.uiSecteur.text()),str(self.uiProduits.toPlainText()),str(self.uiMarche.text()),str(self.uiSociete.text()))
        global Nom
        Nom=QtCore.QString(self.uiTitre.text())
        print type(Nom) 
        if (etude.titre=="" or etude.type=="" or etude.description=="" or etude.dureeEtude==0 or etude.nature=="" or etude.secteur=="" or etude.produits=="" or etude.marche=="" or etude.societe==""):
            self.uiErreur.setText("veuillez bien remplir le formulaire")
            #QMessageBox.warning(self,"erreur","veuillez bien remplir le formulaire",QMessageBox.Ok)
        elif (Etude().verifier(etude)):
            
            etude.ajouter()
            etude.getIdEtude()
            version=Version(None,1,str(datetime.datetime.now().date()),False,0,0,etude.idEtude)
            version.ajouter()
            global NomVersion
            NomVersion="1"
            
            
            interface=interfaceEtude()
            window.setCentralWidget(interface)
        else :
            #QMessageBox.warning(self,"erreur","le nom de projet existe",QMessageBox.Ok)
            self.uiErreur.setText("le nom de projet existe")
    
    
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)    
      

ouvrirEtudeBase, ouvriEtudeForm = uic.loadUiType('ouvrirEtude.ui')
class ouvrirEtude(ouvrirEtudeBase,QtGui.QDialog):
    """
    - Si UiMaFenetre, importe depuis le designer a ete construit comme QMainWindow, 
        alors MaFenetre doit heriter de QMainWindow
    - si UiMafFenetre est construit dans designer comme un QWidget, alors MaFenetre doit     
        heriter de QWidget"""
       
    def __init__(self, parent=None):
        
        super(ouvrirEtudeBase,self).__init__(parent)
        self.setupUi(self)
        QObject.connect(self.uiValider,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiValider,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAnnuler,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAnnuler,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiValider,SIGNAL("clicked()"),self.ouvrir)
       
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        
        cursor.execute('SELECT titre From "Etude"')
        rows = cursor.fetchall()
        ListeE=[]
        for row in rows:
            
            ListeE.append(row[0])
        cnx.fermerConnexion()
       
        
        model=PaletteListModel(ListeE)
        self.listView.setModel(model)
        QObject.connect(self.listView,SIGNAL("clicked(QModelIndex)"),self.clic)
        QObject.connect(self.listView,SIGNAL("doubleClicked(QModelIndex)"),self.ouvrirDoubleClick)
    
    def ouvrirDoubleClick(self,index):
        global Nom
        Nom= index.model().data(index,QtCore.Qt.DisplayRole)
        self.close()    
        interface=interfaceEtude()
        window.setCentralWidget(interface)
            
    def clic(self,index):
        global Nom
        Nom= index.model().data(index,QtCore.Qt.DisplayRole)
        
           
    def ouvrir(self):
        
        self.close()    
        interface=interfaceEtude()
        window.setCentralWidget(interface)
    
    
        
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)


global Presentation
widgetBase, widgetForm = uic.loadUiType('acceuil.ui')
class MaWidget(widgetBase,widgetForm):
    """
    - Si UiMaFenetre, importe depuis le designer a ete construit comme QMainWindow, 
        alors MaFenetre doit heriter de QMainWindow
    - si UiMafFenetre est construit dans designer comme un QWidget, alors MaFenetre doit     
        heriter de QWidget"""
    def __init__(self, parent=None):
        super(widgetBase,self).__init__(parent)
        self.setupUi(self)
        
        data=["hhh","mmm","lll"]
        
        model =PaletteListModel(data)
        #self.listView.setModel(model)
        QObject.connect(self.uiAjouter,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiAjouter,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiAjouter,SIGNAL("clicked()"),self.inserer)
        QObject.connect(self.uiActualiser,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiActualiser,SIGNAL("released()"),self.buttonReleased)
        QObject.connect(self.uiParametres,SIGNAL("pressed()"),self.buttonPressed)
        QObject.connect(self.uiParametres,SIGNAL("released()"),self.buttonReleased)
        rootNode=Node("Etude0")
        rows=Etude.getListEtude()
        ListeE=[]
        for row in rows:   
            ListeE.append(row.titre)  
        model=PaletteListModel(ListeE)
        self.listEtude.setModel(model)    
            
        
        
        QObject.connect(self.listEtude,SIGNAL("clicked(QModelIndex)"),self.on_ListEtude_clicked)
        Presentation=WidgetPresentation()
        self.verticalLayout_2.addWidget(Presentation)
        self.LabelEtude.hide()
       
    
    def on_ListEtude_clicked(self,index):
        global Nom
        Nom= index.model().data(index,QtCore.Qt.DisplayRole)
        etude=Etude.getEtude(Nom)
        ListeV=[]
        
        for row in etude.listVersions:
            
            ListeV.append(row.numero)
        model=PaletteListModel(ListeV)
        self.listVersions.setModel(model) 
        QObject.connect(self.listVersions,SIGNAL("clicked(QModelIndex)"),self.on_ListVersion_clicked)
    def on_ListVersion_clicked(self,index):
        global NomVersion
        NomVersion= index.model().data(index,QtCore.Qt.DisplayRole)
        interface=interfaceEtude()
        window.setCentralWidget(interface)   
        
        
   
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())    
        
    def inserer(self):
        l=QtGui.QLayout
        #l.c
        #if (self.uiAjouter.isEnabled()):
        self.LabelEtude.show()
        self_ajout=WidgetAjout(self)
        #self.uiAjouter.isEnabled(False)
        self.clearLayout(self.verticalLayout_2)
        self.verticalLayout_2.addWidget(self_ajout)
        self.uiAjouter.setEnabled(False)
          
    def buttonPressed(self):
        font=QtGui.QFont("Segoe UI",9,QtGui.QFont.Bold,True)
        self.sender().setFont(font)
        
    def buttonReleased(self):
        font=QtGui.QFont("Segoe UI",10,QtGui.QFont.Bold,True)
        self.sender().setFont(font)        
          
        #QObject.connect(self.pushButton, SIGNAL("clicked()"),self.afficher)


winBase, winForm = uic.loadUiType('MainContainer.ui')

class MaFenetre(winBase,winForm):
    """
    - Si UiMaFenetre, importe depuis le designer a ete construit comme QMainWindow, 
        alors MaFenetre doit heriter de QMainWindow
    - si UiMafFenetre est construit dans designer comme un QWidget, alors MaFenetre doit     
        heriter de QWidget"""
    def __init__(self, parent=None):
        super(winBase,self).__init__(parent)
        self.setupUi(self)
        self.aficher_p = MaWidget(self)
         
        self.setCentralWidget(self.aficher_p)  
        
global window       
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle("windowsxp") 
    window= MaFenetre()
    start=time()
    spashScreen=QtGui.QPixmap("E:\Users\HA\workspace\PFE\ProjectRessources\logoO5.png")
    
    splash = QtGui.QSplashScreen(spashScreen)
    splash.show()
    sleep(1)
    
    splash.finish(window)
    locale = QLocale.system().name()
    translator=QTranslator()
    translator.load(u"qt_" + locale, QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)
    
    #temp0=interfaceAjout()
    #temp0=Widget2()
    window.show()
    
    #temp0.show()
    sys.exit(app.exec_())