from datetime import datetime, timedelta


class PlayList:
    def __init__(self, i, n, d):
        self.__id = i
        self.__nome = n
        self.__descricao = d
        self.__tempo = timedelta() 

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_descricao(self): return self.__descricao
    def set_id(self, i): self.__id = i
    def set_nome(self, n): self.__nome = n
    def set_descricao(self, d): self.__descricao = d
    def set_tempo(self, t): self.__tempo = t

    def TempoTotal(self):
        return self.__tempo

    def __str__(self):
        return f"{self.__id} - {self.__nome} ({self.__descricao}) - duração {self.__tempo}"


class Musica:
    def __init__(self, i, t, art, alb, d):
        self.__id = i
        self.__titulo = t
        self.__artista = art
        self.__album = alb
        self.__duracao = d

    def get_id(self): return self.__id
    def get_titulo(self): return self.__titulo
    def get_artista(self): return self.__artista
    def get_album(self): return self.__album
    def get_duracao(self): return self.__duracao
    def set_id(self, i): self.__id = i
    def set_titulo(self, t): self.__titulo = t
    def set_artista(self, art): self.__artista = art
    def set_album(self, alb): self.__album = alb
    def set_duracao(self, d): self.__duracao = d

    def __str__(self):
        return (f"{self.__id} - {self.__titulo} - {self.__artista} - "
                f"{self.__album} - {self.__duracao}")


class PlayListItem:
    def __init__(self, i, ip, im, d, s):
        self.__id = i
        self.__id_playlist = ip
        self.__id_musica = im
        self.__data_inclusao = d
        self.__sequencia = s

    def get_id(self): return self.__id
    def get_id_playlist(self): return self.__id_playlist
    def get_id_musica(self): return self.__id_musica
    def get_data_inclusao(self): return self.__data_inclusao
    def get_sequencia(self): return self.__sequencia
    def set_id(self, i): self.__id = i
    def set_id_playlist(self, ip): self.__id_playlist = ip
    def set_id_musica(self, im): self.__id_musica = im
    def set_data_inclusao(self, d): self.__data_inclusao = d
    def set_sequencia(self, s): self.__sequencia = s

    def __str__(self):
        return (f"{self.__id} - playlist {self.__id_playlist} - música {self.__id_musica} - "
                f"incluída em {self.__data_inclusao.strftime('%d/%m/%Y')} - "
                f"posição {self.__sequencia}")


class UI:
    def __init__(self):
        self.__playlists = []
        self.__musicas = []
        self.__itens = []

    def __proximo_id(self, lista):
        return max([x.get_id() for x in lista], default=0) + 1

    def __buscar(self, lista, id):
        for x in lista:
            if x.get_id() == id:
                return x
        return None

    def __ler_duracao(self):
        m, s = map(int, input("Duração (mm:ss): ").split(":"))
        return timedelta(minutes=m, seconds=s)

    def __atualizar_tempos(self):
        for p in self.__playlists:
            total = timedelta()
            for it in self.__itens:
                if it.get_id_playlist() == p.get_id():
                    m = self.__buscar(self.__musicas, it.get_id_musica())
                    total += m.get_duracao()
            p.set_tempo(total)

    def __listar(self, lista):
        if not lista:
            print("Nada cadastrado.")
        for x in lista:
            print(x)

    @staticmethod
    def Main():
        ui = UI()
        op = 0
        while op != 13:
            op = ui.Menu()
            try:
                if op == 1: ui.PlayListInserir()
                elif op == 2: ui.PlayListListar()
                elif op == 3: ui.PlayListAtualizar()
                elif op == 4: ui.PlayListExcluir()
                elif op == 5: ui.MusicaInserir()
                elif op == 6: ui.MusicaListar()
                elif op == 7: ui.MusicaAtualizar()
                elif op == 8: ui.MusicaExcluir()
                elif op == 9: ui.ItemInserir()
                elif op == 10: ui.ItemListar()
                elif op == 11: ui.ItemAtualizar()
                elif op == 12: ui.ItemExcluir()
            except ValueError:
                print("Dado inválido, tente novamente.")

    def Menu(self):
        print("\n--- PlayList ---     1-Inserir  2-Listar  3-Atualizar  4-Excluir")
        print("Playlists: 1 a 4 | Músicas: 5 a 8 | Itens da playlist: 9 a 12 | 13-Sair")
        try:
            return int(input("Opção: "))
        except ValueError:
            return 0

    def PlayListInserir(self):
        nome = input("Nome: ")
        desc = input("Descrição: ")
        self.__playlists.append(PlayList(self.__proximo_id(self.__playlists), nome, desc))

    def PlayListListar(self):
        self.__listar(self.__playlists)

    def PlayListAtualizar(self):
        p = self.__buscar(self.__playlists, int(input("Id da playlist: ")))
        if p is None:
            print("Playlist não encontrada.")
            return
        p.set_nome(input("Novo nome: "))
        p.set_descricao(input("Nova descrição: "))

    def PlayListExcluir(self):
        p = self.__buscar(self.__playlists, int(input("Id da playlist: ")))
        if p is None:
            print("Playlist não encontrada.")
            return
        self.__playlists.remove(p)
        self.__itens = [i for i in self.__itens if i.get_id_playlist() != p.get_id()]

    def MusicaInserir(self):
        t = input("Título: ")
        art = input("Artista: ")
        alb = input("Álbum: ")
        d = self.__ler_duracao()
        self.__musicas.append(Musica(self.__proximo_id(self.__musicas), t, art, alb, d))

    def MusicaListar(self):
        self.__listar(self.__musicas)

    def MusicaAtualizar(self):
        m = self.__buscar(self.__musicas, int(input("Id da música: ")))
        if m is None:
            print("Música não encontrada.")
            return
        m.set_titulo(input("Novo título: "))
        m.set_artista(input("Novo artista: "))
        m.set_album(input("Novo álbum: "))
        m.set_duracao(self.__ler_duracao())
        self.__atualizar_tempos()

    def MusicaExcluir(self):
        m = self.__buscar(self.__musicas, int(input("Id da música: ")))
        if m is None:
            print("Música não encontrada.")
            return
        self.__musicas.remove(m)
        self.__itens = [i for i in self.__itens if i.get_id_musica() != m.get_id()]
        self.__atualizar_tempos()

    def ItemInserir(self):
        ip = int(input("Id da playlist: "))
        im = int(input("Id da música: "))
        if self.__buscar(self.__playlists, ip) is None or self.__buscar(self.__musicas, im) is None:
            print("Playlist ou música não encontrada.")
            return
        seq = len([i for i in self.__itens if i.get_id_playlist() == ip]) + 1
        self.__itens.append(PlayListItem(self.__proximo_id(self.__itens), ip, im, datetime.now(), seq))
        self.__atualizar_tempos()

    def ItemListar(self):
        ip = int(input("Id da playlist: "))
        itens = [i for i in self.__itens if i.get_id_playlist() == ip]
        itens.sort(key=lambda i: i.get_sequencia())
        self.__listar(itens)

    def ItemAtualizar(self):
        it = self.__buscar(self.__itens, int(input("Id do item: ")))
        if it is None:
            print("Item não encontrado.")
            return
        it.set_sequencia(int(input("Nova sequência: ")))

    def ItemExcluir(self):
        it = self.__buscar(self.__itens, int(input("Id do item: ")))
        if it is None:
            print("Item não encontrado.")
            return
        self.__itens.remove(it)
        self.__atualizar_tempos()


UI.Main()
