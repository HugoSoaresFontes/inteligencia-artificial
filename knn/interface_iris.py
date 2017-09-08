from Tkinter import *

# Interface grafica
class Interface:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["padx"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["padx"] = 20
        self.quintoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["padx"] = 20
        self.sextoContainer.pack()

        self.setimoContainer = Frame(master)
        self.setimoContainer["pady"] = 20
        self.setimoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="KNN para o database IRIS")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.lenghtSepalLabel = Label(self.segundoContainer,text="Sepal Lenght", font=self.fontePadrao)
        self.lenghtSepalLabel.pack(side=LEFT)

        self.lengthSepal = Entry(self.segundoContainer)
        self.lengthSepal["width"] = 30
        self.lengthSepal["font"] = self.fontePadrao
        self.lengthSepal.pack(side=LEFT)

        self.widthSepalLabel = Label(self.terceiroContainer, text="Sepal Width", font=self.fontePadrao)
        self.widthSepalLabel.pack(side=LEFT)

        self.widthSepal = Entry(self.terceiroContainer)
        self.widthSepal["width"] = 30
        self.widthSepal["font"] = self.fontePadrao
        self.widthSepal.pack(side=LEFT)

        self.lengthPetalLabel = Label(self.quartoContainer, text="Petal Lenth", font=self.fontePadrao)
        self.lengthPetalLabel.pack(side=LEFT)

        self.lengthPetal = Entry(self.quartoContainer)
        self.lengthPetal["width"] = 30
        self.lengthPetal["font"] = self.fontePadrao
        self.lengthPetal.pack(side=LEFT)

        self.widthPetalLabel = Label(self.quintoContainer, text="Petal Width", font=self.fontePadrao)
        self.widthPetalLabel.pack(side=LEFT)

        self.widthPetal = Entry(self.quintoContainer)
        self.widthPetal["width"] = 30
        self.widthPetal["font"] = self.fontePadrao
        self.widthPetal.pack(side=LEFT)

        self.vizinhosLabel = Label(self.sextoContainer, text="N de vizinhos", font=self.fontePadrao)
        self.vizinhosLabel.pack(side=LEFT)

        self.vizinhos = Entry(self.sextoContainer)
        self.vizinhos["width"] = 30
        self.vizinhos["font"] = self.fontePadrao
        self.vizinhos.pack(side=LEFT)

        self.autenticar = Button(self.setimoContainer)
        self.autenticar["text"] = "Classificar"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.classificar
        self.autenticar.pack()

        self.mensagem = Label(self.setimoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

    def classificar(self):
        plt.close('all')
        valores_alvo = [0,0,0,0,""]
        valores_alvo[0] = float(self.lengthSepal.get())
        valores_alvo[1] = float(self.widthSepal.get())
        valores_alvo[2] = float(self.lengthPetal.get())
        valores_alvo[3] = float(self.widthPetal.get())
        valores_alvo[4] = ""
        quantidade_vizinhos = int(self.vizinhos.get())

        resposta = main(valores_alvo, quantidade_vizinhos)
        self.mensagem["text"] = "Classe: " + str(resposta[0]) + ". Precisao da resposta: " + str(resposta[1]) + "%" + "    Usando as centroides, Classe: " + str(resposta[2])
        vermelho = mpatches.Patch(color='red', label='Iris versicolor')
        azul = mpatches.Patch(color='blue', label='Iris virginica')
        verde = mpatches.Patch(color='green', label='Iris septosa')
        amarelo = mpatches.Patch(color='yellow', label='Alvo e seus k vizinhos')
        plt.legend(handles=[vermelho, verde, azul, amarelo])

        plt.show()
