from pyfiglet import Figlet
import datetime

def AfficheTitreApplication():
    custom_fig = Figlet(font='big')
    print(custom_fig.renderText('F38C Init'))

def AfficheInstructionUtilisateur():
    #instructions pour l'utilisateur
    print("Cet outil génère un fichier 'c' avec les initialisation hardware pour le microcontrôlleur F38C" )
    print("pour cela écrivez ce qui vous est demandé puis pressez 'Enter'")

def GetDescription():
    print("Décrivez votre projet pour l'en-tête de votre code (max 226 caractères)")
    description = input()
    # détecte une description trop longue pour une ligne et la coupe en plusieurs lignes
    if len(description) > 67: 
        caracteres = list(description)
        spaceFound = False
        spacePosition = 0
        for index in range(67):
            if caracteres[67-index] == " ":
                spaceFound = True
                spacePosition = 67 - index
                break
        if spaceFound:
            caracteres[spacePosition] = '\n'
        if len(caracteres) > 146:
            for index in range(80):
                if caracteres[146-index] == " ":
                    spaceFound = True
                    spacePosition = 146 - index
                    break
            if spaceFound:
                caracteres[spacePosition] = '\n'

        return "".join(caracteres)

def RecupInfoEntete():
    print("Commençons par l'en-tête du programme vous pouvez laisser ces champs vides si vous le souhaitez")
    #nom Projet
    print("Entrez un nom pour votre projet")
    nomProjet = input()
    #nom utilisateur
    print("Quel est votre nom?")
    nomAuteur = input()
    #date
    dt = datetime.datetime.today() 
    date = dt.strftime('%d/%m/%Y')
    print("La date de création du projet est: " + date)
    #description
    description = GetDescription()
    return [nomProjet,nomAuteur,date,description]

def ChoixClockSysteme():
    print("à quelle vitesse le clock système doit-il tourner ?")
    print("(Options : 10Khz, 20Khz, 40Khz, 80Khz, 1.5Mhz, 3Mhz, 6Mhz, 12Mhz, 24Mhz, 48Mhz)")
    print("entrer la valeur en Khz ex: 48Mhz --> 48000")
    print("si aucune valeur (ou une valeur non valide est rentrée le clock est par défaut à 48Mhz)")
    vitesseClockSysteme = input()
    if vitesseClockSysteme.isdigit():
        vitesseClockSysteme = int(vitesseClockSysteme)
    else:
        vitesseClockSysteme = 48000
    listeDeValeursPossibles = [10,20,40,80,1500,3000,6000,12000,24000,48000]
    ValeurCorrecteTrouvee = False
    for ValeurCorrecte in listeDeValeursPossibles:
        if vitesseClockSysteme == ValeurCorrecte:
            ValeurCorrecteTrouvee = True
    if not(ValeurCorrecteTrouvee) :
        vitesseClockSysteme = 48000
    return vitesseClockSysteme

