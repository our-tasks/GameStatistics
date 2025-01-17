from random import randrange
import copy
import numpy as np
from GameObjects.GameSettings import *
from GameObjects.MainRAMVars import *
from GameObjects.Cards import *
from collections import Counter


class WormCards(Cards):
    """description of class"""

    def __init__(self,vars,wcdeck):
        self.PV = copy.deepcopy(vars)
        self.playedWCName = []    
        self.playedwc = np.array([]).astype(int)
        self.nofRoundspausing = 0
        self.damages = []
        self.GS = GameSettings()        
        self.currentWC = 0
        self.playingdeck = wcdeck
        self.firstdeck = list()
        if len(self.playingdeck)==0:
            cards  = self.GS.WC_Cards
            q    = self.GS.WC_Quantity
            Cards.__init__(self, cardsVaraity = cards, quantities =  q )
            self.playingdeck = self.deck
        self.shuffle()
        return 

    def updateWC(self,vars,pwc):
        
        self.PV = copy.deepcopy(vars)
        self.playingdeck = pwc
        return self

    def ifPossibleToPlay(self,ind):
        a= any(item in ind for item in self.PV.Nullindex)
        if   a==True:
            return False
        return True

    def assignVar(self,var,value):
        if var in self.PV.Nullindex:
            self.PV.Nullindex.remove(var)
        self.PV.varsValue[var]=value
        return
    def shuffle(self):
        shuffle(self.playingdeck)
    
    def selectNextWC(self):
        self.reset()
        wc = self.playingdeck[0]
        self.currentWC = wc
        self.playingdeck = np.delete(self.playingdeck,[0])
        return self.currentWC
    
    def reset(self):
        if (len(self.playingdeck) == 0):
            
            cards  = self.GS.WC_Cards
            q      = self.GS.WC_Quantity
            Cards.__init__(self, cardsVaraity = cards, quantities =  q )
            self.playingdeck = self.deck
            self.shuffle()
        return(self)


    def playFunc(self,s):
        self.updateWC(s.P.playerVars,s.WC.playingdeck)
        self.selectNextWC()
        FuncName = 'WCFunc' + str(self.currentWC)
        getattr(self, FuncName)()
       # print("playfunc")
        #print(self.playedwc)
        #print(self.currentWC)
        self.playedwc = np.append(self.playedwc,self.currentWC)
        #print(self.playedwc)
        s.P.updatePlayer(self.PV,self.nofRoundspausing)
        if (len(self.damages) > 0) and (self.damages[0] not in s.P.PCStatus):
            s.P.PCStatus = s.P.PCStatus+self.damages
        return self

    # list of Cards
    #A=Null
    def WCFunc0(self):
        self.playedWCName.append(' WC Name: A=NULL; ')        
        if 0 not in self.PV.Nullindex:
            self.PV.Nullindex.append(0) 
        return(self)
    
    def WCFunc1(self):
        self.playedWCName.append(' WC Name: B=NULL; ')
        if 1 not in self.PV.Nullindex:
            self.PV.Nullindex.append(1) 
        return(self)
    def WCFunc2(self):
        self.playedWCName.append(' WC Name: C=NULL; ')
        if 2 not in self.PV.Nullindex:    
            self.PV.Nullindex.append(2) 
        return(self)

    def WCFunc3(self):
        self.playedWCName.append(' WC Name: B,C=0; ')
        self.assignVar(1,0)
        self.assignVar(2,0)
        return(self)

    def WCFunc4(self):
        self.playedWCName.append(' WC Name: T -=100 ')
        ind= [3]
        if self.ifPossibleToPlay(ind):
            self.PV.varsValue[3] = self.PV.varsValue[3]-100 
        return(self)

    def WCFunc5(self):
        #print(self)
        self.playedWCName.append(' WC Name: Capture CPU ')
        self.damages.append('CPU1Captured') 
        self.nofRoundspausing = 2
        return(self)
 
    def WCFunc6(self):
        self.playedWCName.append(' WC Name: T =xx00 ') 
        ind= [3]
        if self.ifPossibleToPlay(ind):
            mod = self.PV.varsValue[3] % 100
            self.PV.varsValue[3] = self.PV.varsValue[3]-mod 
        return(self)

    def WCFunc7(self):
        self.playedWCName.append(' WC Name: A=0,B=-1,C=N ')
        self.assignVar(0,0)
        self.assignVar(1,-1)
        if 2 not in self.PV.Nullindex:
            self.PV.Nullindex.append(2)
        return(self)

    def WCFunc8(self):
        self.playedWCName.append(' WC Name: B=-10 ')
        self.assignVar(1,-10)
        return(self)

    def WCFunc9(self):
        self.playedWCName.append(' WC Name: C=-20 ')
        self.assignVar(2,-20) 
        return(self)
    
    def WCFunc10(self):
        self.playedWCName.append(' WC Name: A=0 ')
        self.assignVar(0,0) 
        return(self)
    
    def WCFunc11(self):
        self.playedWCName.append(' WC Name: B=0 ')
        self.assignVar(1,0) 
        return(self)
    
    def WCFunc12(self):
        self.playedWCName.append(' WC12: B -=10 ')
        ind= [1]
        if self.ifPossibleToPlay(ind):
            self.PV.varsValue[1] = self.PV.varsValue[1]-10      
        return(self)
    
    def WCFunc13(self):
        self.playedWCName.append(' WC13: A -=10 ')
        ind= [0]
        if self.ifPossibleToPlay(ind):
            self.PV.varsValue[0] = self.PV.varsValue[0]-10      
        return(self)

    def WCFunc14(self):
        self.playedWCName.append(' WC14: C -=10 ')
        ind= [2]
        if self.ifPossibleToPlay(ind):
            self.PV.varsValue[2] = self.PV.varsValue[2]-10      
        return(self)


    #Bug: when all wcs are played once, and nOfWC is 2, then the game play one WC Card 2 Times instead of playing two WC Card