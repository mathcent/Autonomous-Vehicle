import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def calcula_posicao(x,y):
        x_fora = [-51,-4.5,
                64.5,111,
                111,64.5,
                -4.5,-51]

        y_fora = [-4.5,-51,
                -51,-4.5,
                133.5,180,
                180,133]


        x_dentro = [-39,-4.5,
                64.5,99,
                99,64.5,
                -4.5,-39]
        y_dentro = [-4.5,-39,
                -39,-4.5,
                133.5,168,
                168,133.5]

        plt.fill(x_fora, y_fora, facecolor='none', edgecolor='purple', linewidth=1)
        plt.fill(x_dentro, y_dentro, facecolor='none', edgecolor='purple', linewidth=1)

        # aqui você pode colocar uma condição tipo, "se dentro do plot vermelho, se não preto", mudando o parâmetro "c"
        pontos = []
        for i in range(0,len(x)):
                pontos.append((x[i],y[i]))
                plt.plot(x[i],y[i], c="red", markersize=5, marker=".")

        plt.show()   
        print(pontos)




        # aqui você vai criar vários pontos, cada um a localização do carro




        # aqui você vai ter que definir os pontos (x,y) de cada vértice do polígno.
        # quando tiver todos os pontos, é só colocar mais dentro da lista
        # "holes" é uma lista com os pontos de dentro.
        polygon = Polygon(
                [(x_fora[0], y_fora[0]) , (x_fora[1], y_fora[1]), (x_fora[2], y_fora[2]), (x_fora[3], y_fora[3])], 
                holes=pontos
        )
        print(polygon.contains(Point(x[0],y[0])))
#>>> True
x = [2,30]
y = [4,50]
calcula_posicao(x,y)