if __name__ == "__main__":
    AfficheTitreApplication()
    AfficheInstructionUtilisateur()
    informationsEntete = RecupInfoEntete()
    clockSysteme = ChoixClockSysteme()

    #region Creation du fichier
    fileName = informationsEntete[0] + '.c'
    Fichier = open(fileName, 'w')
    #En-tête
    Fichier.write("/*==============================================================================" + '\n')
    Fichier.write("Projet           : " + informationsEntete[0] + '\n')
    Fichier.write("Auteur           : " + informationsEntete[1] + '\n')
    Fichier.write("Date de creation : " + informationsEntete[2] + '\n')
    Fichier.write("================================================================================" + '\n')
    Fichier.write("Descriptif : " + str(informationsEntete[3]) + '\n') # conversion en string car peut être de "non-type" et genere un erreur
    Fichier.write("==============================================================================*/" + '\n')
    Fichier.write("#include <reg51f380.h>" + '\n')
    Fichier.write('\n')
    Fichier.write("//= CONSTANTES =================================================================" + '\n')
    Fichier.write('\n')
    
    #Fonctions Prototypes
    Fichier.write("//= FONCTIONS PROTOTYPES =======================================================" + '\n')
    Fichier.write("void ClockInit ();   //init. du clock systeme" + '\n')
    Fichier.write("void PortInit ();    //init. des Ports" + '\n')
    Fichier.write('\n')
    Fichier.write("void main ()" + '\n')
    Fichier.write("{" + '\n')
    Fichier.write("   //--- Variables locales -----------------------------------------------------" + '\n')
    Fichier.write('\n')
    Fichier.write("   //--- Initialisations Uc ----------------------------------------------------" + '\n')
    Fichier.write('\n')
    Fichier.write("   PCA0MD &= ~0x40;  // WDTE = 0 (disable watchdog timer)" + '\n')
    Fichier.write("   ClockInit ();" + '\n')
    Fichier.write("   PortInit ();" + '\n')
    Fichier.write('\n')
    Fichier.write("   //--- Boucle Infinie -------------------------------------------------------" + '\n')
    Fichier.write("   while (1)" + '\n')
    Fichier.write("   {" + '\n')
    Fichier.write("   }" + '\n')
    Fichier.write("}" + '\n')
    Fichier.write('\n')

    #Clock init.
    Fichier.write("/*-----------------------------------------------------------------------------" + '\n')
    Fichier.write("ClockInit ()" + '\n')
    Fichier.write("-------------------------------------------------------------------------------" + '\n')
    Fichier.write("Descriptif: Init. du clock systeme" + '\n')
    Fichier.write("Entree    : --" + '\n')
    Fichier.write("Sortie    : --" + '\n')
    Fichier.write("-----------------------------------------------------------------------------*/" + '\n')
    Fichier.write("void ClockInit ()" + '\n')
    Fichier.write("{" + '\n')
    if clockSysteme == 48000 or clockSysteme == 24000:
        Fichier.write("   OSCLCN = 0x00;" + '\n')
        if clockSysteme == 48000:
            Fichier.write("   CLKSEL = 0x03;" + '\n')
        else:
            Fichier.write("   CLKSEL = 0x02;" + '\n')
        Fichier.write("   OSCICN = 0x83;" + '\n')
        if clockSysteme == 48000:
            Fichier.write("   FLSCL  = 0x90;" + '\n')
    if clockSysteme == 1500 or clockSysteme == 3000 or clockSysteme == 6000 or clockSysteme == 12000:
        Fichier.write("   OSCLCN = 0x00;" + '\n')
        Fichier.write("   CLKSEL = 0x00;" + '\n')
        if clockSysteme == 1500:
            Fichier.write("   OSCICN = 0x80;" + '\n')
        if clockSysteme == 3000:
            Fichier.write("   OSCICN = 0x81;" + '\n')
        if clockSysteme == 6000:
            Fichier.write("   OSCICN = 0x82;" + '\n')
        if clockSysteme == 12000:
            Fichier.write("   OSCICN = 0x83;" + '\n')
    if clockSysteme == 10 or clockSysteme == 20 or clockSysteme == 40 or clockSysteme == 80:
        if clockSysteme == 10:
            Fichier.write("   OSCLCN = 0x80;" + '\n')
        if clockSysteme == 20:
            Fichier.write("   OSCLCN = 0x81;" + '\n')
        if clockSysteme == 40:
            Fichier.write("   OSCLCN = 0x82;" + '\n')
        if clockSysteme == 80:
            Fichier.write("   OSCLCN = 0x83;" + '\n')
        Fichier.write("   CLKSEL = 0x04;" + '\n')
        Fichier.write("   OSCICN = 0x00;" + '\n')
    Fichier.write("} // ClockInit ----------------------------------------------------------------" + '\n')
    Fichier.write('\n')

    #Port init.
    Fichier.write("/*-----------------------------------------------------------------------------" + '\n')
    Fichier.write("PortInit ()" + '\n')
    Fichier.write("-------------------------------------------------------------------------------" + '\n')
    Fichier.write("Descriptif: Init. des Ports" + '\n')
    Fichier.write("Entree    : --" + '\n')
    Fichier.write("Sortie    : --" + '\n')
    Fichier.write("-----------------------------------------------------------------------------*/" + '\n')
    Fichier.write("void PortInit ()" + '\n')
    Fichier.write("{" + '\n')  
    Fichier.write("   XBR1 |= 0x40;   // autorise le fonctionnement du crossbar" + '\n')
    #Fichier.write("   XBR0 |= 0x01;   // autorise l'UART 0x01 ou sysclock sur P0^0 0x08" + '\n')
    Fichier.write("} // PortInit -----------------------------------------------------------------" + '\n')

    Fichier.close()
    print("Le fichier " + informationsEntete[0] + ".c à été créé")
    #endregion