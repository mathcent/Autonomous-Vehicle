import numpy as np
from skfuzzy import control
import skfuzzy




#Ficar no meio da pista




def controleFreio():
    #Velocidade e freio
    distanciaPlaca = control.Antecedent(np.arange(1,10,0.1), 'distanciaPare')
    distaciaFarol = control.Antecedent(np.arange(1,10,0.1), 'distaciaFarol')
    velocidade = control.Antecedent(np.arange(1,10,0.1), 'velocidade')
    tipoPlaca = control.Antecedent(np.arange(1,6,1), 'tipoPlaca')

    distanciaPlaca['perto'] = skfuzzy.trapmf(distanciaPlaca.universe, [1,1,4,6])
    distanciaPlaca['medio'] = skfuzzy.trapmf(distanciaPlaca.universe, [1,1,4,6])
    distanciaPlaca['longe'] = skfuzzy.trapmf(distanciaPlaca.universe, [1,1,4,6])
    distanciaPlaca['none']=  skfuzzy.trapmf(distanciaPlaca.universe, [1,1,4,6])

    distaciaFarol['verde'] = skfuzzy.trapmf(distaciaFarol.universe, [1,1,4,6])
    distaciaFarol['perto'] = skfuzzy.trapmf(distaciaFarol.universe, [1,1,4,6])
    distaciaFarol['medio'] = skfuzzy.trapmf(distaciaFarol.universe, [1,1,4,6])
    distaciaFarol['longe'] = skfuzzy.trapmf(distaciaFarol.universe, [1,1,4,6])

    velocidade['alta']= skfuzzy.trapmf(velocidade.universe, [1,1,4,6])
    velocidade['media']= skfuzzy.trapmf(velocidade.universe, [1,1,4,6])
    velocidade['baixa']= skfuzzy.trapmf(velocidade.universe, [1,1,4,6])
    velocidade['parado']= skfuzzy.trapmf(velocidade.universe, [1,1,4,6])

    tipoPlaca['pare']= skfuzzy.trimf(tipoPlaca.universe, [0.5,1,1.5])
    tipoPlaca['altaV']= skfuzzy.trimf(tipoPlaca.universe, [1.5,2,2.5])
    tipoPlaca['mediaV']= skfuzzy.trimf(tipoPlaca.universe, [2.5,3,3.5])
    tipoPlaca['baixaV']= skfuzzy.trimf(tipoPlaca.universe, [3.5,4,4.5])
    tipoPlaca['baixaV']= skfuzzy.trimf(tipoPlaca.universe, [4.5,5,5.5])



def controlePlacaPare(disctancia):
    disctControle = control.Antecedent(np.arange(0,2500,1), 'disctControle')
    velControle = control.Consequent(np.arange(0,130,0.1), 'velControle')

    disctControle['distante'] = skfuzzy.trapmf(disctControle.universe, [0,0,300,500])
    disctControle['medio'] = skfuzzy.trapmf(disctControle.universe, [400 , 710 , 1500 , 1700])
    disctControle['perto'] = skfuzzy.trapmf(disctControle.universe, [1600 , 1900 , 2500 , 2500])


    velControle['baixa'] = skfuzzy.trimf(velControle.universe, [0,0,50])
    velControle['media'] = skfuzzy.trimf(velControle.universe, [40,65,90])
    velControle['alta'] = skfuzzy.trimf(velControle.universe, [80,115,130])

    regras = []
    regras.append(control.Rule(disctControle['distante'] ,velControle['alta']))
    regras.append(control.Rule(disctControle['medio'] ,velControle['media']))
    regras.append(control.Rule(disctControle['perto'] ,velControle['baixa']))



    pareControl = control.ControlSystem(regras)
    pareSimulacao = control.ControlSystemSimulation(pareControl)  
    #pareSimulacao.input['disctControle'] = 1200
    pareSimulacao.input['disctControle'] = disctancia
    pareSimulacao.compute()     
    print("Velocidade: ",pareSimulacao.output['velControle'])
    return pareSimulacao.output['velControle']


    
    
    print("a")

def controleLinha(erro):

    erroLinha = control.Antecedent(np.arange(-300,300,0.1), 'erroLinha')
    angulo = control.Consequent(np.arange(-0.035, 0.035, 0.001), 'angulo')

    erroLinha['direita']= skfuzzy.trapmf(erroLinha.universe, [-50,100,300,300])    
    #erroLinha['meio'] = skfuzzy.trimf(erroLinha.universe, [-50,0,50])
    erroLinha['esquerda']= skfuzzy.trapmf(erroLinha.universe, [-300,-300,-100,50])
        

    angulo['direita'] = skfuzzy.smf(angulo.universe, -0.015, 0.035)
    #angulo['meio'] = skfuzzy.trimf(angulo.universe, [-0.005,0,0.005])
    angulo['esquerda'] = skfuzzy.zmf(angulo.universe, -0.035, 0.015)
    
    regras = []
    regras.append(control.Rule(erroLinha['direita'] , 
                            angulo['direita']))
    regras.append(control.Rule(erroLinha['esquerda'] , 
                            angulo['esquerda']))   
    #regras.append(control.Rule(erroLinha['meio'], angulo['meio']))        

    angControl = control.ControlSystem(regras)
    angSimulacao = control.ControlSystemSimulation(angControl)  
    print(erro)
    angSimulacao.input['erroLinha'] = erro
    angSimulacao.compute()     
    print(angSimulacao.output['angulo'])
    return angSimulacao.output['angulo'][0]



