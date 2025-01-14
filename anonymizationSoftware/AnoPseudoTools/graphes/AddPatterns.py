"""
Ce code source contient le code utilisé pour faire construire nos automates finis
"""

"""
états finaux 
S4; S6; S9 ; S16
"""
from AnoPseudoTools.graphes.Graphe import MyGraph
class AddPartterns():

    def __init__(self) -> None:
        
        self.MyGraphe=MyGraph()

    
    def addPatternsGraphLoc(self):

        """
        Pattern commençant par CLS 
        """
        #Automate fini commençant par CLS GV P GN
        self.MyGraphe.add_arc(("S00","S01"),"CLS")
        self.MyGraphe.add_arc(("S01","S02"),"GV")
        self.MyGraphe.add_arc(("S02","S03"),"P")
        self.MyGraphe.add_arc(("S03","S04"),"GN")

        #Automate fini commençant par CLS GV P GN CC GN
        self.MyGraphe.add_arc(("S04","S10"),"CC")
        self.MyGraphe.add_arc(("S11","S12"),"GN")

        #Automate fini commençant par CLS GV P NC P GN 
        self.MyGraphe.add_arc(("S03","S20"),"NC")
        self.MyGraphe.add_arc(("S20","S21"),"P")
        self.MyGraphe.add_arc(("S21","S22"),"GN")

        #Automate fini commençant par CLS CLR GV DET U P GN
        self.MyGraphe.add_arc(("S01","S30"),"CLR")
        self.MyGraphe.add_arc(("S30","S31"),"GV")
        self.MyGraphe.add_arc(("S31","S32"),"DET")
        self.MyGraphe.add_arc(("S32","S33"),"U")
        self.MyGraphe.add_arc(("S33","S34"),"P")
        self.MyGraphe.add_arc(("S34","S35"),"GN")

        #Automate fini commençant par CLS CLR GV P DET GN
        self.MyGraphe.add_arc(("S31","S40"),"P")
        self.MyGraphe.add_arc(("S40","S41"),"DET")
        self.MyGraphe.add_arc(("S41","S42"),"GN")

        #Automate fini commençant par CLS GV GN
        self.MyGraphe.add_arc(("S02","S50"),"GN")

        #Automate fini commençant par CLS CLR GV P GN
        self.MyGraphe.add_arc(("S40","S60"),"GN")

        #Automate fini commençant par CLS CLO GV P GN
        self.MyGraphe.add_arc(("S01","S70"),"CLO")
        self.MyGraphe.add_arc(("S70","S02"),"GV")

        #Automate fini commençant par CLS CLR GV P GN
        self.MyGraphe.add_arc(("S01","S80"),"CLR")
        self.MyGraphe.add_arc(("S80","S02"),"GV")

        """
        Pattern commençant par DET
        """
        #Automate fini commençant par DET NC P GN
        self.MyGraphe.add_arc(("S00","T01"),"DET")
        self.MyGraphe.add_arc(("T01","T02"),"NC")
        self.MyGraphe.add_arc(("T02","T03"),"P")
        self.MyGraphe.add_arc(("T03","T04"),"GN")

        #Automate fini commençant par DET NC GN
        self.MyGraphe.add_arc(("T02","T10"),"GN")

        """
        Pattern commençant par DETWH
        """
        #Automate fini commençant par DETWH ADJ GN
        self.MyGraphe.add_arc(("S00","P01"),"DETWH")
        self.MyGraphe.add_arc(("P01","P02"),"ADJ")
        self.MyGraphe.add_arc(("P02","P03"),"GN")

        #Automate fini commençant par DETWH NC P GN
        self.MyGraphe.add_arc(("P01","P10"),"NC")
        self.MyGraphe.add_arc(("P10","P11"),"P")
        self.MyGraphe.add_arc(("P11","P12"),"GN")

        """
        Pattern commençant par P
        """
        #Automate fini commençant par P DET NC P GN
        self.MyGraphe.add_arc(("S00","U01"),"P")
        self.MyGraphe.add_arc(("U01","U02"),"DET")
        self.MyGraphe.add_arc(("U02","U03"),"NC")
        self.MyGraphe.add_arc(("U03","U04"),"P")
        self.MyGraphe.add_arc(("U04","U05"),"GN")

        #Automate fini commençant par P DET NC  GN
        self.MyGraphe.add_arc(("U03","U10"),"GN")
        
        """
        Pattern commençant par P
        """
        #Automate fini commençant par P GV P GN
        self.MyGraphe.add_arc(("U01","U10"),"GV")
        self.MyGraphe.add_arc(("U10","U11"),"P")
        self.MyGraphe.add_arc(("U11","U12"),"GN")
       
        """
        Pattern commençant par GN
        """
        #Automate fini commençant par GN CLS CLR GV DET NC
        self.MyGraphe.add_arc(("S00","G01"),"GN")
        self.MyGraphe.add_arc(("G01","G02"),"CLS")
        self.MyGraphe.add_arc(("G02","G03"),"CLR")
        self.MyGraphe.add_arc(("G03","G04"),"GV")
        self.MyGraphe.add_arc(("G04","G05"),"DET")
        self.MyGraphe.add_arc(("G05","G06"),"NC")
        
        """
        Pattern commençant par VIMP
        """
        #Automate fini commençant par VIMP PONCT PRO P GN
        self.MyGraphe.add_arc(("S00","E01"),"VIMP")
        self.MyGraphe.add_arc(("E01","E02"),"PONCT")
        self.MyGraphe.add_arc(("E02","E03"),"PRO")
        self.MyGraphe.add_arc(("E03","E04"),"P")
        self.MyGraphe.add_arc(("E04","E05"),"GN")

        return self.MyGraphe
        
    #########################################################################################
    # PER
    #########################################################################################

    def addPatternsGraphPer(self):
        """
        Pattern commençant par NC
        """
        #Automate fini commençant par NC GN
        self.MyGraphe.add_arc(("S100","A01"),"NC")
        self.MyGraphe.add_arc(("A01","A02"),"GN")

        #Automate fini commençant par NC P NC GN
        self.MyGraphe.add_arc(("A01","A10"),"P")
        self.MyGraphe.add_arc(("A10","A11"),"NC")
        self.MyGraphe.add_arc(("A11","A12"),"GN")

        """
        Pattern commençant par CLS
        """
        #Automate fini commençant par CLS GV DET NC GN
        self.MyGraphe.add_arc(("S100","B00"),"CLS")
        self.MyGraphe.add_arc(("B00","B01"),"GV")
        self.MyGraphe.add_arc(("B01","B02"),"DET")
        self.MyGraphe.add_arc(("B02","B03"),"NC")
        self.MyGraphe.add_arc(("B03","B04"),"GN")

        #Automate fini commençant par CLS GV DET NC P GN
        self.MyGraphe.add_arc(("B03","B90"),"P")
        self.MyGraphe.add_arc(("B90","B91"),"GN")

        #Automate fini commençant par CLS CLR GV DET NC GN
        self.MyGraphe.add_arc(("B00","B10"),"CLR")
        self.MyGraphe.add_arc(("B10","B11"),"GV")
        self.MyGraphe.add_arc(("B11","B12"),"DET")
        self.MyGraphe.add_arc(("B12","B13"),"NC")
        self.MyGraphe.add_arc(("B13","B14"),"GN")

        #Automate fini commençant par CLS CLR GV DET ADJ NC ADJ P NC GN
        self.MyGraphe.add_arc(("B12","B100"),"ADJ")
        self.MyGraphe.add_arc(("B100","B101"),"NC")
        self.MyGraphe.add_arc(("B101","B102"),"ADJ")
        self.MyGraphe.add_arc(("B102","B103"),"P")
        self.MyGraphe.add_arc(("B103","B104"),"NC")
        self.MyGraphe.add_arc(("B104","B105"),"GN")

        #Automate fini commençant par CLS GV NC GN
        self.MyGraphe.add_arc(("B00","B20"),"GV")
        self.MyGraphe.add_arc(("B20","B21"),"NC")
        self.MyGraphe.add_arc(("B21","B22"),"GN")

        #Automate fini commençant par CLS GV  GN
        self.MyGraphe.add_arc(("B00","B30"),"GN")

        #Automate fini commençant par CLS GV P GN
        self.MyGraphe.add_arc(("B00","B40"),"P")
        self.MyGraphe.add_arc(("B40","B41"),"GN")
        
        #Automate fini commençant par CLS GV PROWH GN
        self.MyGraphe.add_arc(("B00","B50"),"PROWH")
        self.MyGraphe.add_arc(("B50","B51"),"GN")

        #Automate fini commençant par CLS CLS CLO GV GN
        self.MyGraphe.add_arc(("B00","B60"),"CLS")
        self.MyGraphe.add_arc(("B60","B61"),"CLO")
        self.MyGraphe.add_arc(("B61","B62"),"GV")
        self.MyGraphe.add_arc(("B62","B63"),"GN")

        #Automate fini commençant par CLS CLR GV GN
        self.MyGraphe.add_arc(("B11","B71"),"GN")

        #Automate fini commençant par CLS CLR GV GN
        self.MyGraphe.add_arc(("B00","B80"),"CLR")
        self.MyGraphe.add_arc(("B80","B81"),"GV")
        self.MyGraphe.add_arc(("B81","B82"),"GN")

        
        
        """
        Pattern commençant par DET
        """
        #Automate fini commençant par DET NC CLS CLR GV GN 
        self.MyGraphe.add_arc(("S100","C00"),"DET")
        self.MyGraphe.add_arc(("C00","C01"),"NC")
        self.MyGraphe.add_arc(("C01","C02"),"CLS")
        self.MyGraphe.add_arc(("C02","C03"),"CLR")
        self.MyGraphe.add_arc(("C03","C04"),"GV")
        self.MyGraphe.add_arc(("C04","C05"),"GN")

        #Automate fini commençant par DET NC P NC P GN
        self.MyGraphe.add_arc(("C01","C12"),"P")
        self.MyGraphe.add_arc(("C12","C13"),"NC")
        self.MyGraphe.add_arc(("C13","C14"),"P")
        self.MyGraphe.add_arc(("C14","C15"),"GN")

        #Automate fini commençant par DET NC ADJ P+D NC GN
        self.MyGraphe.add_arc(("C13","C20"),"ADJ")
        self.MyGraphe.add_arc(("C20","C21"),"P+D")
        self.MyGraphe.add_arc(("C21","C22"),"NC")
        self.MyGraphe.add_arc(("C22","C23"),"GN")
       

        #Automate fini commençant par DET NC ADJ P+D NC NPP GN
        self.MyGraphe.add_arc(("C23","C31"),"P")
        self.MyGraphe.add_arc(("C31","C32"),"GN")

        #Automate fini commençant par DET NC CC GN
        self.MyGraphe.add_arc(("C01","C40"),"CC")
        self.MyGraphe.add_arc(("C40","C41"),"GN")
       

        #Automate fini commençant par DET NC GN
        self.MyGraphe.add_arc(("C01","C30"),"GN")


        """
        Pattern commençant par ADV
        """

        #Automate fini commençant par ADV P GN
        self.MyGraphe.add_arc(("S100","D00"),"ADV")
        self.MyGraphe.add_arc(("D00","D01"),"P")
        self.MyGraphe.add_arc(("D01","D02"),"GN")

        """
        Pattern commençant par PRO
        """
        #Automate fini commençant par PRO CLS CLR GV GN
        self.MyGraphe.add_arc(("S100","F00"),"PRO")
        self.MyGraphe.add_arc(("F00","F01"),"CLS")
        self.MyGraphe.add_arc(("F01","F02"),"CLR")
        self.MyGraphe.add_arc(("F02","F03"),"GV")
        self.MyGraphe.add_arc(("F03","F04"),"GN")

        """
        Pattern commençant par GN
        """
        #Automate fini commençant par GN CLS GV DET NC
        self.MyGraphe.add_arc(("S100","G00"),"GN")
        self.MyGraphe.add_arc(("G00","G01"),"CLS")
        self.MyGraphe.add_arc(("G01","G02"),"GV")
        self.MyGraphe.add_arc(("G02","G03"),"DET")
        self.MyGraphe.add_arc(("G03","G04"),"NC")

        #Automate fini commençant par GN CLS GV NC
        self.MyGraphe.add_arc(("G02","G10"),"NC")
       

        return self.MyGraphe


    #########################################################################################
    # ORG
    #########################################################################################

    def addPatternsGraphOrg(self):

        """
        Pattern commençant par NC
        """
        #Automate fini commençant par NC DET GN
        self.MyGraphe.add_arc(("S200","H00"),"NC")
        self.MyGraphe.add_arc(("H00","H01"),"DET")
        self.MyGraphe.add_arc(("H01","H02"),"GN")
        
        #Automate fini commençant par NC P NC P GN 
        self.MyGraphe.add_arc(("H00","H11"),"P")
        self.MyGraphe.add_arc(("H11","H12"),"NC")
        self.MyGraphe.add_arc(("H12","H13"),"P")
        self.MyGraphe.add_arc(("H13","H14"),"GN")

        #Automate fini commençant par NC P GN 
        self.MyGraphe.add_arc(("H11","H20"),"GN")

        #Automate fini commençant par NC GN 
        self.MyGraphe.add_arc(("H00","H30"),"GN")
        
        
        """
        Pattern commençant par GV
        """
        #Automate fini commençant par GV ADV GN
        self.MyGraphe.add_arc(("S200","J00"),"GV")
        self.MyGraphe.add_arc(("J00","J01"),"ADV")
        self.MyGraphe.add_arc(("J01","J02"),"GN")

        """
        Pattern commençant par DET
        """
        #Automate fini commençant par DET NC P GN
        self.MyGraphe.add_arc(("S200","O00"),"DET")
        self.MyGraphe.add_arc(("O00","O01"),"NC")
        self.MyGraphe.add_arc(("O01","O02"),"P")
        self.MyGraphe.add_arc(("O02","O03"),"GN")

        #Automate fini commençant par DET NC ADJ P+D GN
        self.MyGraphe.add_arc(("O01","O12"),"ADJ")
        self.MyGraphe.add_arc(("O12","O13"),"P+D")
        self.MyGraphe.add_arc(("O13","O14"),"GN")

        #Automate fini commençant par DET NC ADJ P GN
        self.MyGraphe.add_arc(("O12","O23"),"P")
        self.MyGraphe.add_arc(("O23","O24"),"GN")

        """
        Pattern commençant par DET
        """

        #Automate fini commençant par CLS CLR GV GN
        self.MyGraphe.add_arc(("S200","K00"),"CLS")
        self.MyGraphe.add_arc(("K00","K01"),"CLR")
        self.MyGraphe.add_arc(("K01","K02"),"GV")
        self.MyGraphe.add_arc(("K02","K03"),"GN")


        #Automate fini commençant par CLS CLR GV GN
        self.MyGraphe.add_arc(("K00","K10"),"CLR")
        self.MyGraphe.add_arc(("K10","K11"),"GV")
        self.MyGraphe.add_arc(("K11","K12"),"GN")
       
        return self.MyGraphe






       
            
    