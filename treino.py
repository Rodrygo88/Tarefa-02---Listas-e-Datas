from datetime import datetime, timedelta


class Treino:
    def __init__(self, id, dt, ds, t):
        self.__id = id
        self.__data = dt
        self.__distancia = ds
        self.__tempo = t

    def get_id(self): return self.__id
    def get_data(self): return self.__data
    def get_distancia(self): return self.__distancia
    def get_tempo(self): return self.__tempo

    def set_id(self, id): self.__id = id
    def set_data(self, dt): self.__data = dt
    def set_distancia(self, ds): self.__distancia = ds
    def set_tempo(self, t): self.__tempo = t

    def Pace(self):
        segundos = self.__tempo.total_seconds() / self.__distancia
        return timedelta(seconds=round(segundos))

    def __str__(self):
        pace = str(self.Pace())[2:] 
        return (f"{self.__id} - {self.__data.strftime('%d/%m/%Y')} - "
                f"{self.__distancia} km - tempo {self.__tempo} - pace {pace} min/km")


class TreinoUI:
    def __init__(self):
        self.__treinos = []

    def __proximo_id(self):
        return max([t.get_id() for t in self.__treinos], default=0) + 1

    def __buscar(self, id):
        for t in self.__treinos:
            if t.get_id() == id:
                return t
        return None

    def __ler_dados(self):
        data = datetime.strptime(input("Data (dd/mm/aaaa): "), "%d/%m/%Y")
        distancia = float(input("Distância (km): "))
        h, m, s = map(int, input("Tempo (hh:mm:ss): ").split(":"))
        return data, distancia, timedelta(hours=h, minutes=m, seconds=s)

    @staticmethod
    def Main():
        ui = TreinoUI()
        op = 0
        while op != 7:
            op = ui.Menu()
            try:
                if op == 1: ui.Inserir()
                elif op == 2: ui.Listar()
                elif op == 3: ui.Listar_Id()
                elif op == 4: ui.Atualizar()
                elif op == 5: ui.Excluir()
                elif op == 6: ui.MaisRapido()
            except ValueError:
                print("Dado inválido, tente novamente.")

    def Menu(self):
        print("\n1-Inserir  2-Listar  3-Listar por id  4-Atualizar  "
              "5-Excluir  6-Treino mais rápido  7-Sair")
        try:
            return int(input("Opção: "))
        except ValueError:
            return 0

    def Inserir(self):
        data, distancia, tempo = self.__ler_dados()
        self.__treinos.append(Treino(self.__proximo_id(), data, distancia, tempo))
        print("Treino inserido.")

    def Listar(self):
        if not self.__treinos:
            print("Nenhum treino cadastrado.")
        for t in self.__treinos:
            print(t)

    def Listar_Id(self):
        t = self.__buscar(int(input("Id do treino: ")))
        print(t if t else "Treino não encontrado.")

    def Atualizar(self):
        t = self.__buscar(int(input("Id do treino: ")))
        if t is None:
            print("Treino não encontrado.")
            return
        data, distancia, tempo = self.__ler_dados()
        t.set_data(data)
        t.set_distancia(distancia)
        t.set_tempo(tempo)
        print("Treino atualizado.")

    def Excluir(self):
        t = self.__buscar(int(input("Id do treino: ")))
        if t is None:
            print("Treino não encontrado.")
        else:
            self.__treinos.remove(t)
            print("Treino excluído.")

    def MaisRapido(self):
        if not self.__treinos:
            print("Nenhum treino cadastrado.")
        else:
            print(min(self.__treinos, key=lambda t: t.Pace()))

TreinoUI.Main()
