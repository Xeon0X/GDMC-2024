from gdpc import *
import networks.legacy_roads.list_block
from random import randint


def delete(co1,co2):
    editor = Editor(buffering=  True) 
    x=abs((co2[0])-(co1[0]))
    z=abs((co2[2])-(co1[2]))
    y= abs(co2[1]-co1[1])
    for i in range(y):
            for j in range(z):
                for a in range(x):
                    editor.placeBlock((co1[0]+a,co1[1]+i,co1[2]+j),air)


def mur_sol(co1,co2,block):
    x1=co1[0]
    y1=co1[1]
    z1=co1[2]
    x2=co2[0]
    y2=co2[1]
    z2=co2[2]
    
    
    if  x1<0 or x2<0:
        if  x1<0 and x2>0:
            tailleX=co2[0]-co1[0]
            midtailleX=(tailleX//2)+x1
        elif x1<0 and x2<0:
        
            tailleX=abs(co2[0])-abs(co1[0])
            midtailleX=(tailleX//2)+x1
    else:
        
        tailleX=co2[0]-co1[0]
        midtailleX=(tailleX//2)+x1
        
    if  z1<0 or z2<0:
        if  z1<0 and z2>0:
            tailleZ=co2[2]-co1[2]
            midtailleZ=(tailleZ//2)+z1
        elif z1<0 and z2<0:
        
            tailleZ=abs(co2[2])-abs(co1[2])
            midtailleZ=(tailleZ//2)+z1
    else:
        
        tailleZ=co2[2]-co1[2]
        midtailleZ=(tailleZ//2)+z1
    editor = Editor(buffering=  True) 
    
    if y1==y2:
        
         for i in range(abs(co2[0]-(co1[0]))):
            for j in range((abs((co2[2])-(co1[2])))):
                editor.placeBlock((co1[0]+i,co1[1],co1[2]+j),block)
    elif x1==x2:
        if  z1<0 or z2<0:
            if  z1<0 and z2>=0:
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range((z2-z1)):
               
                        editor.placeBlock((co1[0],co1[1]+i,co1[2]+j),block)
            elif z1<0 and z2<0:
                
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range(abs(z2-z1)):
               
                        editor.placeBlock((co1[0],co1[1]+i,co1[2]+j),block)
        else:
            for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range((abs(co2[2])-abs(co1[2]))):
               
                        editor.placeBlock((co1[0],co1[1]+i,co1[2]+j),block)
            
                
    elif z2==z1:
        if  x1<0 or x2<0:
            if  x1<0 and x2>=0:
                print(abs(abs(co2[1])-abs(co1[1])))
                print(x2-x1)
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range(x2-x1):
            
                        editor.placeBlock((co1[0]+j,co1[1]+i,co1[2]),block)
            elif x1<0 and x2<0:
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range(abs(x2-x1)):
            
                        editor.placeBlock((co1[0]+j,co1[1]+i,co1[2]),block)
        else:
             for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range( (abs(co2[0])-abs(co1[0]))):
            
                        editor.placeBlock((co1[0]+j,co1[1]+i,co1[2]),block)
            
                
                        
    
   
                
    
def poserEscalier(co1,co2,type):
    
    editor = Editor(buffering=  True) 
    x1=co1[0]
    y1=co1[1]
    z1=co1[2]
    x2=co2[0]
    y2=co2[1]
    z2=co2[2]
    
    if x1==x2:
        
        if  z1<0 or z2<0:
            
            if  z1<0 and z2>=0:
               
                    for i in range((z2-z1)):
                        print(1)
                        editor.placeBlock((co1[0],co1[1],co1[2]+i),type)
            elif z1<0 and z2<0:
                
                
                    for i in range(abs(z2-z1)):
               
                        editor.placeBlock((co1[0],co1[1],co1[2]+i),type)
        else:
                    print(z1)
            
                    for i in range((abs(co2[2])-abs(co1[2]))):
                        editor.placeBlock((co1[0],co1[1],co1[2]+i),type)
            
                
    elif z2==z1:
        print(x1)
        if  x1<0 or x2<0:
            if  x1<0 and x2>=0:
                
                
                for i in range(x2-x1):
            
                        editor.placeBlock((co1[0]+i,co1[1],co1[2]),type)
            elif x1<0 and x2<0:
                
                    for i in range(abs(x2-x1)):
            
                        editor.placeBlock((co1[0]+i,co1[1],co1[2]),type)
        else:
           
                    for i in range((abs(co2[0])-abs(co1[0]))):
                        editor.placeBlock((co1[0]+i,co1[1],co1[2]),type)
   
                
def poserPorte(co,type):
    editor = Editor(buffering=  True) 
    editor.placeBlock((co[0],co[1],co[2]),type)
    
    
    
def poserToit(co1,co2,hauteurMax,cotegarage,style,direction):
    x1=co1[0]
    y1=co1[1]
    z1=co1[2]
    x2=co2[0]
    y2=co2[1]
    z2=co2[2]
    
    toit_esca_devant=Block(style['toit_esca'],{"facing": "east"})
    toit_esca_derriere=Block(style['toit_esca'],{"facing": "west"})
    toit_esca_droite=Block(style['toit_esca'],{"facing": "north"})
    toit_esca_gauche=Block(style['toit_esca'],{"facing": "south"})
    toit_esca_devant_ret=Block(style['toit_esca'],{"facing": "east","half":"top"})
    toit_esca_derriere_ret=Block(style['toit_esca'],{"facing": "west","half":"top"})
    toit_esca_droite_ret=Block(style['toit_esca'],{"facing": "north","half":"top"})
    toit_esca_gauch_rete=Block(style['toit_esca'],{"facing": "south","half":"top"})
    toit_planche=Block(style['toit_planche'])
    toit_slab=Block(style['toit_slab'])
    mur=Block(style['mur'])
    
    
    editor = Editor(buffering=  True) 
    if  x1<0 or x2<0:
        if  x1<0 and x2>=0:
            tailleX=x2-x1
            midtailleX=(tailleX//2)+x1
        elif x1<0 and x2<0:
        
            tailleX=abs(co2[0]-co1[0])
            midtailleX=(tailleX//2)+x1
    else:
        
        tailleX=co2[0]-co1[0]
        midtailleX=(tailleX//2)+x1
        
    if  z1<0 or z2<0:
        if  z1<0 and z2>=0:
            tailleZ=co2[2]-co1[2]
            midtailleZ=(tailleZ//2)+z1
        elif z1<0 and z2<0:
        
            tailleZ=abs(co2[2]-co1[2])
            midtailleZ=(tailleZ//2)+z1
    else:
        
        tailleZ=co2[2]-co1[2]
        midtailleZ=(tailleZ//2)+z1
        
        
    if direction=='west':
        if cotegarage=='left':
            if x1==0 and z1==0:
                for i in range(3):
                    if i==2:
                        mur_sol((x1-1,y1+4+i,z1+i),(x2-i,y1+4+i,midtailleZ-i),toit_planche)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2+1),toit_planche)
                        mur_sol((x1-1,y1+5+i,z1+i),(x2-i,y1+5+i,midtailleZ-i),toit_slab)
                        mur_sol((midtailleX+i,y1+5+i,midtailleZ-i),(x2-i,y1+5+i,z2+1),toit_slab)
                        
                    else:
                        mur_sol((x1,y1+4+i,z1+i),(x2-i,y1+4+i,midtailleZ-i),mur)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2),mur)
                        
                    poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+3-i,y1+4+i,z1-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+2+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ+1-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ-i-1),toit_esca_gauch_rete)
                    editor.placeBlock((x2-1-i,y1+4+i,z2),toit_esca_devant_ret)
                    editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
            elif x1==0:
                for i in range(3):
                    if i==2:
                        mur_sol((x1-1,y1+4+i,z1+i),(x2+2-i,y1+4+i,midtailleZ-i),toit_planche)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2+1),toit_planche)
                        mur_sol((x1-1,y1+5+i,z1+i),(x2+2-i,y1+5+i,midtailleZ-i),toit_slab)
                        mur_sol((midtailleX+i,y1+5+i,midtailleZ-i),(x2-i,y1+5+i,z2+1),toit_slab)
                        
                    else:
                        mur_sol((x1,y1+4+i,z1+i),(x2-i,y1+4+i,midtailleZ-i),mur)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2),mur)
                        
                    poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+3-i,y1+4+i,z1-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+2+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ+1-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ-i-1),toit_esca_gauch_rete)
                    editor.placeBlock((x2-1-i,y1+4+i,z2),toit_esca_devant_ret)
                    editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
                    
            elif  z1==0:
                for i in range(3):
                    if i==2:
                        mur_sol((x1-1,y1+4+i,z1+i),(x2-i,y1+4+i,midtailleZ-i),toit_planche)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2+1),toit_planche)
                        mur_sol((x1-1,y1+5+i,z1+i),(x2-i,y1+5+i,midtailleZ-i),toit_slab)
                        mur_sol((midtailleX+i,y1+5+i,midtailleZ-i),(x2-i,y1+5+i,z2+1),toit_slab)
                        
                    else:
                        mur_sol((x1,y1+4+i,z1+i),(x2-i,y1+4+i,midtailleZ-i),mur)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2),mur)
                        
                    poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+1-i,y1+4+i,z1-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ+1-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ-i-1),toit_esca_gauch_rete)
                    editor.placeBlock((x2-1-i,y1+4+i,z2),toit_esca_devant_ret)
                    editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
                
            
            
            
            else:
                for i in range(3):
                    if i==2:
                        mur_sol((x1-1,y1+4+i,z1+i),(x2-i,y1+4+i,midtailleZ-i),toit_planche)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2+1),toit_planche)
                        mur_sol((x1-1,y1+5+i,z1+i),(x2-i,y1+5+i,midtailleZ-i),toit_slab)
                        mur_sol((midtailleX+i,y1+5+i,midtailleZ-i),(x2-i,y1+5+i,z2+1),toit_slab)
                        
                    else:
                        mur_sol((x1,y1+4+i,z1+i),(x2-i,y1+4+i,midtailleZ-i),mur)
                        mur_sol((midtailleX+i,y1+4+i,midtailleZ-i),(x2-i,y1+4+i,z2),mur)
                        
                        
                    poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+1-i,y1+4+i,z1-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ+1-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ-i-1),toit_esca_gauch_rete)
                    editor.placeBlock((x2-1-i,y1+4+i,z2),toit_esca_devant_ret)
                    editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
                
    
        elif cotegarage=='right':
            if x1==0 and z1==0:
            
                for i in range(3):
                    if i==2:
                        
                        
                        mur_sol((midtailleX+i,y1+4+i,z1-1),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((x1-1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((midtailleX+i,y1+5+i,z1-1),(x2-i,y1+5+i,z2-i),toit_slab)
                        mur_sol((x1-1,y1+5+i,midtailleZ+i),(x2-i,y1+5+i,z2-i),toit_slab)
                        
                    else:
                        mur_sol((midtailleX+i,y1+4+i,z1),(x2-i,y1+4+i,z2-i),mur)
                        mur_sol((x1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),mur)
                    
                    poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+2+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2+3-i),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,z2-i),(x2-i+2,y1+4-i,z2-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,z1-1),(midtailleX-1+i,y1+4+i,midtailleZ+1+i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                    editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    pass
            elif x1==0:
                for i in range(3):
                    if i==2:
                    
                        
                        mur_sol((midtailleX+i,y1+4+i,z1-1),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((x1-1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((midtailleX+i,y1+5+i,z1-1),(x2-i,y1+5+i,z2-i),toit_slab)
                        mur_sol((x1-1,y1+5+i,midtailleZ+i),(x2-i,y1+5+i,z2-i),toit_slab)
                        
                    else:
                        mur_sol((midtailleX+i,y1+4+i,z1),(x2-i,y1+4+i,z2-i),mur)
                        mur_sol((x1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),mur)
                    
                    poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+2+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2+1-i),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,z2-i),(x2-i+2,y1+4-i,z2-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,z1-1),(midtailleX-1+i,y1+4+i,midtailleZ+i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                    editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    pass
                
            elif z1==0:
                
                for i in range(3):
                    if i==2:
                    
                        
                        mur_sol((midtailleX+i,y1+4+i,z1-1),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((x1-1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((midtailleX+i,y1+5+i,z1-1),(x2-i,y1+5+i,z2-i+1),toit_slab)
                        mur_sol((x1-1,y1+5+i,midtailleZ+i),(x2-i,y1+5+i,z2-i),toit_slab)
                        
                    else:
                        mur_sol((midtailleX+i,y1+4+i,z1),(x2-i,y1+4+i,z2-i),mur)
                        mur_sol((x1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),mur)
                    
                    poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2+2-i),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,z2-i),(x2-i+1,y1+4-i,z2-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,z1-1),(midtailleX-1+i,y1+4+i,midtailleZ+1+i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                    editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    
            else:
                
                for i in range(3):
                    if i==2:
                    
                        
                        mur_sol((midtailleX+i,y1+4+i,z1-1),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((x1-1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),toit_planche)
                        mur_sol((midtailleX+i,y1+5+i,z1-1),(x2-i,y1+5+i,z2-i),toit_slab)
                        mur_sol((x1-1,y1+5+i,midtailleZ+i),(x2-i,y1+5+i,z2-i),toit_slab)
                        
                    else:
                        mur_sol((midtailleX+i,y1+4+i,z1),(x2-i,y1+4+i,z2-i),mur)
                        mur_sol((x1,y1+4+i,midtailleZ+i),(x2-i,y1+4+i,z2-i),mur)
                        
                        
                    poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2-i),toit_esca_derriere)
                    poserEscalier((x1-1,y1+4+i,z2-i),(x2-i+1,y1+4-i,z2-i),toit_esca_droite)
                    poserEscalier((midtailleX-1+i,y1+4+i,z1-1),(midtailleX-1+i,y1+4+i,midtailleZ+i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                    editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    pass
                
                
                
                
                
                
                
                
                
    elif direction=='east':
        
         
        if cotegarage=='left':
            if x1==0 and z1==0:
                for i in range(3):
                    if i==2:
                        i=1
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                        mur_sol((x1+1+i,y1+5+i,z1-1),(midtailleX-i,y1+5+i,midtailleZ+2),toit_planche)
                        mur_sol((x1+1+i,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                        mur_sol((x1+1+i,y1+6+i,z1-1),(midtailleX-i,y1+6+i,midtailleZ+2),toit_slab)
                        i=2
                        
                    else:
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2,y1+5+i,z2-1-i),mur)
                        mur_sol((x1+1+i,y1+5+i,z1),(midtailleX-i,y1+5+i,midtailleZ+2),mur)
                        
                    poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((midtailleX+1-i,y1+4+i,z1-1),(midtailleX+1-i,y1+4+i,midtailleZ+i+1),toit_esca_derriere)
                    poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                    poserEscalier((x1-1+i,y1+4+i,z1-1),(x1-1+i,y1+4+i,z2+3-i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    pass
                    editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    editor.placeBlock((midtailleX-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                    
                    
                    
            elif x1==0:
                for i in range(3):
                    if i==2:
                        i=1
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                        mur_sol((x1+1+i,y1+5+i,z1-1),(midtailleX-i,y1+5+i,midtailleZ+2),toit_planche)
                        mur_sol((x1+1+i,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                        mur_sol((x1+1+i,y1+6+i,z1-1),(midtailleX-i,y1+6+i,midtailleZ+2),toit_slab)
                        i=2
                        
                    else:
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2,y1+5+i,z2-1-i),mur)
                        mur_sol((x1+1+i,y1+5+i,z1),(midtailleX-i,y1+5+i,midtailleZ+2),mur)
                        
                    poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((midtailleX+1-i,y1+4+i,z1-1),(midtailleX+1-i,y1+4+i,midtailleZ+i),toit_esca_derriere)
                    poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                    poserEscalier((x1-1+i,y1+4+i,z1-1),(x1-1+i,y1+4+i,z2+1-i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    pass
                    editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    editor.placeBlock((midtailleX-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                    
                    
                    
            elif  z1==0:
                for i in range(3):
                    if i==2:
                        i=1
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                        mur_sol((x1+1+i,y1+5+i,z1-1),(midtailleX-i,y1+5+i,midtailleZ+2),toit_planche)
                        mur_sol((x1+1+i,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                        mur_sol((x1+1+i,y1+6+i,z1-1),(midtailleX-i,y1+6+i,midtailleZ+2),toit_slab)
                        i=2
                        
                    else:
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2,y1+5+i,z2-1-i),mur)
                        mur_sol((x1+1+i,y1+5+i,z1),(midtailleX-i,y1+5+i,midtailleZ+2),mur)
                        
                    poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((midtailleX+1-i,y1+4+i,z1-1),(midtailleX+1-i,y1+4+i,midtailleZ+i+1),toit_esca_derriere)
                    poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                    poserEscalier((x1-1+i,y1+4+i,z1-1),(x1-1+i,y1+4+i,z2+3-i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    pass
                    editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    editor.placeBlock((midtailleX-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                
            
            
            
            else:
                for i in range(3):
                    if i==2:
                        i=1
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                        mur_sol((x1+1+i,y1+5+i,z1-1),(midtailleX-i,y1+5+i,midtailleZ+2),toit_planche)
                        mur_sol((x1+1+i,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                        mur_sol((x1+1+i,y1+6+i,z1-1),(midtailleX-i,y1+6+i,midtailleZ+2),toit_slab)
                        i=2
                        
                    else:
                        mur_sol((x1+1+i,y1+5+i,midtailleZ+1+i),(x2,y1+5+i,z2-1-i),mur)
                        mur_sol((x1+1+i,y1+5+i,z1),(midtailleX-i,y1+5+i,midtailleZ+2),mur)
                        
                    poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                    poserEscalier((midtailleX+1-i,y1+4+i,z1-1),(midtailleX+1-i,y1+4+i,midtailleZ+i),toit_esca_derriere)
                    poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                    poserEscalier((x1-1+i,y1+4+i,z1-1),(x1-1+i,y1+4+i,z2+1-i),toit_esca_devant)
                    if hauteurMax==5+i:
                        break
                for i in range(2):
                    pass
                    editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                    editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                    editor.placeBlock((midtailleX-i,y1+4+i,z1-1),toit_esca_devant_ret)
                    editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                

        elif cotegarage=='right':
                if x1==0 and z1==0:
                        for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ-2),(midtailleX-i,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+2,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ-2),(midtailleX-i,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ),(midtailleX-i,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-i),(midtailleX+1-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX+2-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1-1+i,y1+4+i,z1+i),(x1-1+i,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((midtailleX-i,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                        
                    
                    
                elif x1==0:
                   for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ-2),(midtailleX-i,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+2,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ-2),(midtailleX-i,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ),(midtailleX-i,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-i),(midtailleX+1-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX+2-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1-1+i,y1+4+i,z1+i),(x1-1+i,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((midtailleX-i,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                        
                        
                elif  z1==0:
                   for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ-2),(midtailleX-i,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+2,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ-2),(midtailleX-i,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ),(midtailleX-i,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-i),(midtailleX+1-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX+2-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1-1+i,y1+4+i,z1+i),(x1-1+i,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((midtailleX-i,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                
            
            
            
                else:
                    for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ-2),(midtailleX-i,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+2,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ-2),(midtailleX-i,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                mur_sol((x1+2,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,midtailleZ),(midtailleX-i,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX+1-i,y1+4+i,midtailleZ-i),(midtailleX+1-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX+2-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1-1+i,y1+4+i,z1+i),(x1-1+i,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((midtailleX-i,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                
            
    
    elif direction=='north':
        
         
        if cotegarage=='left':
            if x1==0 and z1==0:
                        for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,midtailleZ+i+1),(x2-1-i,y1+5+i,z2-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1-1),(x2-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1-1,y1+6+i,midtailleZ+i+1),(x2-1-i,y1+6+i,z2-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1-1),(x2-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,midtailleZ+i+1),(x2-i,y1+5+i,z2-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1),(x2-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+1+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2+3-i),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,z2-i),(x2+3-i,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((midtailleX+i-1,y1+4+i,z1-1),(midtailleX+i-1,y1+4+i,midtailleZ+2+i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                        
                    
                    
            elif x1==0:
                  for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,midtailleZ+i+1),(x2-1-i,y1+5+i,z2-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1-1),(x2-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1-1,y1+6+i,midtailleZ+i+1),(x2-1-i,y1+6+i,z2-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1-1),(x2-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,midtailleZ+i+1),(x2-i,y1+5+i,z2-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1),(x2-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+1+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2-i),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,z2-i),(x2+3-i,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((midtailleX+i-1,y1+4+i,z1-1),(midtailleX+i-1,y1+4+i,midtailleZ+i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
            elif  z1==0:
                   for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,midtailleZ+i+1),(x2-1-i,y1+5+i,z2-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1-1),(x2-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1-1,y1+6+i,midtailleZ+i+1),(x2-1-i,y1+6+i,z2-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1-1),(x2-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,midtailleZ+i+1),(x2-i,y1+5+i,z2-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1),(x2-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+1+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2+3-i),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,z2-i),(x2-i,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((midtailleX+i-1,y1+4+i,z1-1),(midtailleX+i-1,y1+4+i,midtailleZ+2+i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                
            
            
            
            else:
                    for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,midtailleZ+i+1),(x2-1-i,y1+5+i,z2-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1-1),(x2-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1-1,y1+6+i,midtailleZ+i+1),(x2-1-i,y1+6+i,z2-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1-1),(x2-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,midtailleZ+i+1),(x2-i,y1+5+i,z2-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1),(x2-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((x1-1,y1+4+i,midtailleZ-1+i),(midtailleX+1+i,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1-1),(x2-i,y1+4+i,z2+1-i),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,z2-i),(x2-i,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((midtailleX+i-1,y1+4+i,z1-1),(midtailleX+i-1,y1+4+i,midtailleZ+i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((x2-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x1-1,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                

        elif cotegarage=='right':
                if x1==0 and z1==0:
                        for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+i+1,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1-1),(midtailleX-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1-1),(midtailleX-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+i,y1+5+i,midtailleZ+i+1),(x2,y1+5+i,z2-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1),(midtailleX-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,z1-1),(midtailleX-i,y1+4+i,midtailleZ+1+i),toit_esca_derriere)
                            poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1-1),(x1+i-1,y1+4+i,z2+3-i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((midtailleX-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                        
                    
                    
                elif x1==0:
                  for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+i+1,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1-1),(midtailleX-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1-1),(midtailleX-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+i,y1+5+i,midtailleZ+i+1),(x2,y1+5+i,z2-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1),(midtailleX-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,z1-1),(midtailleX-i,y1+4+i,midtailleZ+i),toit_esca_derriere)
                            poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1-1),(x1+i-1,y1+4+i,z2+1-i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((midtailleX-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                        
                        
                elif  z1==0:
                   for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+i+1,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1-1),(midtailleX-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1-1),(midtailleX-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+i,y1+5+i,midtailleZ+i+1),(x2,y1+5+i,z2-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1),(midtailleX-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,z1-1),(midtailleX-i,y1+4+i,midtailleZ+1+i),toit_esca_derriere)
                            poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1-1),(x1+i-1,y1+4+i,z2+3-i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((midtailleX-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                
            
            
            
                else:
                    for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+i+1,y1+5+i,midtailleZ+1+i),(x2+1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1-1),(midtailleX-i-1,y1+5+i,z2-1-i),toit_planche)
                                mur_sol((x1+i+1,y1+6+i,midtailleZ+1+i),(x2+1,y1+6+i,z2-1-i),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1-1),(midtailleX-i-1,y1+6+i,z2-1-i),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+i,y1+5+i,midtailleZ+i+1),(x2,y1+5+i,z2-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1),(midtailleX-i-1,y1+5+i,z2-i),mur)
                                
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-1+i),(x2+1,y1+4+i,midtailleZ-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,z1-1),(midtailleX-i,y1+4+i,midtailleZ+i),toit_esca_derriere)
                            poserEscalier((x1+i,y1+4+i,z2-i),(x2+1,y1+4+i,z2-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1-1),(x1+i-1,y1+4+i,z2+1-i),toit_esca_devant)
                         
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x1+i,y1+4+i,z1-1),toit_esca_derriere_ret)
                                editor.placeBlock((midtailleX-1-i,y1+4+i,z1-1),toit_esca_devant_ret)
                                editor.placeBlock((x2,y1+4+i,z2-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,midtailleZ+i),toit_esca_droite_ret)
                
                    
    elif direction=='south':
        
         
        if cotegarage=='left':
            if x1==0 and z1==0:
                        for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+1+i,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1+1+i),(midtailleX-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(midtailleX-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1+i),(x1+i-1,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
                        
                    
                    
            elif x1==0:
                  for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+1+i,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1+1+i),(midtailleX-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(midtailleX-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1+i),(x1+i-1,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
            elif  z1==0:
                   for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+1+i,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1+1+i),(midtailleX-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(midtailleX-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1+i),(x1+i-1,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
                
            
            
            
            else:
                    for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2+1,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1+1+i,y1+6+i,z1+i+1),(x2+1,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((x1+i+1,y1+6+i,z1+1+i),(midtailleX-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1+1+i,y1+5+i,z1+i+1),(x2,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((x1+i+1,y1+5+i,z1+1+i),(midtailleX-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1+i,y1+4+i,z1-1+i),(x2+1,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(midtailleX-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((midtailleX-i,y1+4+i,midtailleZ-i),(x2+1,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((x1+i-1,y1+4+i,z1+i),(x1+i-1,y1+4+i,z2+1),toit_esca_devant)
                            editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((midtailleX-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((x1+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x2,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x2,y1+4+i,z1+i),toit_esca_droite_ret)
                

        elif cotegarage=='right':
                if x1==0 and z1==0:
                        for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1-1,y1+6+i,z1+i+1),(x2-1-i,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1+1+i),(x2-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+3-i,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+1+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                            #editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                        
                    
                    
                elif x1==0:
                  for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1-1,y1+6+i,z1+i+1),(x2-1-i,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1+1+i),(x2-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+3-i,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+1+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                            #editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                elif  z1==0:
                   for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1-1,y1+6+i,z1+i+1),(x2-1-i,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1+1+i),(x2-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+1-i,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+1+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                            #editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                
            
            
            
                else:
                    for i in range(3):
                            if i==2:
                                i=1
                                mur_sol((x1-1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),toit_planche)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2+1),toit_planche)
                                mur_sol((x1-1,y1+6+i,z1+i+1),(x2-1-i,y1+6+i,midtailleZ-i-1),toit_slab)
                                mur_sol((midtailleX+i+1,y1+6+i,z1+1+i),(x2-i-1,y1+6+i,z2+1),toit_slab)
                                i=2
                                
                            else:
                                pass
                                mur_sol((x1,y1+5+i,z1+i+1),(x2-1-i,y1+5+i,midtailleZ-i-1),mur)
                                mur_sol((midtailleX+i+1,y1+5+i,z1+1+i),(x2-i-1,y1+5+i,z2),mur)
                                
                            poserEscalier((x1-1,y1+4+i,z1-1+i),(x2+1-i,y1+4+i,z1-1+i),toit_esca_gauche)
                            poserEscalier((x2-i,y1+4+i,z1+i),(x2-i,y1+4+i,z2+1),toit_esca_derriere)
                            poserEscalier((x1-1,y1+4+i,midtailleZ-i),(midtailleX+1+i,y1+4+i,midtailleZ-i),toit_esca_droite)
                            poserEscalier((midtailleX-1+i,y1+4+i,midtailleZ-i),(midtailleX-1+i,y1+4+i,z2+1),toit_esca_devant)
                            #editor.placeBlock((x1-1+i,y1+4+i,z1-1+i),toit_esca_devant)
                            if hauteurMax==5+i:
                                break
                            for i in range(2):
                                pass
                                editor.placeBlock((x2-i-1,y1+4+i,z2),toit_esca_devant_ret)
                                editor.placeBlock((midtailleX+i,y1+4+i,z2),toit_esca_derriere_ret)
                                editor.placeBlock((x1-1,y1+4+i,midtailleZ-1-i),toit_esca_gauch_rete)
                                editor.placeBlock((x1-1,y1+4+i,z1+i),toit_esca_droite_ret)
                
def poserFenetre(co1,co2,type):
    editor = Editor(buffering=  True) 
    
    x=abs((co2[0])-(co1[0]))
    z=abs((co2[2])-(co1[2]))
    y= abs(co2[1]-co1[1])
  
    if co1[0]==co2[0]:
        if z%2==0:
            if z==4:
                  
                    editor.placeBlock((co1[0],co1[1]+1,co1[2]+1),type)
                    editor.placeBlock((co1[0],co1[1]+1,co1[2]+2),type)
            else:
                
                for i in range(z//2):
                    if i%2==0:
                        editor.placeBlock((co1[0],co1[1]+1,co1[2]+i*2),type)
                        editor.placeBlock((co1[0],co1[1]+1,co1[2]+i*2+1),type)
        else:
            if z<=5:
                for i in range(z):
                    
                        
                        editor.placeBlock((co1[0],co1[1]+1,co1[2]+i),type)
            else:
                
                for i in range((z//3)):
                        if 3*(i+1)+(i)>abs(co2[2]-co1[2]):
                            break
                        else:
                            editor.placeBlock((co1[0],co1[1]+1,co1[2]+i*4),type)
                            editor.placeBlock((co1[0],co1[1]+1,co1[2]+i*4+1),type)
                            editor.placeBlock((co1[0],co1[1]+1,co1[2]+i*4+2),type)
                        
                    
                
            
    if co1[2]==co2[2]:
        
        if x%2==0:
            if x==4:
                  
                    editor.placeBlock((co1[0]+1,co1[1]+1,co1[2]),type)
                    editor.placeBlock((co1[0]+2,co1[1]+1,co1[2]),type)
            else:
                for i in range(x//2):
                    if i%2==0:
                        editor.placeBlock((co1[0]+i*2,co1[1]+1,co1[2]),type)
                        editor.placeBlock((co1[0]+i*2+1,co1[1]+1,co1[2]),type)
        else:
            if x<=5:
                
                 
                for i in range(x):
                        
                            
                            editor.placeBlock((co1[0]+i,co1[1]+1,co1[2]),type)
            else:
                
                for i in range((x//3)):
                        if 3*(i+1)+i>abs(co2[0]-co1[0]):
                            break
                        else:
                            editor.placeBlock((co1[0]+i*4,co1[1]+1,co1[2]),type)
                            editor.placeBlock((co1[0]+i*4+1,co1[1]+1,co1[2]),type)
                            editor.placeBlock((co1[0]+i*4+2,co1[1]+1,co1[2]),type)
            
                    
                    
                    
                    
            

def poserGarage(co1,co2):
    
    x1=co1[0]
    y1=co1[1]
    z1=co1[2]
    x2=co2[0]
    y2=co2[1]
    z2=co2[2]
    editor = Editor(buffering=  True) 
    if  x1<0 or x2<0:
        if  x1<0 and x2>=0:
            x=x2-x1
            
        elif x1<0 and x2<0:
            
            x=abs(co2[0]-co1[0])
            
    else:
        
        x=co2[0]-co1[0]
        
    if  z1<0 or z2<0:
        if  z1<0 and z2>=0:
            z=co2[2]-co1[2]
            
        elif z1<0 and z2<0:
        
            z=abs(co2[2]-co1[2])
            
    else:
        
        z=co2[2]-co1[2]
        
        
    
       
       
    
    if x1==x2:
        if  z1<0 or z2<0:
            if  z1<0 and z2>=0:
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range((z2-z1)):
               
                        editor.placeBlock((co1[0],co1[1]+i,co1[2]+j),block_quartz)
            elif z1<0 and z2<0:
                
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range(abs(z2-z1)):
               
                        editor.placeBlock((co1[0],co1[1]+i,co1[2]+j),block_quartz)
        else:
            for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range((abs(co2[2])-abs(co1[2]))):
               
                        editor.placeBlock((co1[0],co1[1]+i,co1[2]+j),block_quartz)
            
                
    elif z2==z1:
        if  x1<0 or x2<0:
            if  x1<0 and x2>=0:
                print(abs(abs(co2[1])-abs(co1[1])))
                print(x2-x1)
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range(x2-x1):
            
                        editor.placeBlock((co1[0]+j,co1[1]+i,co1[2]),block_quartz)
            elif x1<0 and x2<0:
                for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range(abs(x2-x1)):
            
                        editor.placeBlock((co1[0]+j,co1[1]+i,co1[2]),block_quartz)
        else:
             for i in range(abs(abs(co2[1])-abs(co1[1]))):
                    for j in range( (abs(co2[0])-abs(co1[0]))):
            
                        editor.placeBlock((co1[0]+j,co1[1]+i,co1[2]),block_quartz) 
       
       
       
         
  
    
    
    if co1[0]==co2[0]:
        
        if z%3==0:
            for i in range(z//3):
                    editor.placeBlock((co1[0],co2[1],co1[2]+i*3),stairs_quartz_droite)
                    editor.placeBlock((co1[0],co2[1],co1[2]+1+i*3),quartz_slab_up)
                    editor.placeBlock((co1[0],co2[1],co1[2]+2+i*3),stairs_quartz_gauche)
        elif z%2==0:
            for i in range(z):
                if i%2==0:
                    editor.placeBlock((co1[0],co2[1],co1[2]+i),stairs_quartz_droite)
                else:
                    editor.placeBlock((co1[0],co2[1],co1[2]+i),stairs_quartz_gauche)
        if  z%5==0:
            for i in range((z//5)):
                    
                    editor.placeBlock((co1[0],co2[1],co1[2]+i*5),stairs_quartz_droite)
                    editor.placeBlock((co1[0],co2[1],co1[2]+1+i*5),stairs_quartz_gauche)
                    editor.placeBlock((co1[0],co2[1],co1[2]+2+i*5),block_quartz)
                    editor.placeBlock((co1[0],co2[1],co1[2]+3+i*5),stairs_quartz_droite)
                    editor.placeBlock((co1[0],co2[1],co1[2]+4+i*5),stairs_quartz_gauche)
                
    elif co1[2]==co2[2]:
        
        if x%3==0:
            
            for i in range(x//3):
                    editor.placeBlock((co1[0]+i*3,co2[1],co1[2]),stairs_quartz_derriere)
                    editor.placeBlock((co1[0]+1+i*3,co2[1],co1[2]),quartz_slab_up)
                    editor.placeBlock((co1[0]+2+i*3,co2[1],co1[2]),stairs_quartz_devant)
        elif x%2==0:
            for i in range(x):
                if i%2==0:
                    editor.placeBlock((co1[0]+i,co2[1],co1[2]),stairs_quartz_derriere)
                else:
                    editor.placeBlock((co1[0]+i,co2[1],co1[2]),stairs_quartz_devant)
        elif  x%5==0:
            for i in range((x//5)):
                    
                    editor.placeBlock((co1[0]+i*5,co2[1],co1[2]),stairs_quartz_derriere)
                    editor.placeBlock((co1[0]+1+i*5,co2[1],co1[2]),stairs_quartz_devant)
                    editor.placeBlock((co1[0]+2+i*5,co2[1],co1[2]),block_quartz)
                    editor.placeBlock((co1[0]+3+i*5,co2[1],co1[2]),stairs_quartz_derriere)
                    editor.placeBlock((co1[0]+4+i*5,co2[1],co1[2]),stairs_quartz_devant)
        
            

                    
                
            

def house(co1,co2,cotegarage,hauteurMax,nb_style,direction):# ,etage):
    """
    Minimun 10*10 
    """
    
    if nb_style==0:
        style=style_basique
    elif nb_style==1:
        style=style_birch
    elif nb_style==2:
        style=style_end
    else:
        style=style_jungle
    
    
    sol=Block(style['sol'])
    mur=Block(style['mur'])
    grass=Block(style['grass'])
    chemin=Block(style['chemin'])
    fence=Block(style['fence'])
    
    glass=Block(style['glass'])
    
    
    
    
    
    
    
    
    tailleX=abs(co2[0])-abs(co1[0])
    
    hauteurMin=min(co2[1],co1[1])
    tailleZ=abs(co2[2])-abs(co1[2])
    
    editor = Editor(buffering=  True) 
    
    
    
    x1=co1[0]
    y1=co1[1]
    z1=co1[2]
    x2=co2[0]
    y2=co2[1]
    z2=co2[2]
    
    if  x1<0 or x2<0:
        if  x1<0 and x2>=0:
            tailleX=x2-x1
            midtailleX=(tailleX//2)+x1
        elif x1<0 and x2<0:
            print(abs(co2[0]-co1[0]),(tailleX//2)+x1)
            tailleX=abs(co2[0]-co1[0])
            midtailleX=(tailleX//2)+x1
    else:
        
        tailleX=co2[0]-co1[0]
        midtailleX=(tailleX//2)+x1
        
    if  z1<0 or z2<0:
        if  z1<0 and z2>=0:
            tailleZ=co2[2]-co1[2]
            midtailleZ=(tailleZ//2)+z1
        elif z1<0 and z2<0:
        
            tailleZ=abs(co2[2]-co1[2])
            midtailleZ=(tailleZ//2)+z1
    else:
        
        tailleZ=co2[2]-co1[2]
        midtailleZ=(tailleZ//2)+z1
        
    
    
    
    
    if direction=='west':
        door=Block(style['door'],{"facing": "east"})
        if cotegarage=='right':
            
                                    
                                    
                                
            #murs
            poserGarage((x1+1,y1+1,midtailleZ+1),(x1+1,y1+3,z2-1))
            mur_sol((x1,y1+1,z2-1),(x2,y1+5,z2-1),mur)
            mur_sol((x1,y1+1,midtailleZ),(x1,y1+5,z2   ),mur)
            mur_sol((x2-1,y1+1,z1),(x2-1,y1+5,z2),mur)
            mur_sol((x1,y1+1,midtailleZ),(midtailleX+1,y1+5,midtailleZ),mur)
            mur_sol((midtailleX,y1+1,z1),(x2,y1+5,z1),mur)
            mur_sol((midtailleX,y1+1,z1),(midtailleX,y1+5,midtailleZ),mur)
            
            
            mur_sol((x1,y1+1,midtailleZ+1),(x1,y1+4,z2-1   ),air)
            
            #sols/plafonds
            mur_sol((midtailleX,y1+4,z1),(x2,y1+4,z2),mur)
            mur_sol((midtailleX,y1,z1),(x2,y1,z2),sol)
            mur_sol((x1,y1+4,midtailleZ),(midtailleX,y1+4,z2),mur)
            mur_sol((x1,y1,midtailleZ),(midtailleX,y1,z2),sol)
            mur_sol((x1,y1,z1),(midtailleX,y1,midtailleZ),grass)
            
        
            
            poserFenetre((midtailleX,y1+1,z1+1),(midtailleX,y1+5,midtailleZ-1),glass)
            poserFenetre((midtailleX+1,y1+1,z1),(x2-1,y1+5,z1),glass)
            poserFenetre((x1+2,y1+1,midtailleZ),(midtailleX-1,y1+5,midtailleZ),glass)
            poserFenetre((x2-1,y1+1,z1+1),(x2-1,y1+5,z2-1),glass)
            poserFenetre((x1+2,y1+1,z2-1),(x2-1,y1+4,z2-1),glass)
            
            if  ((z2-z1)//2)%2==0:
                 
                    poserPorte((x1+tailleX//2,hauteurMin+1,z1+(tailleZ//4)),door)
                    poserPorte((x1+tailleX//2,hauteurMin+1,z1+(tailleZ//4)-1),door)
                    mur_sol((x1,y1,z1+(tailleZ//4)-1),(x1+tailleX//2,y1,z1+(tailleZ//4)+1),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if(z1+j != z1+(tailleZ//4) and z1+j != z1+(tailleZ//4)-1 ) and (x1+i< x1+(tailleX//2) and z1+j<z1+(tailleZ//2)) and(x1+i==x1 or z1+j==z1) and (z1+j != z1+(tailleZ//4) or z1+j != z1+(tailleZ//4)-1) :
                            
                                editor.placeBlock((x1+i,y1+1,z1+j),fence)
                    
            else:
                
                    poserPorte((x1+tailleX//2,hauteurMin+1,z1+(tailleX//4)),door)
                    mur_sol((x1,y1,z1+(tailleZ//4)),(x1+tailleX//2,y1,z1+(tailleZ//4)+1),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if (x1+i< x1+(tailleX//2) and z1+j<z1+(tailleZ//2)) and(x1+i==x1 or z1+j==z1) and z1+j != z1+(tailleZ//4):
                                
                                editor.placeBlock((x1+i,y1+1,z1+j),fence)
                    
                    
            poserToit(co1,co2,hauteurMax,cotegarage,style,direction)    
            
        
        
        
        elif cotegarage=='left':
                
            
                                
                        
                                    
                    
                
                
                            
                        
                                    
            
            
            #murs
            poserGarage((x1+1,y1+1,z1+1),(x1+1,y1+3,midtailleZ-1))
            mur_sol((x1,y1+1,z1),(x2,y1+5,z1),mur)
            mur_sol((x1,y1+1,z1),(x1,y1+5,midtailleZ   ),mur)
            mur_sol((x2-1,y1+1,z1),(x2-1,y1+5,z2),mur)
            mur_sol((x1,y1+1,midtailleZ-1),(midtailleX+1,y1+5,midtailleZ-1),mur)
            mur_sol((midtailleX,y1+1,midtailleZ),(midtailleX,y1+5,z2),mur)
            mur_sol((midtailleX,y1+1,z2-1),(x2,y1+5,z2-1),mur)
            
            
            mur_sol((x1,y1+1,z1+1),(x1,y1+4,midtailleZ-1),air)
            
            #sols/plafonds
            mur_sol((x1,y1+4,z1),(x2,y1+4,midtailleZ),mur)
            mur_sol((x1,y1,z1),(x2,y1,midtailleZ),oak_planks)
            mur_sol((midtailleX,y1+4,midtailleZ),(x2,y1+4,z2),mur)
            mur_sol((midtailleX,y1,midtailleZ),(x2,y1,z2),oak_planks)
            mur_sol((x1,y1,midtailleZ),(midtailleX,y1,z2),grass_block)
            
            poserFenetre((midtailleX,y1+1,midtailleZ+1),(midtailleX,y1+5,z2-1),glass)
            poserFenetre((x2-1,y1+1,z1+1),(x2-1,y1+5,z2-1),glass)
            poserFenetre((midtailleX+1,y1+1,z2-1),(x2-1,y1+5,z2-1),glass)
            poserFenetre((x1+2,y1+1,z1),(x2-1,y1+5,z1),glass)
            poserFenetre((x1+2,y1+1,midtailleZ-1),(midtailleX-1,y1+5,midtailleZ-1),glass)
            
            
            
        
            if  (tailleZ-((z2-z1)//2))%2==0:
        
                    poserPorte((x1+tailleX//2,hauteurMin+1,z2-(tailleZ//4)-2),door)
                    poserPorte((x1+tailleX//2,hauteurMin+1,z2-(tailleZ//4)-1),door)
                    mur_sol((x1,y1,z2-(tailleZ//4)-2),(x1+tailleX//2,y1,z2-(tailleZ//4)),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if (x1+i< x1+(tailleX//2) and z2-j>=z2-tailleZ//2 ) and(x1+i==x1 or z2-j==z2) and z2-j != z2-(tailleZ//4)-1 and z2-j != z2-(tailleZ//4):
                                
                                editor.placeBlock((x1+i,y1+1,z2-1-j),fence)
            else:
                
                    poserPorte((x1+tailleX//2,hauteurMin+1,z2-(tailleZ//4)-1),door)
                    mur_sol((x1,y1,z2-(tailleZ//4)-1),(x1+tailleX//2,y1,z2-(tailleZ//4)),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if (x1+i< x1+(tailleX//2) and z2-j>=z2-tailleZ//2 ) and (x1+i==x1 or z2-j==z2) and z2-j != z2-(tailleZ//4):
                              
                                editor.placeBlock((x1+i,y1+1,z2-1-j),fence)
                            
                    
                    
                    
            poserToit(co1,co2,hauteurMax,cotegarage,style,direction)    
            
            
            
        
      
    
    
    
    
    elif direction=='east' :
        door=Block(style['door'],{"facing": "west"})
        if cotegarage=='right':
            
                                    
                                    
                                
            #murs
             #murs
            poserGarage((x2-2,y1+1,z1+1),(x2-2,y1+3,midtailleZ-1))
            mur_sol((x1,y1+1,z1),(x2,y1+5,z1),mur)
            mur_sol((x1,y1+1,z1),(x1,y1+5,z2   ),mur)
            mur_sol((x2-1,y1+1,z1),(x2-1,y1+5,midtailleZ),mur)
            mur_sol((midtailleX,y1+1,midtailleZ),(midtailleX,y1+5,z2),mur)
            mur_sol((midtailleX,y1+1,midtailleZ-1),(x2,y1+5,midtailleZ-1),mur)
            mur_sol((x1,y1+1,z2-1),(midtailleX,y1+5,z2-1),mur)
            
            
            mur_sol((x2-1,y1+1,z1+1),(x2-1,y1+4,midtailleZ-1),air)
           
            
            #sols/plafonds
            mur_sol((x1,y1+4,z1),(x2,y1+4,midtailleZ),mur)
            mur_sol((x1,y1,z1),(x2,y1,midtailleZ),sol)
            mur_sol((x1,y1+4,midtailleZ),(midtailleX+1,y1+4,z2),mur)
            mur_sol((x1,y1,midtailleZ),(midtailleX+1,y1,z2),sol)
            mur_sol((midtailleX+1,y1,midtailleZ),(x2,y1,z2),grass)
            
            poserFenetre((x1+1,y1+1,z2-1),(midtailleX-1,y1+5,z2-1),glass)
            poserFenetre((midtailleX+1,y1+1,midtailleZ-1),(x2-2,y1+5,midtailleZ-1),glass)
            poserFenetre((midtailleX,y1+1,midtailleZ+1),(midtailleX,y1+5,z2-1),glass)
            poserFenetre((x1+1,y1+1,z1),(x2-1,y1+5,z1),glass)
            poserFenetre((x1,y1+1,z1+1),(x1,y1+5,z2-1   ),glass)
            
            
            
    
    
            if  (tailleZ-((z2-z1)//2))%2==0:
        
                    poserPorte((x1+tailleX//2,hauteurMin+1,z2-1-(tailleZ//4)),door)
                    poserPorte((x1+tailleX//2,hauteurMin+1,z2-(tailleZ//4)-2),door)
                    mur_sol((midtailleX,y1,z2-2-(tailleZ//4)),(x2,y1,z2-(tailleZ//4)-4),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if (midtailleX+1+i< x2 and z1+j>=midtailleZ ) and (midtailleX+i+1==x2-1 or z1+j==z2-1)   and z1+j != z2-1-(tailleZ//4) and z1+j != z2-2-(tailleZ//4) :
                                
                                editor.placeBlock((midtailleX+1+i,y1+1,z1+j),fence)
            else:
                
                    poserPorte((x1+tailleX//2,hauteurMin+1,z2-1-(tailleZ//4)),door)
                    mur_sol((midtailleX,y1,z2-1-(tailleZ//4)),(x2,y1,z2-(tailleZ//4)-2),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if (midtailleX+1+i< x2 and z1+j>=midtailleZ ) and (midtailleX+i+1==x2-1 or z1+j==z2-1)   and z1+j != z2-1-(tailleZ//4):
                          
                                editor.placeBlock((midtailleX+i+1,y1+1,z1+j),fence)
                            
                    
                    
                    
            poserToit(co1,co2,hauteurMax,cotegarage,style,direction )    
            
        
        
        
        elif cotegarage=='left':
                
            
                                
                        
                                    
                    
                
                
                            
                   
                                
            #murs
            poserGarage((x2-2,y1+1,midtailleZ+1),(x2-2,y1+3,z2-1))
            mur_sol((x1,y1+1,z1),(midtailleX,y1+5,z1),mur)
            mur_sol((x1,y1+1,z1),(x1,y1+5,z2   ),mur)
            mur_sol((x2-1,y1+1,midtailleZ),(x2-1,y1+5,z2),mur)
            mur_sol((midtailleX,y1+1,z1),(midtailleX,y1+5,midtailleZ),mur)
            mur_sol((midtailleX,y1+1,midtailleZ),(x2,y1+5,midtailleZ),mur)
            mur_sol((x1,y1+1,z2-1),(x2,y1+5,z2-1),mur)
            
            
            mur_sol((x2-1,y1+1,midtailleZ+1),(x2-1,y1+4,z2-1),air)
         
            
            #sols/plafonds
            mur_sol((x1,y1+4,midtailleZ),(x2,y1+4,z2),mur)
            mur_sol((x1,y1,midtailleZ),(x2,y1,z2),sol)
            mur_sol((x1,y1+4,z1),(midtailleX+1,y1+4,midtailleZ),mur)
            mur_sol((x1,y1,z1),(midtailleX+1,y1,midtailleZ),sol)
            mur_sol((midtailleX+1,y1,z1),(x2,y1,midtailleZ),grass)
            
            poserFenetre((x1+1,y1+1,z1),(midtailleX,y1+5,z1),glass)
            poserFenetre((x1,y1+1,z1+1),(x1,y1+5,z2-1   ),glass)
            poserFenetre((midtailleX,y1+1,z1+1),(midtailleX,y1+5,midtailleZ-1),glass)
            poserFenetre((midtailleX+2,y1+1,midtailleZ),(x2-2,y1+5,midtailleZ),glass)
            poserFenetre((x1+1,y1+1,z2-1),(x2-1,y1+5,z2-1),glass)
            
            
            
    
    
            if  ((z2-z1)//2)%2==0:
        
                    poserPorte((x1+tailleX//2,hauteurMin+1,z1+(tailleZ//4)),door)
                    poserPorte((x1+tailleX//2,hauteurMin+1,z1+(tailleZ//4)+1),door)
                    mur_sol((midtailleX,y1,z1+(tailleZ//4)),(x2,y1,z1+(tailleZ//4)+2),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if (midtailleX+1+i< x2 and z1+j<midtailleZ ) and(midtailleX+i+1==x2-1 or z1+j==z1)and z2-j != z2-(tailleZ//4)-1 and z2-j != z2-(tailleZ//4):
                                
                                editor.placeBlock((x1+i,y1+1,z2-1-j),fence)
            else:
                
                    poserPorte((x1+tailleX//2,hauteurMin+1,z1+(tailleZ//4)),door)
                    mur_sol((midtailleX,y1,z1+(tailleZ//4)),(x2,y1,z1+(tailleZ//4)+1),chemin)
                    for i in range(tailleX):
                        for j in range(tailleZ):
                            if (midtailleX+1+i< x2 and z1+j<midtailleZ ) and (midtailleX+i+1==x2-1 or z1+j==z1)   and z2-j != z2-(tailleZ//4):
                            
                                editor.placeBlock((midtailleX+i+1,y1+1,z1+j),fence)
                            
                    
                    
                    
            poserToit(co1,co2,hauteurMax,cotegarage,style,direction )   
        
        
        
    elif direction=='north' :
            door=Block(style['door'],{"facing": "south"})
            if cotegarage=='right':
                
                                        
                                        
                                    
                #murs
                #murs
                poserGarage((x1+1,y1+1,z1+1),(midtailleX-1,y1+3,z1+1))
                mur_sol((x1,y1+1,z1),(midtailleX,y1+5,z1),mur)
                mur_sol((midtailleX-1,y1+1,z1),(midtailleX-1,y1+5,midtailleZ   ),mur)
                mur_sol((x1,y1+1,z1),(x1,y1+5,z2),mur)
                mur_sol((x1,y1+1,z2-1),(x2,y1+5,z2-1),mur)
                mur_sol((x2-1,y1+1,midtailleZ),(x2-1,y1+5,z2),mur)
                mur_sol((midtailleX,y1+1,midtailleZ),(x2-1,y1+5,midtailleZ),mur)
                
                
                mur_sol((x1+1,y1+1,z1),(midtailleX-1,y1+4,z1),air)
         
                
                #sols/plafonds
                mur_sol((x1,y1+4,z1),(x2,y1+4,z2),mur)
                mur_sol((x1,y1,z1),(x2,y1,z2),sol)
                
                mur_sol((midtailleX,y1+4,z1),(x2,y1+4,midtailleZ),air)
                
                mur_sol((midtailleX,y1,z1),(x2,y1,midtailleZ),grass)
                
                poserFenetre((midtailleX+1,y1+1,midtailleZ),(x2-1,y1+5,midtailleZ),glass)
                poserFenetre((x2-1,y1+1,midtailleZ+1),(x2-1,y1+5,z2-1),glass)
                poserFenetre((x1+1,y1+1,z2-1),(x2-1,y1+5,z2-1),glass)
                poserFenetre((x1,y1+1,z1+1),(x1,y1+5,z2-1),glass)
                poserFenetre((midtailleX-1,y1+1,z1+2),(midtailleX-1,y1+5,midtailleZ -1  ),glass)
                
                
                
        
        
                if  (tailleX-((x2-x1)//2))%2==0:
            
                        poserPorte((x2-1-tailleX//4,hauteurMin+1,midtailleZ),door)
                        poserPorte((x2-2-tailleX//4,hauteurMin+1,midtailleZ),door)
                        mur_sol((x2-2-tailleX//4,y1,z1),(x2-tailleX//4,y1,midtailleZ),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if (x1+i>= midtailleX and z1+j<midtailleZ ) and (x1+i==x2-1 or z1+j==z1)   and x1+i != x2-1-tailleX//4 and x1+i != x2-2-tailleX//4:
                                    
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                else:
                    
                        poserPorte((x2-1-tailleX//4,hauteurMin+1,midtailleZ),door)
                        mur_sol((x2-1-tailleX//4,y1,z1),(x2-tailleX//4,y1,midtailleZ),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if (x1+i>= midtailleX and z1+j<midtailleZ ) and (x1+i==x2-1 or z1+j==z1)   and x1+i != x2-1-tailleX//4:
                                  
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                                
                        
                        
                        
                poserToit(co1,co2,hauteurMax,cotegarage,style,direction )    
                
            
            
            
            elif cotegarage=='left':
                    
                
                                    
                            
                                        
                        
                    
                    
                                   
                #murs
                #murs
                poserGarage((midtailleX+1,y1+1,z1+1),(x2-1,y1+3,z1+1))
                mur_sol((x1,y1+1,midtailleZ),(midtailleX,y1+5,midtailleZ),mur)
                mur_sol((midtailleX,y1+1,z1),(midtailleX,y1+5,midtailleZ   ),mur)
                mur_sol((x1,y1+1,midtailleZ),(x1,y1+5,z2),mur)
                mur_sol((x1,y1+1,z2-1),(x2,y1+5,z2-1),mur)
                mur_sol((x2-1,y1+1,z1),(x2-1,y1+5,z2),mur)
                
                
                
               
         
                
                #sols/plafonds
                mur_sol((x1,y1+4,z1),(x2,y1+4,z2),mur)
                mur_sol((x1,y1,z1),(x2,y1,z2),sol)
                
                mur_sol((x1,y1+4,z1),(midtailleX,y1+4,midtailleZ),air)
                
                mur_sol((x1,y1,z1),(midtailleX,y1,midtailleZ),grass)
                
                poserFenetre((x1+1,y1+1,midtailleZ),(midtailleX-1,y1+5,midtailleZ),glass)
                poserFenetre((midtailleX,y1+1,z1+2),(midtailleX,y1+5,midtailleZ -1  ),glass)
                poserFenetre((x1,y1+1,midtailleZ+1),(x1,y1+5,z2-1),glass)
                poserFenetre((x1+1,y1+1,z2-1),(x2-1,y1+5,z2-1),glass)
                poserFenetre((x2-1,y1+1,z1+1),(x2-1,y1+5,z2-1),glass)
                
                
                
        
        
                if  (((x2-x1)//2))%2==0:
            
                        poserPorte((x1+tailleX//4,hauteurMin+1,midtailleZ),door)
                        poserPorte((x1+1+tailleX//4,hauteurMin+1,midtailleZ),door)
                        mur_sol((x1+1+tailleX//4,y1,z1),(x1+2+tailleX//4,y1,midtailleZ),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if (x1+i>= midtailleX and z1+j<midtailleZ ) and (x1+i==x2-1 or z1+j==z1)   and x1+i != x1+tailleX//4 and x1+i != x1+1+tailleX//4:
                                    
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                else:
                    
                        poserPorte((x1+tailleX//4,hauteurMin+1,midtailleZ),door)
                        mur_sol((x1+tailleX//4,y1,z1),(x1+1+tailleX//4,y1,midtailleZ),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if (x1+i< midtailleX and z1+j<midtailleZ ) and (x1+i==x1 or z1+j==z1)   and x1+i != x1+tailleX//4:
                                   
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                                
                        
                        
                        
                poserToit(co1,co2,hauteurMax,cotegarage,style,direction )    
                
                
    
    elif direction=='south' :
            door=Block(style['door'],{"facing": "north"})
            if cotegarage=='right':
                
                                        
                                        
              #murs
                #murs
                poserGarage((midtailleX+1,y1+1,z2-2),(x2-1,y1+3,z2-2))
                mur_sol((x1,y1+1,midtailleZ-1),(midtailleX,y1+5,midtailleZ-1),mur)
                mur_sol((x2-1,y1+1,z1),(x2-1,y1+5,z2   ),mur)
                mur_sol((midtailleX,y1+1,midtailleZ),(midtailleX,y1+5,z2),mur)
                mur_sol((x1,y1+1,z1),(x2,y1+5,z1),mur)
                mur_sol((x1,y1+1,z1 ),(x1,y1+5,midtailleZ),mur)
                
                
                
               
         
                
                #sols/plafonds
                mur_sol((x1,y1+4,z1),(x2,y1+4,z2),mur)
                mur_sol((x1,y1,z1),(x2,y1,z2),sol)
                
                mur_sol((x1,y1+4,midtailleZ),(midtailleX,y1+4,z2),air)
                
                mur_sol((x1,y1,midtailleZ),(midtailleX,y1,z2),grass)
                
                poserFenetre((x1+1,y1+1,midtailleZ-1),(midtailleX-1,y1+5,midtailleZ-1),glass)
                poserFenetre((x2-1,y1+1,z1+1),(x2-1,y1+5,z2-1   ),glass)
                poserFenetre((midtailleX,y1+1,midtailleZ+1),(midtailleX,y1+5,z2-2),glass)
                poserFenetre((x1+1,y1+1,z1),(x2-1,y1+5,z1),glass)
                poserFenetre((x1,y1+1,z1+1 ),(x1,y1+5,midtailleZ-1),glass)
                
                
                
        
        
                if  (((x2-x1)//2))%2==0:
            
                        poserPorte((x1+tailleX//4,hauteurMin+1,midtailleZ),door)
                        poserPorte((x1+1+tailleX//4,hauteurMin+1,midtailleZ),door)
                        mur_sol((x1+tailleX//4,y1,midtailleZ),(x1+2+tailleX//4,y1,z2),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if  (x1+i< midtailleX and z1+j>=midtailleZ )and (x1+i==x1 or z1+j==z2-1)   and x1+i != x1+tailleX//4 and x1+i != x1+1+tailleX//4:
                                    
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                else:
                    
                        poserPorte((x1+tailleX//4,hauteurMin+1,midtailleZ-1),door)
                        mur_sol((x1+tailleX//4,y1,midtailleZ),(x1+1+tailleX//4,y1,z2),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if (x1+i< midtailleX and z1+j>=midtailleZ )and (x1+i==x1 or z1+j==z2-1)  and x1+i != x1+tailleX//4:
                                   
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                                
                        
                        
                        
                poserToit(co1,co2,hauteurMax,cotegarage,style,direction )    
            
            
            
            elif cotegarage=='left':
                 #murs
                #murs
                poserGarage((x1+1,y1+1,z2-2),(midtailleX-1,y1+3,z2-2))
                mur_sol((midtailleX,y1+1,midtailleZ-1),(x2,y1+5,midtailleZ-1),mur)
                mur_sol((x2-1,y1+1,z1),(x2-1,y1+5,midtailleZ   ),mur)
                mur_sol((x1,y1+1,z1),(x1,y1+5,z2),mur)
                mur_sol((x1,y1+1,z1),(x2,y1+5,z1),mur)
                mur_sol((midtailleX-1,y1+1,midtailleZ ),(midtailleX-1,y1+5,z2),mur)
                
                
                
               
         
                
                #sols/plafonds
                mur_sol((x1,y1+4,z1),(x2,y1+4,z2),mur)
                mur_sol((x1,y1,z1),(x2,y1,z2),sol)
                
                mur_sol((midtailleX,y1+4,midtailleZ),(x2,y1+4,z2),air)
                
                mur_sol((midtailleX,y1,midtailleZ),(x2,y1,z2),grass)
                
                poserFenetre((midtailleX+1,y1+1,midtailleZ-1),(x2-1,y1+5,midtailleZ-1),glass)
                poserFenetre((x2-1,y1+1,z1+1),(x2-1,y1+5,midtailleZ-1   ),glass)
                poserFenetre((x1,y1+1,z1+1),(x1,y1+5,z2-1),glass)
                poserFenetre((x1+1,y1+1,z1),(x2-1,y1+5,z1),glass)
                poserFenetre((midtailleX-1,y1+1,midtailleZ+1 ),(midtailleX-1,y1+5,z2-2),glass)
                
                
                
        
        
                if  (((x2-x1)//2))%2==0:
            
                        poserPorte((x2-tailleX//4,hauteurMin+1,midtailleZ),door)
                        poserPorte((x2-1-tailleX//4,hauteurMin+1,midtailleZ),door)
                        mur_sol((x2-1-tailleX//4,y1,midtailleZ),(x2-3-tailleX//4,y1,z2),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if (x1+i>= midtailleX and z1+j>=midtailleZ )and (x1+i==x2-1 or z1+j==z2-1)   and x1+i != x2-2-tailleX//4 and x1+i != x2-1-tailleX//4:
                                    
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                else:
                    
                        poserPorte((x2-1-tailleX//4,hauteurMin+1,midtailleZ-1),door)
                        mur_sol((x2-1-tailleX//4,y1,midtailleZ),(x2-2-tailleX//4,y1,z2),chemin)
                        for i in range(tailleX):
                            for j in range(tailleZ):
                                if (x1+i>= midtailleX and z1+j>=midtailleZ )and (x1+i==x2-1 or z1+j==z2-1)  and x1+i != x2-1-tailleX//4:
                                   
                                    editor.placeBlock((x1+i,y1+1,z1+j),fence)
                                
                        
                        
                        
                poserToit(co1,co2,hauteurMax,cotegarage,style,direction )    
                
                
                
if __name__=="__main__":
    
    
   
        
        
    nb_style=randint(0,3)
    
    delete((-40,-60,-40),(50,-40,50)) 
    
    house((-20,-60,-20),(-10,-60,-10),"right",10,nb_style,'north')
    

   
    

    
    
    
    
    
