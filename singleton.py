# Classe Journal avec pattern Singleton
class Journal:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Journal, cls).__new__(cls)
            cls._instance.journal = ""
        return cls._instance
    
    def ajouter(self, message):
        self.journal += message + "\n"
    
    def afficher(self):
        print(" JOURNAL UNIQUE POUR TOUS LES COMPTES")
        print(self.journal, end="")

# Classe abstraite Compte
class Compte:
    def __init__(self, num, nom, depot=0):
        self.solde = depot
        self.titulaire = nom
        self.numero = num
    
    def getSolde(self):
        return self.solde
    
    def setSolde(self, value):
        self.solde = value
    
    def getTitulaire(self):
        return self.titulaire
    
    def setTitulaire(self, nom):
        self.titulaire = nom
    
    def getNumero(self):
        return self.numero
    
    def __str__(self):
        return f"Compte n° {self.numero} de M. {self.titulaire} solde = {self.solde} E"
    
    def consulter(self):
        print(self.__class__.__name__)
        print(self)
        print()
    
    def deposer(self, somme):
        import datetime
        journal = Journal()
        date_actuelle = datetime.datetime.now().strftime("%d/%m/%Y")
        
        if somme > 0:
            self.solde += somme
            journal.ajouter(f"{date_actuelle} INFO Dépôt de {somme} Euros sur le compte {self.numero}")
        else:
            journal.ajouter(f"{date_actuelle} INFO Echec Retrait de {somme} Euros sur le compte {self.numero} : Somme négative")
    
    def retirer(self, somme):
        import datetime
        journal = Journal()
        date_actuelle = datetime.datetime.now().strftime("%d/%m/%Y")
        
        if somme <= 0:
            journal.ajouter(f"{date_actuelle} INFO Echec Retrait de {somme} Euros sur le compte {self.numero} : Somme négative")
            return

# Classe CompteCourant
class CompteCourant(Compte):
    def __init__(self, num, nom, depot=0, decouv=0):
        super().__init__(num, nom, depot)
        self.decouvertAutorise = decouv
    
    def __str__(self):
        return super().__str__() + f" < découvert aut. {self.decouvertAutorise} E >"
    
    def deposer(self, somme):
        super().deposer(somme)
    
    def retirer(self, somme):
        import datetime
        journal = Journal()
        date_actuelle = datetime.datetime.now().strftime("%d/%m/%Y")
        
        journal.ajouter(f"{date_actuelle} INFO Tentative Retrait de {somme} Euros sur le compte {self.numero}")
        
        if somme > 0:
            if somme <= self.solde + self.decouvertAutorise:
                frais = 0
                if somme > self.solde:
                    frais = 0.12 * (somme - self.solde)
                self.solde = self.solde - somme - frais
            else:
                journal.ajouter(f"{date_actuelle} INFO Echec Tentative Retrait de {somme} Euros sur le compte {self.numero} : Decouvert dépassé")

# Classe CompteLivret
class CompteLivret(Compte):
    def __init__(self, num, nom, depot, taux):
        super().__init__(num, nom, depot)
        self.taux = taux
    
    def __str__(self):
        return super().__str__() + f" < taux {self.taux*100} % >"
    
    def deposer(self, somme):
        super().deposer(somme)
        self.solde += somme * self.taux
    
    def retirer(self, somme):
        import datetime
        journal = Journal()
        date_actuelle = datetime.datetime.now().strftime("%d/%m/%Y")
        
        journal.ajouter(f"{date_actuelle} INFO Tentative Retrait de {somme} Euros sur le compte {self.numero}")
        
        if somme > 0:
            if somme <= self.solde:
                self.solde -= somme
            else:
                journal.ajouter(f"{date_actuelle} INFO Echec Tentative Retrait de {somme} Euros sur le compte {self.numero} : Solde insuffisant")

# Programme principal de test
class Prog:
    @staticmethod
    def main():
        compte1 = CompteCourant("123", "Dupont", 0, 1000)
        compte2 = CompteLivret("456", "Martin", 0, 0.05)
        
        # Opérations sur les comptes
        compte1.deposer(100.0)
        compte1.retirer(-80.0)
        compte1.retirer(2000.0)
        compte2.retirer(1000.0)
        
        # Affichage du journal
        journal = Journal()
        journal.afficher()

# Exécution du programme
if __name__ == "__main__":
    Prog.main()
