import numpy as np
from skfuzzy import control
import skfuzzy




#Ficar no meio da pista

def controlePedestre(disctancia):
    disctControle = control.Antecedent(np.arange(0,3000,1), 'disctControle')
    velControle = control.Consequent(np.arange(-1,60,0.1), 'velControle')

    disctControle['proximo'] = skfuzzy.trapmf(disctControle.universe, [2500,2600,3000,3000])
    disctControle['medio'] = skfuzzy.trimf(disctControle.universe, [900,2200,2500])
    disctControle['distante'] = skfuzzy.trimf(disctControle.universe, [0,0,1000])

    velControle['baixa'] = skfuzzy.zmf(velControle.universe, 0,40)
    velControle['media'] = skfuzzy.smf(velControle.universe, 30,60)
    velControle['pare'] = skfuzzy.trimf(velControle.universe, [-0.1,0,0.1])

    regras = []
    regras.append(control.Rule(disctControle['distante'] ,velControle['media']))
    regras.append(control.Rule(disctControle['medio'] ,velControle['baixa']))
    regras.append(control.Rule(disctControle['proximo'] ,velControle['pare']))


    pareControl = control.ControlSystem(regras)
    pareSimulacao = control.ControlSystemSimulation(pareControl)  
    #pareSimulacao.input['disctControle'] = 1200
    pareSimulacao.input['disctControle'] = disctancia
    pareSimulacao.compute()     
    print("Velocidade: ",pareSimulacao.output['velControle'])
    return pareSimulacao.output['velControle']



def controleSemaforo(disctancia):
    disctControle = control.Antecedent(np.arange(0,2500,1), 'disctControle')
    velControle = control.Consequent(np.arange(-1,50,0.1), 'velControle')

    disctControle['proximo'] = skfuzzy.trapmf(disctControle.universe, [899,1000,2500,2500])
    disctControle['medio'] = skfuzzy.trimf(disctControle.universe, [400,600,901])
    disctControle['distante'] = skfuzzy.trimf(disctControle.universe, [0,0,500])

    velControle['baixa'] = skfuzzy.zmf(velControle.universe, -10,30)
    velControle['media'] = skfuzzy.smf(velControle.universe, 20,50)
    velControle['pare'] = skfuzzy.trimf(velControle.universe, [-0.1,0,0.1])

    regras = []
    regras.append(control.Rule(disctControle['distante'] ,velControle['media']))
    regras.append(control.Rule(disctControle['medio'] ,velControle['baixa']))
    regras.append(control.Rule(disctControle['proximo'] ,velControle['pare']))


    pareControl = control.ControlSystem(regras)
    pareSimulacao = control.ControlSystemSimulation(pareControl)  
    #pareSimulacao.input['disctControle'] = 1200
    pareSimulacao.input['disctControle'] = disctancia
    pareSimulacao.compute()     
    print("Velocidade: ",pareSimulacao.output['velControle'])
    return pareSimulacao.output['velControle']




def controlePlacaPare(disctancia):
    disctControle = control.Antecedent(np.arange(0,1400,1), 'disctControle')
    velControle = control.Consequent(np.arange(-1,80,0.1), 'velControle')

    disctControle['proximo'] = skfuzzy.trapmf(disctControle.universe, [1200,1400,1400,1400])
    disctControle['medio'] = skfuzzy.trimf(disctControle.universe, [500,1000,1200])
    disctControle['distante'] = skfuzzy.trimf(disctControle.universe, [0,0,600])

    velControle['baixa'] = skfuzzy.zmf(velControle.universe, 0,40)
    velControle['media'] = skfuzzy.smf(velControle.universe, 30,60)
    velControle['pare'] = skfuzzy.trimf(velControle.universe, [-0.1,0,0.1])

    regras = []
    regras.append(control.Rule(disctControle['distante'] ,velControle['media']))
    regras.append(control.Rule(disctControle['medio'] ,velControle['baixa']))
    regras.append(control.Rule(disctControle['proximo'] ,velControle['pare']))

    pareControl = control.ControlSystem(regras)
    pareSimulacao = control.ControlSystemSimulation(pareControl)  
    #pareSimulacao.input['disctControle'] = 1200
    pareSimulacao.input['disctControle'] = disctancia
    pareSimulacao.compute()     
    print("Velocidade: ",pareSimulacao.output['velControle'])
    return pareSimulacao.output['velControle']

    


def controleLinha(erro,anguloAntigo):

    erroLinha = control.Antecedent(np.arange(-1000,1000,0.1), 'erroLinha')
    angulo = control.Consequent(np.arange(-0.15, 0.15, 0.001), 'angulo')
    
    erroLinha['direita']= skfuzzy.trapmf(erroLinha.universe, [100,600,1000,1000])    
    erroLinha['meio'] = skfuzzy.trimf(erroLinha.universe, [-200,0,200])
    erroLinha['esquerda']= skfuzzy.trapmf(erroLinha.universe, [-1000,-1000,-600,-100])


    angulo['direita'] = skfuzzy.smf(angulo.universe, -0.01, 0.1)
    angulo['meio'] = skfuzzy.trimf(angulo.universe, [-0.005,0,0.005])
    angulo['esquerda'] = skfuzzy.zmf(angulo.universe, -0.1, 0.01)
    
    regras = []
    regras.append(control.Rule(erroLinha['direita'] , 
                            angulo['direita']))
    regras.append(control.Rule(erroLinha['meio'] ,angulo['meio']))  
    regras.append(control.Rule(erroLinha['esquerda'] , 
                            angulo['esquerda']))   
       
    try:
        angControl = control.ControlSystem(regras)
        angSimulacao = control.ControlSystemSimulation(angControl)  
        #print("Erro: ", erro[0])
        angSimulacao.input['erroLinha'] = erro
        angSimulacao.compute()     
        #print(angSimulacao.output['angulo'][0])
        return angSimulacao.output['angulo'][0]
    except:
        return anguloAntigo



