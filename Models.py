#!/usr/bin/python2.7
# -*-coding:UTF-8-*-
import sys
import psycopg2
import datetime
from math import *


class Connexion ():
    
    _connexion = None
    
    def __init__(self):
        self._connexion=None
    
    @property
    def connexion(self):
        return self._connexion
    
    def ouvrirConnexion(self):
        strConnect ="dbname='projet' user='postgres' host='localhost' password=''" 
        try:
            self._connexion = psycopg2.connect(strConnect)
        except:
            self._connexion=None
            
    def fermerConnexion(self):
        self._connexion.close()
        self._connexion=None
class Etude():
    _idEtude=None
    _titre=None
    _description=None
    _type=None
    _dureeEtude=None
    _nature=None
    _secteur=None
    _produits=None
    _marche=None
    _societe=None
    _listInvestissements=None
    _listPromotteurs=None
    _listVersions=None
    _financement=None
    _changee=None

    def __init__(self,idEtude=None,titre=None,description=None,type=None,dureeEtude=None,nature=None,secteur=None,produits=None,marche=None,societe=None,changee=None):
        self._idEtude=idEtude
        self._titre=titre
        self._description=description
        self._type=type
        self._dureeEtude=dureeEtude
        self._nature=nature
        self._secteur=secteur
        self._produits=produits
        self._marche=marche
        self._societe=societe
        self._listInvestissements=self.getInvestissements()
        self._listPromotteurs=self.getPromotteurs()
        self._financement=self.getFinancement()
        self._listVersions=self.getListVersions()
        self._changee=changee
    def ajouter (self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('INSERT INTO "Etude" (titre, description,type,nature,secteur,produits,marche,societe,dureeetude,changee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (self.titre,self.description,self.type,self.nature,self.secteur,self.produits,self.marche,self.societe,self.dureeEtude,self.changee))
        c.commit()
        
        cnx.fermerConnexion()
    @staticmethod    
    def verifier(Etude):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('SELECT titre From "Etude"')
        rows = cursor.fetchall()
        cnx.fermerConnexion()
        for row in rows:
            if (Etude.titre==row[0]):
                return False
        return True 
    
        
    def modifier(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        cursor.execute('UPDATE "Etude" SET titre = '+"'"+self.titre+"'"+',  description = '+"'"+self.description+"'"+', type = '+"'"+self.type+"'"+', nature='+"'"+self.nature+"'"+' ,secteur='+"'"+self.secteur+"'"+',produits='+"'"+self.produits+"'"+',marche='+"'"+self.marche+"'"+',societe='+"'"+self.societe+"'"+',dureeetude= '+"'"+str(self.dureeEtude)+"'"+' WHERE id_etude = '+str(self.idEtude)+';')
        c.commit()
        cnx.fermerConnexion()
        
    def supprimer(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        
        cursor.execute('DELETE FROM "Etude" WHERE titre = '+"'"+self.titre+"'"+';')
        c.commit()
        cnx.fermerConnexion()
        return True    
    @property
    def listInvestissements(self):
        return self._listInvestissements
    @listInvestissements.setter
    def listInvestissements(self,value):
        self._listInvestissements=value  
    @property
    def listPromotteurs(self):
        return self._listPromotteurs
    @listPromotteurs.setter
    def listPromotteurs(self,value):
        self._listPromotteurs=value
    @property
    def listVersions(self):
        return self._listVersions
    @listVersions.setter
    def listVersions(self,value):
        self._listVersions=value           
    
    def getIdEtude(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('SELECT id_etude From "Etude" WHERE titre='+"'"+self.titre+"'")
        rows = cursor.fetchall()
        cnx.fermerConnexion()
        self.idEtude= rows[0][0]
        
    
    @property
    def idEtude(self):
        return self._idEtude
            
    @idEtude.setter
    def idEtude(self,value):
        self._idEtude=value
        
    @property
    def changee(self):
        return self._changee
            
    @changee.setter
    def changee(self,value):
        self._changee=value    
    
    @property
    def titre(self):
        return self._titre
    @titre.setter
    def titre(self,value):
        self._titre=value
        
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self,value):
        self._description=value
    
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self,value):
        self._type=value
        
    @property
    def dureeEtude(self):
        return self._dureeEtude
    @dureeEtude.setter
    def dureeEtude(self,value):
        self._dureeEtude=value
        
    @property
    def nature(self):
        return self._nature
    @nature.setter
    def nature(self,value):
        self._nature=value
    
    @property
    def secteur(self):
        return self._secteur
    @secteur.setter
    def secteur(self,value):
        self._secteur=value
        
    @property
    def produits(self):
        return self._produits
    @produits.setter
    def produits(self,value):
        self._produits=value
        
    @property
    def marche(self):
        return self._marche
    @marche.setter
    def marche(self,value):
        self._marche=value
        
    @property
    def societe(self):
        return self._societe
    @societe.setter
    def societe(self,value):
        self._societe=value
    @property
    def financement(self):
        return self._financement
    @financement.setter
    def financement(self,value):
        self._financement=value
        
    def getFinancement(self):
        if self.idEtude!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Financement" WHERE id_etude='+"'"+str(self.idEtude)+"'")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            fi=[]
            if (rows):
                for row in rows:
                    fi = Financement(row[0],row[1], self.idEtude)
                return fi
            else :
                return fi
        
    def getInvestissements(self):
        if self.idEtude!=None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Investissement" WHERE id_etude='+"'"+str(self.idEtude)+"'")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = Investissement(row[0], row[1], row[2], row[3], row[6], row[4], row[5], row[7], row[8], row[9], row[10], row[11], row[12])
                list.append(s)
            return list
        
    def getPromotteurs(self):
        if self.idEtude!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Promotteur" WHERE cin IN (SELECT cin From "PromotteurParEtude" WHERE id_etude='+"'"+str(self.idEtude)+"')")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = Promotteur(row[0], row[1], row[2], row[3], row[4], row[5])
                list.append(s)
            return list
    def getListVersions(self):
        if self.idEtude!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Version" WHERE id_etude='+"'"+str(self.idEtude)+"'")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = Version(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                list.append(s)
            return list
            
               
    @staticmethod     
    def getEtude(titre):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        req='SELECT * From "Etude" where titre='+"'"+str(titre)+"'"
        cursor.execute(req)
        rows = cursor.fetchall()
        for row in rows:
            etude=Etude(row[0],str(row[1]),str(row[2]),str(row[3]),row[9],str(row[4]),str(row[5]),str(row[6]),str(row[7]),str(row[8]))          
        cnx.fermerConnexion()
        return etude 
    
    @staticmethod     
    def getListEtude():
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        req='SELECT * From "Etude" '
        cursor.execute(req)
        rows = cursor.fetchall()
        cnx.fermerConnexion()
        list = []
        for row in rows:
            s = Etude(row[0],str(row[1]),str(row[2]),str(row[3]),row[9],str(row[4]),str(row[5]),str(row[6]),str(row[7]),str(row[8]))
            list.append(s)
        return list

     
    
       
class ArticleParVersion():
    _idArticle=None
    _idVersion=None
    
    def __init__(self,idArticle=None,idVersion=None):
        self._idArticle=idArticle
        self._idVersion=idVersion
        
    @property
    def idArticle(self):
        return self._idArticle
    @idArticle.setter
    def idArticle(self,value):
        self._idArticle=value
        
    @property
    def idVersion(self):
        return self._idVersion
    @idVersion.setter
    def idVersion(self,value):
        self._idVersion=value
        
        
    def ajouter(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            cursor.execute('INSERT INTO "ArticleParVersion" (id_article,id_version) VALUES (%s, %s)', (self.idArticle,self.idVersion))
            c.commit()
            cnx.fermerConnexion()
            
           
        
      
        
    def supprimer(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor() 
            #cursor.execute('DELETE FROM "Investissement" WHERE id_investissement=%s ', (self.idInvestissement))
            cursor.execute('DELETE FROM "ArticleParVersion" WHERE id_article = '+str(self.idArticle)+' AND id_version = '+str(self.idVersion)+' ;')
            c.commit()
            cnx.fermerConnexion()
            
    @staticmethod         
    def verifierArticle(article):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()    
            cursor.execute('SELECT id_article FROM "ArticleParVersion" WHERE id_article=  ' +"'"+ str(article.idArticle)+"';")
            c.commit()
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            if(len(rows)>1):
                return True
            else :
                return False   
        
               
class Version():
    _idVersion=None
    _numero=1
    _dateCreation=None
    _changee=False
    _van=None
    _tri=None
    _idEtude=None
    _listArticles=None
    _listProduits=None
    _listChargePersonnel=None
    _listFraisGeneraux=None
    _listProduitsFinis=None
    
    def __init__(self,idVersion=None,numero=None,dateCreation=None,changee=False,van=None,tri=None,idEtude=None):
        self._idVersion=idVersion
        self._numero=numero
        self._dateCreation=dateCreation
        self._changee=changee
        self._van=van
        self._tri=tri
        self._idEtude=idEtude
        self._listArticles=self.getListArticles()
        self._listProduits=self.getListProduits()
        self._listChargePersonnel=self.getListChargePersonnel()
        self._listFraisGeneraux=self.getListFraisGeneraux()
        self._listProduitsFinis=self.getListProduitsFinis()
    
    @property
    def idVersion(self):
        return self._idVersion
    @idVersion.setter
    def idVersion(self,value):
        self._idVersion=value
        
    @property
    def idEtude(self):
        return self._idEtude
    @idEtude.setter
    def idEtude(self,value):
        self._idEtude=value
        
    @property
    def numero(self):
        return self._numero
    @numero.setter
    def numero(self,value):
        self._numero=value
        
    @property
    def dateCreation(self):
        return self._dateCreation
    @dateCreation.setter
    def dateCreation(self,value):
        self._dateCreation=value
    
    @property
    def changee(self):
        return self._changee
    @changee.setter
    def changee(self,value):
        self._changee=value
        
    @property
    def van(self):
        return self._van
    @van.setter
    def van(self,value):
        self._van=value
        
    @property
    def tri(self):
        return self._tri
    @tri.setter
    def tri(self,value):
        self._tri=value
    @property
    def listAritcles(self):
        return self._listArticles
    @listAritcles.setter
    def listAritcles(self,value):
        self._listArticles=value
    @property
    def listProduits(self):
        return self._listProduits
    @listProduits.setter
    def listProduits(self,value):
        self._listProduits=value
    @property
    def listChargePersonnel(self):
        return self._listChargePersonnel
    @listChargePersonnel.setter
    def listChargePersonnel(self,value):
        self._listChargePersonnel=value
    @property
    def listFraisGeneraux(self):
        return self._listFraisGeneraux
    @listFraisGeneraux.setter
    def listFraisGeneraux(self,value):
        self._listFraisGeneraux=value  
    @property
    def listProduitsFinis(self):
        return self._listProduitsFinis
    @listProduitsFinis.setter
    def listProduitsFinis(self,value):
        self._listProduitsFinis=value                   
        
        
    def ajouter (self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('INSERT INTO "Version" (numero,date_creation,change,van,tri,id_etude) VALUES (%s, %s, %s, %s, %s, %s)', (self.numero,self.dateCreation,self.changee,self.van,self.tri,self.idEtude))
        c.commit()
        cnx.fermerConnexion()  
    def getListArticles(self):
        if self.idVersion!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Article" WHERE type <>'+"'produit'"+' AND fournisseur <>'+"''"+' AND id_article IN (SELECT id_article From "ArticleParVersion" WHERE id_version='+"'"+str(self.idVersion)+"')")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = Article(row[0], row[1], row[2], row[3], row[4], row[6], row[5])
                list.append(s)
            return list
        
    def getListProduits(self):
        if self.idVersion!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Article" WHERE type ='+"'"+'produit'+"'"+'  AND id_article IN (SELECT id_article From "ArticleParVersion" WHERE id_version='+"'"+str(self.idVersion)+"')")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = Article(row[0], row[1], row[2], row[3], row[4], row[6], row[5])
                list.append(s)
            return list
        
    def getListChargePersonnel(self):
        if self.idVersion!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "ChargePersonnel" WHERE id_version='+"'"+str(self.idVersion)+"'")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = ChargePersonnel(row[0], row[1], row[2], self.idVersion)
                list.append(s)
            return list
    def getListFraisGeneraux(self):
        if self.idVersion!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "FraisGeneraux" WHERE id_version='+"'"+str(self.idVersion)+"'")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = FraisGeneraux(row[0], row[1], row[2], self.idVersion)
                list.append(s)
            return list
        
    def getListProduitsFinis(self):
        if self.idVersion!= None:
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Article" WHERE type ='+"'"+'produit'+"'"+' OR type ='+"'"+'Fini'+"'"+' AND id_article IN (SELECT id_article From "ArticleParVersion" WHERE id_version='+"'"+str(self.idVersion)+"')")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list = []
            for row in rows:
                s = Article(row[0], row[1], row[2], row[3], row[4], row[6], row[5])
                list.append(s)
            return list               
            
          
    @staticmethod     
    def getVersion(num,id):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        req='SELECT * From "Version" where numero='+str(num)+'and id_etude='+str(id)
        cursor.execute(req)
        rows = cursor.fetchall()
        for row in rows:
            version=Version(row[0],row[1],row[2],row[3],row[4],row[5],row[6])          
        cnx.fermerConnexion()
        return version     
        


class PromotteurParEtude():
    _idEtude=None
    _cin=None
    
    def __init__(self,idEtude,cin):
        self._cin=cin
        self._idEtude=idEtude
    
    @property
    def idEtude(self):
        return self._idEtude
    @idEtude.setter
    def idEtude(self,value):
        self._idEtude=value
        
    @property
    def cin(self):
        return self._cin
    @cin.setter
    def cin(self,value):
        self._cin=value
        
    def ajouter(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            cursor.execute('INSERT INTO "PromotteurParEtude" (id_etude,cin) VALUES (%s, %s)', (self.idEtude,self.cin))
            c.commit()
            cnx.fermerConnexion()
            
           
        
      
        
    def supprimer(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
                      
            #cursor.execute('DELETE FROM "Investissement" WHERE id_investissement=%s ', (self.idInvestissement))
            cursor.execute('DELETE FROM "PromotteurParEtude" WHERE id_etude = '+str(self.idEtude)+' AND cin = '+"'"+(self.cin)+"'"+' ;')
            c.commit()
            cnx.fermerConnexion()
            
    @staticmethod         
    def verifierPE(promotteur,etude):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('SELECT cin FROM "PromotteurParEtude" WHERE cin= %s AND id_etude = %s ' , (promotteur.cin,etude.idEtude))
            c.commit()
            rows = cursor.fetchall()
            if (rows):
                return True
            else: 
                return False
            
                     
    @staticmethod         
    def verifierP(promotteur):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            print type(promotteur.cin)          
            cursor.execute('SELECT cin FROM "PromotteurParEtude" WHERE cin=  ' +"'"+ (promotteur.cin)+"';")
            c.commit()
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            if (rows):
                return True
            else : 
                return False
        
        
        
class Promotteur():
    
    _cin=None
    _nom=None
    _prenom=None
    _telephone=None
    _adresse=None
    _presentation=None
    
    
    
    def __init__(self,cin=None,nom=None,prenom=None,telephone=None,adresse=None,presentation=None):
        self._cin=cin
        self._nom=nom
        self._prenom=prenom
        self._telephone=telephone
        self._adresse=adresse
        self._presentation=presentation
        
    @property
    def cin(self):
        return self._cin
    @cin.setter
    def cin(self,value):
        self._cin=value
        
    @property
    def nom(self):
        return self._nom
    @nom.setter
    def nom(self,value):
        self._nom=value
        
    @property
    def prenom(self):
        return self._prenom
    @prenom.setter
    def prenom(self,value):
        self._prenom=value
        
    @property
    def telephone(self):
        return self._telephone
    @telephone.setter
    def telephone(self,value):
        self._telephone=value
        
        
        
    @property
    def adresse(self):
        return self._adresse
    @adresse.setter
    def adresse(self,value):
        self._adresse=value
        
    @property
    def presentation(self):
        return self._presentation
    @presentation.setter
    def presentation(self,value):
        self._presentation=value
    
      
        
    def ajouter(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            cursor.execute('INSERT INTO "Promotteur" (cin, nom,prenom,telephone,adresse,presentation) VALUES (%s, %s, %s, %s, %s, %s)', (self.cin,self.nom,self.prenom,self.telephone,self.adresse,self.presentation))
            c.commit()
            cnx.fermerConnexion()
             
        
    @staticmethod     
    def modifier(promotteur,id):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
                      
            cursor.execute('UPDATE "Promotteur" SET cin=%s,nom=%s,prenom=%s,telephone=%s ,adresse=%s,presentation=%s WHERE cin=%s', (promotteur.cin,promotteur.nom,promotteur.prenom,promotteur.telephone,promotteur.adresse,promotteur.presentation,id))
            c.commit()
            cnx.fermerConnexion()
         
        
    def supprimer(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
                      
            #cursor.execute('DELETE FROM "Investissement" WHERE id_investissement=%s ', (self.idInvestissement))
            cursor.execute('DELETE FROM "Promotteur" WHERE cin = '+"'"+(self.cin)+"'"+';')
            c.commit()
            cnx.fermerConnexion() 
    @staticmethod    
    def verifier(promotteur):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('SELECT cin FROM "Promotteur" WHERE cin= '+"'"+promotteur.cin+"';")
            c.commit()
            rows = cursor.fetchall()
            if (rows):
                return True
            else: 
               return False
         
    @staticmethod          
    def getPromotteur(cin):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        cursor.execute('SELECT * FROM "Promotteur" WHERE cin= '+"'"+cin+"'" )
        c.commit()
        rows = cursor.fetchall()
        if(rows):
            s=None
            for row in rows:
                s = Promotteur(row[0], row[1], row[2], row[3], row[4], row[5])
            return s
        
                       
               
        
class Financement():
    
    _idFinancement=None
    _montantPropre=None
    _idEtude=None
    _listCredits=None
    
    
    def __init__(self,idFinancement=None,montantpropre=None,idEtude=None):   
        
        self._idFinancement=idFinancement
        self._montantPropre=montantpropre
        self._idEtude=idEtude
        self._listCredits=self.getCredits()
        
       
    @property
    def idFinancement(self):
        return self._idFinancement
    @idFinancement.setter
    def idFinancement(self,value):
        self._idFinancement=value
        
    @property
    def idEtude(self):
        return self._idEtude
    
    @idEtude.setter
    def idEtude(self,value):
        self._idEtude=value    
        
    @property
    def montantPropre(self):
        return self._montantPropre
    @montantPropre.setter
    def montantPropre(self,value):
        self._montantPropre=value
        
    @property
    def listCredits(self):
        return self._listCredits
    @listCredits.setter
    def listCredits(self,value):
        self._listCredits=value
    
    def ajouter (self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        
        cursor.execute('INSERT INTO "Financement" (id_financement,montant_propre,id_etude) VALUES (%s, %s, %s);', (self.idFinancement,self.montantPropre,self.idEtude))
        c.commit()
        cnx.fermerConnexion()
     
    
       
    def modifier(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        
        cursor.execute('UPDATE "Financement" SET montant_propre = '+"'"+str(self.montantPropre)+"'"+' WHERE id_etude = '+"'"+str(self.idEtude)+"'"+';')
        c.commit()
        cnx.fermerConnexion()
        return True
    def getCredits(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c=cnx.connexion
        cursor = cnx.connexion.cursor()
        cursor.execute('SELECT * From "Credit" WHERE id_financement='+"'"+str(self.idFinancement)+"'")
        rows = cursor.fetchall()
        cnx.fermerConnexion()
        list=[]
        for row in rows:
            cr=Credit(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            list.append(cr)
        return list

class Credit():
    _idCredit=None
    _type=None
    _nomBanque=None
    _delaisRem=None
    _tauxInteret=None
    _delaisGrace =None
    _idFinancement=None
    _listsRemboursement=None
    _montant=None
    
    def __init__(self,idCredit=None,type=None,nomBanque=None,delaisRem=None,tauxInteret=None,delaisGrace =None,idFinancement=None,montant=None):
        self._idCredit=idCredit
        self._type=type
        self._nomBanque=nomBanque
        self._delaisRem=delaisRem
        self._tauxInteret=tauxInteret
        self._delaisGrace =delaisGrace 
        self._idFinancement=idFinancement
        self._montant=montant
        self._listsRemboursement=self.getRemboursement()
        
    @property
    def idCredit(self):
        return self._idCredit
    @idCredit.setter
    def idCredit(self,value):
        self._idCredit=value
        
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self,value):
        self._type=value
        
    @property
    def montant(self):
        return self._montant
    @montant.setter
    def montant(self,value):
        self._montant=value    
        
    @property
    def nomBanque(self):
        return self._nomBanque
    @nomBanque.setter
    def nomBanque(self,value):
        self._nomBanque=value
        
    @property
    def delaisRem(self):
        return self._delaisRem
    @delaisRem.setter
    def delaisRem(self,value):
        self._delaisRem=value
        
        
    @property
    def tauxInteret(self):
        return self._tauxInteret
    @tauxInteret.setter
    def tauxInteret(self,value):
        self._tauxInteret=value
        
    @property
    def delaisGrace (self):
        return self._delaisGrace 
    @delaisGrace .setter
    def delaisGrace (self,value):
        self._delaisGrace =value
        
    @property
    def idFinancement(self):
        return self._idFinancement
    @idFinancement.setter
    def idFinancement(self,value):
        self._idFinancement=value
        
        
    @property
    def listsRemboursement(self):
        return self.getRemboursement()
    @listsRemboursement.setter
    def listsRemboursement(self,value):
        self._listsRemboursement=value    
        
    def getRemboursement(self):
        if self.idCredit!=None:
            
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Remboursement" WHERE id_credit='+"'"+str(self.idCredit)+"'")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list=[]
            for row in rows:
                rem = Remboursement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])   
                list.append(rem)
            return list 
        
    def getIdCre(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        cursor.execute('SELECT id_credit FROM "Credit"')
        c.commit()
        rows = cursor.fetchall()      
        self.idCredit= rows[len(rows)-1][0]       
        
    def ajouter (self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('INSERT INTO "Credit" (type,nom_du_banque,delais_rem,taux_interet,delais_grace,id_financement,montant) VALUES (%s, %s,%s, %s,%s, %s,%s);', (self.type,self.nomBanque,self.delaisRem,self.tauxInteret,self.delaisGrace,self.idFinancement,self.montant))
        c.commit()
        cnx.fermerConnexion()
     
    
       
    def modifier(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        
        cursor.execute('UPDATE "Credit" SET type = '+"'"+str(self.type)+"'"+',nom_du_banque = '+"'"+str(self.nomBanque)+"'"+',delais_rem = '+"'"+str(self.delaisRem)+"'"+',taux_interet = '+"'"+str(self.tauxInteret)+"'"+',delais_grace = '+"'"+str(self.delaisGrace)+"'"+',id_financement = '+"'"+str(self.idFinancement)+"'"+',montant = '+"'"+str(self.montant)+"'"+' WHERE id_credit = '+"'"+str(self.idCredit)+"'"+';')
        c.commit()
        cnx.fermerConnexion()
        
    
    def supprimer(self):
        
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        #cursor.execute('DELETE FROM "Investissement" WHERE id_investissement=%s ', (self.idInvestissement))
        cursor.execute('DELETE FROM "Credit" WHERE id_credit = '+str(self.idCredit)+';')
        c.commit()
        cnx.fermerConnexion()
        
    def suppRem(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        
        cursor.execute('DELETE FROM "Remboursement" WHERE id_credit = '+str(self.idCredit)+';')
        c.commit()
        cnx.fermerConnexion()
        
            
    def calculRemboursement(self):
        interetCumule=0.0
        annuite=self.montant*((float(self.tauxInteret)/100)/(1-((1+(float(self.tauxInteret)/100))**(-self.delaisRem))))
        
        interet=self.montant*(float(self.tauxInteret)/100)
        interetCumule=interetCumule+interet
        amortissement=annuite-interet
        capitale=self.montant
        remboursement=Remboursement(None,self.idCredit,1,capitale,interet,amortissement,interetCumule,annuite)
        
        
        remboursement.ajouter()
        i=1
        
        while i<self.delaisRem:
            i=i+1
            capitale=capitale-amortissement
            interet=capitale*(float(self.tauxInteret)/100)
            amortissement=annuite-interet
            interetCumule=interetCumule+interet
            remboursement=Remboursement(None,self.idCredit,i,capitale,interet,amortissement,interetCumule,annuite)
            remboursement.ajouter()
            
               

class Remboursement():
    _idRem=None
    _idCredit=None
    _annee=None
    _capitalRestant=None
    _interet=None
    _amortissement=None
    _interetsCumules=None
    _annuite=None
    
    
    def __init__(self,idRem=None,idCredit=None,annee=None,capitalRestant=None,interet=None,amortissement=None,interetsCumules=None,annuite=None):
        self._idRem=idRem
        self._idCredit=idCredit
        self._annee=annee
        self._capitalRestant=capitalRestant
        self._interet=interet
        self._amortissement=amortissement
        self._interetsCumules=interetsCumules
        self._annuite=annuite

    @property
    def idRem(self):
        return self._idRem
    @idRem.setter
    def idRem(self,value):
        self._idRem=value
    
    
    @property
    def idCredit(self):
        return self._idCredit
    @idCredit.setter
    def idCredit(self,value):
        self._idCredit=value
    @property
    def annee(self):
        return self._annee
    @annee.setter
    def annee(self,value):
        self._annee=value
    @property
    def capitalRestant(self):
        return self._capitalRestant
    @capitalRestant.setter
    def capitalRestant(self,value):
        self._capitalRestant=value
    @property
    def interet(self):
        return self._interet
    @interet.setter
    def interet(self,value):
        self._interet=value
    @property
    def amortissement(self):
        return self._amortissement
    @amortissement.setter
    def amortissement(self,value):
        self._amortissement=value
    @property
    def interetsCumules(self):
        return self._interetsCumules
    @interetsCumules.setter
    def interetsCumules(self,value):
        self._interetsCumules=value
    @property
    def annuite(self):
        return self._annuite
    @annuite.setter
    def annuite(self,value):
        self._annuite=value
        
    def ajouter(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            
            cursor.execute('INSERT INTO "Remboursement" (id_credit,annee,capital_restant,interet,amortissement,interets_cumules ,annuite) VALUES (%s, %s, %s, %s, %s, %s, %s)', (self.idCredit,self.annee,self.capitalRestant,self.interet,self.amortissement,self.interetsCumules,self.annuite))
            c.commit()
            cnx.fermerConnexion()    
                                
        
        
    
    
class Investissement():
    _idInvestissement=None
    _designation=None
    _type=None
    _fournisseur=None
    _prix=None
    _idEtude=None
    _pays=None
    _quantite=None
    _prixTotal=None
    _typeAmortissement=None
    _dureVie=None
    _tauxAmortissement=None
    _dateAchat=None
    _listsAmortissement=None
    
    def __init__(self,idInvestissement=None,designation=None,type=None,fournisseur=None,pays=None,prix=None,idEtude=None,quantite=None,prixTotal=None,typeAmortissement=None,dureVie=None,tauxAmortissement=None,dateAchat=None):
        self._idInvestissement=idInvestissement
        self._designation=designation
        self._fournisseur=fournisseur
        self._prix=prix
        self._type=type
        self._idEtude=idEtude
        self._pays=pays
        self._quantite=quantite
        self._prixTotal=prixTotal
        self._typeAmortissement=typeAmortissement
        self._dureVie=dureVie
        self._tauxAmortissement=tauxAmortissement
        self._dateAchat=dateAchat
        self._listsAmortissement=self.getAmortissement()
    @property
    def idInvestissement(self):
        return self._idInvestissement
    @idInvestissement.setter
    def idInvestissement(self,value):
        self._idInvestissement=value
        
    @property
    def designation(self):
        return self._designation
    @designation.setter
    def designation(self,value):
        self._designation=value
        
    @property
    def idEtude(self):
        return self._idEtude
    
    @idEtude.setter
    def idEtude(self,value):
        self._idEtude=value    
        
    @property
    def fournisseur(self):
        return self._fournisseur
    @fournisseur.setter
    def fournisseur(self,value):
        self._fournisseur=value
        
    @property
    def prix(self):
        return self._prix
    @prix.setter
    def prix(self,value):
        self._prix=value
        
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self,value):
        self._type=value
     
    @property
    def pays(self):
        return self._pays
    @pays.setter
    def pays(self,value):
        self._pays=value
        
    @property
    def quantite(self):
        return self._quantite
    @quantite.setter
    def quantite(self,value):
        self._quantite=value
        
    @property
    def prixTotal(self):
        return self._prixTotal
    @prixTotal.setter
    def prixTotal(self,value):
        self._prixTotal=value
        
    @property
    def typeAmortissement(self):
        return self._typeAmortissement
    @typeAmortissement.setter
    def typeAmortissement(self,value):
        self._typeAmortissement=value
        
    @property
    def dureVie(self):
        return self._dureVie
    @dureVie.setter
    def dureVie(self,value):
        self._dureVie=value
        
    @property
    def tauxAmortissement(self):
        return self._tauxAmortissement
    @tauxAmortissement.setter
    def tauxAmortissement(self,value):
        self._tauxAmortissement=value 
    @property
    def dateAchat(self):
        return self._dateAchat
    @dateAchat.setter
    def dateAchat(self,value):
        self._dateAchat=value
        
        
    @property
    def listsAmortissement(self):
        return self.getAmortissement()
    @listsAmortissement.setter
    def listsAmortissement(self,value):
        self._listsAmortissement=value    
        
    def getAmortissement(self):
        if self.idInvestissement!=None:
            
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT * From "Amortissement" WHERE id_investissement='+"'"+str(self.idInvestissement)+"'")
            rows = cursor.fetchall()
            cnx.fermerConnexion()
            list=[]
            for row in rows:
                am = Amortissement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                list.append(am)
            return list      
                                 
    def suppRem(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        cursor.execute('DELETE FROM "Amortissement" WHERE id_investissement = '+str(self.idInvestissement)+';')
        c.commit()
        cnx.fermerConnexion()
            
    def ajouter(self):
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            cursor.execute('INSERT INTO "Investissement" (designation, type,fournisseur,prix,id_etude,pays,quantite,prix_total,type_amortissement,dure_vie,taux_amortissement,date_achat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (self.designation,self.type,self.fournisseur,self.prix,self.idEtude,self.pays,self.quantite,self.prixTotal,self.typeAmortissement,self.dureVie,self.tauxAmortissement,self.dateAchat))
            c.commit()
            cnx.fermerConnexion()
              
        
        
    def modifier(self):
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('UPDATE "Investissement" SET designation=%s,type=%s,fournisseur=%s,prix=%s ,pays=%s,quantite=%s,prix_total=%s,type_amortissement=%s,dure_vie=%s,taux_amortissement=%s,date_achat=%s WHERE id_investissement=%s', (self.designation,self.type,self.fournisseur,self.prix,self.pays,self.quantite,self.prixTotal,self.typeAmortissement,self.dureVie,self.tauxAmortissement,self.dateAchat,self.idInvestissement))
            c.commit()
            cnx.fermerConnexion() 
        
    def supprimer(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('DELETE FROM "Investissement" WHERE id_investissement = '+str(self.idInvestissement)+';')
            c.commit()
            cnx.fermerConnexion()
            
        
            
        
    @staticmethod    
    def verifier(investissement):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('SELECT * FROM "Investissement" WHERE designation= %s AND id_etude = %s ' , (investissement.designation , investissement.idEtude))
            c.commit()
            rows = cursor.fetchall()
            if (rows):
                print "true"
                return True
            else: 
                print "false"
                return False      
    
    def getIdInv(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        cursor.execute('SELECT id_investissement FROM "Investissement" WHERE designation= %s AND id_etude = %s ' , (self.designation , self.idEtude))
        c.commit()
        rows = cursor.fetchall()      
        self.idInvestissement= rows[0][0] 
        
        
    def calculRemboursement(self):
        
        if self.typeAmortissement=="lineaire":
            mois=int(self.dateAchat[0]+self.dateAchat[1])
            jour=int(self.dateAchat[3]+self.dateAchat[4])
            annee=int(self.dateAchat[6]+self.dateAchat[7]+self.dateAchat[8]+self.dateAchat[9])
            print "mois= "+str(mois)
            print "jour ="+str(jour) 
            
            if self.dateAchat[0]=="0" and self.dateAchat[1]=="1" and self.dateAchat[3]=="0" and self.dateAchat[4]=="1" :
                nbrLigne= self.dureVie
            else :
                nbrLigne= self.dureVie +1
                nbrJoursDE=(30-jour+1)+(12-mois)*30
                nbrJoursFIN=(jour-1)+(mois-1)*30
            if(nbrLigne!=self.dureVie):    
                base=self.prixTotal
                annuiteNormal=float(base)*float(self.tauxAmortissement/100)
                print nbrJoursDE
                print annuiteNormal
                premiereAnnuite=(annuiteNormal*float(nbrJoursDE))/360
                vnc=float(base)-float(premiereAnnuite)
                annuiteCumule=premiereAnnuite
                amortissement=Amortissement(None,self.idInvestissement,annee,base,premiereAnnuite,annuiteCumule,vnc,None,None)
                amortissement.ajouter()
                for i in range(nbrLigne-2):
                    annee=annee+1
                    annuiteCumule=annuiteCumule+annuiteNormal
                    premiereAnnuite=annuiteNormal
                    vnc=float(base)-float(annuiteCumule)
                    amortissement=Amortissement(None,self.idInvestissement,annee,base,premiereAnnuite,annuiteCumule,vnc,None,None)
                    amortissement.ajouter()
                annee=annee+1    
                derniereAnnuite=(annuiteNormal*float(nbrJoursFIN))/360
                annuiteCumule=annuiteCumule+derniereAnnuite
                vnc=float(base)-float(annuiteCumule)
                amortissement=Amortissement(None,self.idInvestissement,annee,base,derniereAnnuite,annuiteCumule,vnc,None,None)
                amortissement.ajouter()   
            else:
                base=self.prixTotal
                annuiteNormal=float(base)*float(self.tauxAmortissement/100)
                
                vnc=float(base)-float(annuiteNormal)
                annuiteCumule=annuiteNormal
                for i in range(nbrLigne):
                    amortissement=Amortissement(None,self.idInvestissement,annee,base,annuiteNormal,annuiteCumule,vnc,None,None)
                    amortissement.ajouter()
                    annuiteCumule=annuiteCumule+annuiteNormal
                    vnc=float(base)-float(annuiteCumule)
        else:
            mois=int(self.dateAchat[0]+self.dateAchat[1])
            jour=int(self.dateAchat[3]+self.dateAchat[4])
            annee=int(self.dateAchat[6]+self.dateAchat[7]+self.dateAchat[8]+self.dateAchat[9])
            nbrAnneeRestant=self.dureVie
            
            tauxLineaire=float(float(100)/nbrAnneeRestant)
            
            nbrMoisAacquisition=12-mois+1
            
            
            if self.dureVie <5:
                coefficient=1.25
            elif self.dureVie <7:
                coefficient=1.75
            else :
                coefficient=2.25
                
            tauxDegressif=tauxLineaire*coefficient
            
            base=float(self.prixTotal)
            annuite=float(base)*float(float(nbrMoisAacquisition)/12)*(float(tauxDegressif)/100)
            
            annuiteCumule=float(annuite)
            vnc=float(base)-float(annuite)
            
            while(tauxDegressif >= tauxLineaire):
                amortissement=Amortissement(None,self.idInvestissement,annee,base,annuite,annuiteCumule,vnc,nbrAnneeRestant,tauxLineaire)
                amortissement.ajouter()
                
                nbrAnneeRestant=nbrAnneeRestant-1
                tauxLineaire=float(float(100)/nbrAnneeRestant)
                base=float(vnc)
                if(tauxDegressif >= tauxLineaire):
                    annuite=float(vnc)*(float(self.tauxAmortissement)/100)
                    annuiteCumule=float(annuiteCumule)+float(annuite)
                    vnc=float(self.prixTotal)-float(annuiteCumule)
                    annee=annee+1
                    
                nbr=nbrAnneeRestant    
            annuite=float(vnc)*(float(tauxLineaire)/100)        
            for i in range(nbrAnneeRestant):
                annee=annee+1
                annuiteCumule=float(annuiteCumule)+float(annuite)
                print "prixTotal="+str(self.prixTotal)
                print "annuiteCumule="+str(annuiteCumule)
                vnc=float(self.prixTotal)-float(annuiteCumule)
                
                if self.prixTotal==annuiteCumule:
                    
                    print "rahom 9ad 9ad "
                amortissement=Amortissement(None,self.idInvestissement,annee,base,annuite,annuiteCumule,vnc,nbr,tauxLineaire)
                amortissement.ajouter()
                nbr=nbr-1    
                            
                
                               
               
            
            
                  
        

class Amortissement():
    _idAmortissement=None
    _base=None
    _annuite=None
    _vnc=None
    _annuiteCumulees=None
    _annee=None
    _idInvestissement=None
    _nbrAnneeRestants=None
    _tauxLineaire=None
    def __init__(self,id=None,idInvestissement=None,annee=None,base=None,annuite=None,annuiteCumulees=None,vnc=None,nbrAnnesRestants=None ,tauxLineaire=None):
        self._idAmortissement=id
        self._base=base
        self._annuite=annuite
        self._vnc=vnc
        self._annuiteCumulees=annuiteCumulees
        self._annee=annee
        self._idInvestissement=idInvestissement
        self._nbrAnneeRestants=nbrAnnesRestants
        self._tauxLineaire=tauxLineaire
    @property
    def idAmortissement(self):
        return self._idAmortissement
    @idAmortissement.setter
    def idAmortissement(self,value):
        self._idAmortissement=value
        
    @property
    def base(self):
        return self._base
    @base.setter
    def base(self,value):
        self._base=value
        
    @property
    def annuite(self):
        return self._annuite
    @annuite.setter
    def annuite(self,value):
        self._annuite=value
        
    @property
    def vnc(self):
        return self._vnc
    @vnc.setter
    def vnc(self,value):
        self._vnc=value
        
    @property
    def tauxLineaire(self):
        return self._tauxLineaire
    @tauxLineaire.setter
    def tauxLineaire(self,value):
        self._tauxLineaire=value
        
    @property
    def annuiteCumulees(self):
        return self._annuiteCumulees
    @annuiteCumulees.setter
    def annuiteCumulees(self,value):
        self._annuiteCumulees=value
    @property
    def annee(self):
        return self._annee
    @annee.setter
    def annee(self,value):
        self._annee=value 
        
    @property
    def idInvestissement(self):
        return self._idInvestissement
    @idInvestissement.setter
    def idInvestissement(self,value):
        self._idInvestissement=value
    @property
    def nbrAnneeRestants(self):
        return self._nbrAnneeRestants
    @nbrAnneeRestants.setter
    def nbrAnneeRestants(self,value):
        self._nbrAnneeRestants=value    
            
    def ajouter(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            cursor.execute('INSERT INTO "Amortissement" (id_investissement,annee,base,annuite,annuite_cumulees,vnc ,nbr_annee_restants,taux_lineaire) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (self.idInvestissement,self.annee,self.base,self.annuite,self.annuiteCumulees,self.vnc,self.nbrAnneeRestants,self.tauxLineaire))
            c.commit()
            cnx.fermerConnexion()
                

class Article ():
    _idArticle=None
    _designation=None
    _type=None
    _fournisseur=None
    _prixAchat=None
    _prixVente=None
    _uniteMesure=None
    _listNomenclature=None
    
    def __init__(self,idArticle=None,designation=None,type=None,fournisseur=None,prixAchat=None,prixVente=None,uniteMesure=None):
        self._idArticle=idArticle
        self._designation=designation
        self._fournisseur=fournisseur
        self._type=type
        self._prixAchat=prixAchat
        self._prixVente=prixVente
        self._uniteMesure=uniteMesure
        self._listNomenclature=self.getListNomenclatureParArticle()
  
    @property
    def idArticle(self):
        return self._idArticle
    @idArticle.setter
    def idArticle(self,value):
        self._idArticle=value
        
    @property
    def designation(self):
        return self._designation
    @designation.setter
    def designation(self,value):
        self._designation=value
        
    @property
    def fournisseur(self):
        return self._fournisseur
    @fournisseur.setter
    def fournisseur(self,value):
        self._fournisseur=value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self,value):
        self._type=value 
    @property
    def prixAchat(self):
        return self._prixAchat
    @prixAchat.setter
    def prixAchat(self,value):
        self._prixAchat=value 
    @property
    def prixVente(self):
        return self._prixVente
    @prixVente.setter
    def prixVente(self,value):
        self._prixVente=value     
    @property
    def uniteMesure(self):
        return self._uniteMesure
    @uniteMesure.setter
    def uniteMesure(self,value):
        self._uniteMesure=value 
    @property
    def listNomenclature(self):
        return self._listNomenclature
    @listNomenclature.setter
    def listNomenclature(self,value):
        self._listNomenclature=value                        
           
            
            
    def ajouter(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
            cursor.execute('INSERT INTO "Article" (designation, type,fournisseur,prix_achat,prix_vente,unite_mesure) VALUES (%s, %s, %s, %s, %s, %s)', (self.designation,self.type,self.fournisseur,self.prixAchat,self.prixVente,self.uniteMesure))
            c.commit()
            cnx.fermerConnexion()
              
        
        
    def modifier(self):

            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('UPDATE "Article" SET designation=%s,type=%s,fournisseur=%s,prix_achat=%s,prix_vente=%s,unite_mesure=%s WHERE id_article =%s', (self.designation,self.type,self.fournisseur,self.prixAchat,self.prixVente,self.uniteMesure,self.idArticle))
            c.commit()
            cnx.fermerConnexion()

        
    def supprimer(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('DELETE FROM "Article" WHERE id_article = '+str(self.idArticle)+';')
            c.commit()
            cnx.fermerConnexion()
            
        
            
        
    @staticmethod    
    def verifier(article,id):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()          
            cursor.execute('SELECT designation FROM "Article" WHERE id_article IN(select id_article FROM "ArticleParVersion" WHERE id_version= '+str(id)+') AND designation= '+"'"+str(article.designation )+"' ")
            c.commit()
            rows = cursor.fetchall()
            if (rows):
                return True
            else: 
                return False  
    def getIdArticle(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        cursor.execute('SELECT id_article FROM "Article" WHERE designation= '+"'"+str(self.designation )+"'")
        c.commit()
        rows = cursor.fetchall()      
        self.idArticle= rows[0][0]
    @staticmethod     
    def getListNomenclatures(id):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        req='SELECT * From "Article" where type='+"'Consommable'"+'OR type ='+"'Matiere premiere'"+' AND id_article IN(SELECT id_article From "ArticleParVersion" WHERE id_version = '+str(id)+')'
        cursor.execute(req)
        rows = cursor.fetchall()
        list=[]
        for row in rows :
            n =Article(row[0], row[1], row[2], row[3], row[4], row[6], row[5])
            list.append(n)
        return list  
    def supprimeListNomenclatureParArticle(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        cursor.execute('DELETE FROM "Nomenclature" WHERE id_composant = '+str(self.idArticle)+';')
        c.commit()
        cnx.fermerConnexion() 
    
    def getListNomenclatureParArticle(self):
        if self.idArticle != None :
            list=[]
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c=cnx.connexion
            cursor = cnx.connexion.cursor()
            cursor.execute('SELECT id_composite,quantite From "Nomenclature" WHERE id_composant ='+"'"+str(self.idArticle)+"'")
            rows = cursor.fetchall()
            for row in rows :
                cursor.execute('SELECT designation From "Article" WHERE id_article='+"'"+str(row[0])+"'")
                r= cursor.fetchall()
                l=[r[0][0],row[1]]
                list.append(l)    
            cnx.fermerConnexion() 
            
            return list      
    @staticmethod 
    def getPrix(designation):
        
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        req='SELECT prix_achat From "Article" where designation='+"'"+str(designation)+"'"
        cursor.execute(req)
        rows = cursor.fetchall()
        return rows 
        
    @staticmethod    
    def getArticle(id):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        req='SELECT * From "Article" where id_article='+"'"+id+"'"
        cursor.execute(req)
        rows = cursor.fetchall()
        ar = Article(rows[0], rows[1], rows[2], rows[3], rows[4], rows[6], rows[5])
        return ar 
            

class Nomenclature():
    _idComposant=None
    _idComposite=None
    _quantite=None
    
    def __init__(self,idComposant=None,idComposite=None,quantite=None):
        
        self._idComposant=idComposant
        self._idComposite=idComposite
        self._quantite=quantite
    
    @property
    def idComposant(self):
        return self._idComposant
    @idComposant.setter
    def idComposant(self,value):
        self._idComposant=value
        
    @property
    def idComposite(self):
        return self._idComposite
    @idComposite.setter
    def idComposite(self,value):
        self._idComposite=value
        
    @property
    def quantite(self):
        return self._quantite
    @quantite.setter
    def quantite(self,value):
        self._quantite=value
        
        
    def ajouter(self):
        
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        
        cursor.execute('INSERT INTO "Nomenclature" (id_composant,id_composite,quantite) VALUES (%s, %s, %s)', (self.idComposant,self.idComposite,self.quantite))
        c.commit()
        cnx.fermerConnexion()
            
           
        
      
        
    def supprimer(self):
        
            cnx=Connexion()
            cnx.ouvrirConnexion()
            c = cnx.connexion
            cursor = c.cursor()
                      
            #cursor.execute('DELETE FROM "Investissement" WHERE id_investissement=%s ', (self.idInvestissement))
            cursor.execute('DELETE FROM "PromotteurParEtude" WHERE id_etude = '+str(self.idEtude)+' AND cin = '+"'"+(self.cin)+"'"+' ;')
            c.commit()
            cnx.fermerConnexion()    
        
class Charge ():
    _idCharge=None
    _designation=None
    _idVersion=None
    
    def __init__(self,idCharge=None,designation=None,idVersion=None):
        self._idCharge=idCharge
        self._designation=designation
        self._idVersion=idVersion
        
    
    
    @property
    def idCharge(self):
        return self._idCharge
    @idCharge.setter
    def idCharge(self,value):
        self._idCharge=value
    @property
    def designation(self):
        return self._designation
    @designation.setter
    def designation(self,value):
        self._designation=value
    @property
    def idVersion(self):
        return self._idVersion
    @idVersion.setter
    def idVersion(self,value):
        self._idVersion=value    
    def ajouter (self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('INSERT INTO "Charge" (designation,id_version) VALUES (%s, %s);', (self.designation,self.idVersion))
        c.commit()
        cnx.fermerConnexion()
     
    
     
    def modifier(self,designation):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        
        cursor.execute('UPDATE "Charge" SET designation = '+"'"+str(self.designation)+"'"+' WHERE designation = '+"'"+str(designation)+"'"+';')
        c.commit()
        cnx.fermerConnexion()
        
    
    def supprimer(self):
        
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        #cursor.execute('DELETE FROM "Investissement" WHERE id_investissement=%s ', (self.idInvestissement))
        cursor.execute('DELETE FROM "Charge" WHERE id_charge = '+"'"+str(self.idCharge)+"'"+';')
        c.commit()
        cnx.fermerConnexion()
    @staticmethod    
    def verifier(charge):
        
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        cursor.execute('SELECT designation FROM "Charge" WHERE designation= %s AND id_version = %s ' , (charge.designation , charge.idVersion))
        c.commit()
        rows = cursor.fetchall()
        if (rows):
            return True
        else: 
            return False    
    @staticmethod              
    def getId(charge):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = c.cursor()          
        cursor.execute('SELECT id_charge FROM "Charge" WHERE designation= %s AND id_version = %s ' , (charge.designation , charge.idVersion))
        c.commit()
        rows = cursor.fetchall()
        return rows[0][0]
               
       
class ChargePersonnel(Charge):
    _salaire=None

    
    
    def __init__(self,idCharge=None,designation=None,salaire=None,idVersion=None):
        Charge.__init__(self, idCharge, designation, idVersion)
        self._salaire=salaire
        

        
        
    
        
    @property
    def salaire(self):
        return self._salaire
    @salaire.setter
    def salaire(self,value):
        self._salaire=value
        
   
                 
        
    def ajouter (self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('INSERT INTO "ChargePersonnel" (id_charge,designation,salaire,id_version) VALUES (%s, %s, %s, %s);', (self.idCharge,self.designation,self.salaire,self.idVersion))
        c.commit()
        cnx.fermerConnexion()
     
    
       
    def modifier(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        
        cursor.execute('UPDATE "ChargePersonnel" SET designation= '+"'"+str(self.designation)+"'"+',salaire= '+str(self.salaire)+' WHERE id_charge = '+"'"+str(self.idCharge)+"'"+';')
        c.commit()
        cnx.fermerConnexion()
        
    
    
         

class FraisGeneraux(Charge):
    
    
    _montant=None
    
    
    def __init__(self,idCharge=None,designation=None,montant=None,idVersion=None):
        Charge.__init__(self, idCharge, designation, idVersion)
        self._montant=montant
        self._idVersion=idVersion
    
   
   
        
    @property
    def montant(self):
        return self._montant
    @montant.setter
    def montant(self,value):
        self._montant=value
          
    def ajouter (self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()            
        cursor.execute('INSERT INTO "FraisGeneraux" (id_charge,designation,montant,id_version) VALUES (%s, %s, %s, %s);', (self.idCharge,self.designation,self.montant,self.idVersion))
        c.commit()
        cnx.fermerConnexion()
     
    
       
    def modifier(self):
        cnx=Connexion()
        cnx.ouvrirConnexion()
        c = cnx.connexion
        cursor = cnx.connexion.cursor()
        
        cursor.execute('UPDATE "FraisGeneraux" SET designation ='+"'"+str(self.designation)+"'"+',montant = '+str(self.montant)+' WHERE id_charge = '+"'"+str(self.idCharge)+"'"+';')
        c.commit()
        cnx.fermerConnexion()
        
    
      
            
        
"""   
if __name__ == '__main__':
    a=Connexion()
    print a.connexion
    a.ouvrirConnexion()
    print a.connexion
    print "------------------------------- Connected -------------------------------"
    a=Etude()
    a.description="fdsgdf"
    a.marche="gdsfds"
    a.ajouter()
"""
              