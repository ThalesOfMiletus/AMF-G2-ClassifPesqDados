import PySimpleGUI as sg
import random

class Jogo:
    def __init__(self, jogo_id, titulo, desenvolvedor, preco, generos):
        self.jogo_id = jogo_id
        self.titulo = titulo
        self.desenvolvedor = desenvolvedor
        self.preco = preco
        self.generos = generos


class NoJogo:
    def __init__(self, jogo):
        self.jogo = jogo
        self.esquerda = None
        self.direita = None


class ArvoreJogos:
    def __init__(self):
        self.raiz = None

    def altura(self, no): # função para calcular a altura de um nó na árvore.
        if no is None:
            return 0
        return max(self.altura(no.esquerda), self.altura(no.direita)) + 1

    def fator_balanceamento(self, no): #calcular a diferença entre a altura da subárvore esquerda e a altura da subárvore direita
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotacao_direita(self, z):
        y = z.esquerda
        T2 = y.direita

        y.direita = z
        z.esquerda = T2

        return y

    def rotacao_esquerda(self, y):
        x = y.direita
        T2 = x.esquerda

        x.esquerda = y
        y.direita = T2

        return x

    def inserir(self, jogo):
        novo_no = NoJogo(jogo)

        if self.raiz is None:
            self.raiz = novo_no
        else:
            self.raiz = self.add_recursivo(self.raiz, novo_no)

    def add_recursivo(self, no_atual, novo_no):
        if no_atual is None:
            return novo_no

        if novo_no.jogo.preco < no_atual.jogo.preco:
            no_atual.esquerda = self.add_recursivo(no_atual.esquerda, novo_no)
        elif novo_no.jogo.preco > no_atual.jogo.preco:
            no_atual.direita = self.add_recursivo(no_atual.direita, novo_no)
        else:
            return no_atual

        no_atual.altura = 1 + max(self.altura(no_atual.esquerda), self.altura(no_atual.direita))

        # pega o fator de balanceamento pra ver se precisa fazer alguma rotação
        balanceamento = self.fator_balanceamento(no_atual)

        # Casos de desequilíbrio
        # Esquerda-Esquerda
        if balanceamento > 1 and novo_no.jogo.preco < no_atual.esquerda.jogo.preco:
            return self.rotacao_direita(no_atual)

        # Direita-Direita
        if balanceamento < -1 and novo_no.jogo.preco > no_atual.direita.jogo.preco:
            return self.rotacao_esquerda(no_atual)

        # Esquerda-Direita
        if balanceamento > 1 and novo_no.jogo.preco > no_atual.esquerda.jogo.preco:
            no_atual.esquerda = self.rotacao_esquerda(no_atual.esquerda)
            return self.rotacao_direita(no_atual)

        # Direita-Esquerda
        if balanceamento < -1 and novo_no.jogo.preco < no_atual.direita.jogo.preco:
            no_atual.direita = self.rotacao_direita(no_atual.direita)
            return self.rotacao_esquerda(no_atual)

        return no_atual

    def mostrar_em_ordem(self):
        elementos = []
        self.mostrar_recursivo(self.raiz, elementos)
        return elementos

    def mostrar_recursivo(self, no, lista):
        if no:
            self.mostrar_recursivo(no.esquerda, lista)
            lista.append(no.jogo)
            self.mostrar_recursivo(no.direita, lista)

    def buscar_por_preco(self, preco_pesquisado):
        resultado = []
        self.buscar_por_preco_recursivo(self.raiz, preco_pesquisado, resultado)
        return resultado

    def buscar_por_preco_recursivo(self, no, preco_pesquisado, resultado):
        if no:
            if no.jogo.preco == preco_pesquisado:
                resultado.append(no.jogo)
            if preco_pesquisado < no.jogo.preco:
                self.buscar_por_preco_recursivo(no.esquerda, preco_pesquisado, resultado)
            if preco_pesquisado > no.jogo.preco:
                self.buscar_por_preco_recursivo(no.direita, preco_pesquisado, resultado)

    def busca_por_faixa_preco(self, preco_minimo, preco_maximo):
        resultado = []
        self.busca_por_faixa_preco_recursivo(self.raiz, preco_minimo, preco_maximo, resultado)
        return resultado

    def busca_por_faixa_preco_recursivo(self, no, preco_minimo, preco_maximo, resultado):
        if no:
            if preco_minimo <= no.jogo.preco <= preco_maximo:
                resultado.append(no.jogo)
            if preco_minimo < no.jogo.preco:
                self.busca_por_faixa_preco_recursivo(
                    no.esquerda, preco_minimo, preco_maximo, resultado)
            if preco_maximo > no.jogo.preco:
                self.busca_por_faixa_preco_recursivo(
                    no.direita, preco_minimo, preco_maximo, resultado)

class HashGeneros:
    def __init__(self):
        self.genero_jogos = {}

    def adicionar_jogo(self, jogo):
        # Para cada gênero no jogo, adicione o jogo à lista correspondente
        for genero in jogo.generos:
            if genero in self.genero_jogos:
                self.genero_jogos[genero].append(jogo)
            else:
                self.genero_jogos[genero] = [jogo]

    def jogos_no_genero(self, genero):
        return self.genero_jogos.get(genero, [])

    def listar_generos(self):
        return list(self.genero_jogos.keys())


class MotorBuscaJogos(ArvoreJogos, HashGeneros):
    def __init__(self):
        self.catalogo_jogos = ArvoreJogos()
        self.generos = HashGeneros()


class GeradorJogos:
    def __init__(self):
        self.titulos = [
            "The Witcher 3", "Red Dead Redemption 2", "Minecraft", "Cyberpunk 2077",
            "The Legend of Zelda: Breath of the Wild", "Grand Theft Auto V", "Fallout 4",
            "Dark Souls III", "The Elder Scrolls V: Skyrim", "Call of Duty: Warzone",
            "FIFA 22", "Assassin's Creed Valhalla", "Bioshock Infinite", "The Last of Us",
            "Borderlands 3", "Hollow Knight", "Doom Eternal", "Sekiro: Shadows Die Twice",
            "Rocket League", "Among Us", "Overwatch", "Mortal Kombat 11", "Rainbow Six Siege",
            "Terraria", "Stardew Valley", "Cuphead", "Dead by Daylight", "The Sims 4",
            "Mafia: Definitive Edition", "Subnautica", "Halo Infinite", "Halo: The Master Chief Collection",
            "Resident Evil 2", "Resident Evil 5", "Resident Evil 6", "Resident Evil 7",
            "Formula 1", "Need for Speed Heat", "Forza Horizon 5", "Forza Horizon 4",
            "Forza Horizon 3", "Forza Horizon 2", "Forza Horizon", "Forza Motorsport",
            "Call of Duty: Black Ops Cold War", "Call of Duty 2", "Call of Duty 3",
            "Call of Duty: Black Ops", "Call of Duty: Modern Warfare",
            "Call of Duty: War at war", "Call of Duty: Modern Warfare 1",
            "Counter-Strike: Global Offensive", "Counter-Strike: Source",
            "Counter-Strike 2", "Counter-Strike 1.6",
        ]

        self.desenvolvedores = [
            "CD Projekt Red", "Rockstar Games", "Mojang",
            "Nintendo", "Bethesda Game Studios", "FromSoftware", "Bethesda Game Studios",
            "Bethesda Game Studios", "Infinity Ward", "EA Sports", "Ubisoft", "2K Games",
            "Naughty Dog", "Gearbox Software", "Team Cherry", "id Software", "FromSoftware",
            "Psyonix", "InnerSloth", "Blizzard Entertainment", "NetherRealm Studios",
            "Ubisoft", "Re-Logic", "ConcernedApe", "Studio MDHR", "Behaviour Interactive",
            "Maxis", "Hangar 13", "Unknown Worlds Entertainment", "Insomniac Games",
        ]

        self.generos = [
            ["RPG", "Ação"], ["Ação", "Aventura"], ["Sobrevivência", "Construção"], ["RPG", "Ação"],
            ["Aventura", "RPG"], ["Ação", "Mundo Aberto"], ["RPG", "Pós-apocalíptico"], ["RPG", "Mundo Aberto"],
            ["RPG", "Ação", "Mundo Aberto"], ["Ação", "FPS"], ["Esportes", "Futebol"],
            ["Ação", "Aventura", "Vikings"], ["FPS", "Aventura"], ["Ação", "História"],
            ["Ação", "RPG", "FPS"], ["Ação", "Plataforma", "Cooperativo"], ["FPS", "Ação"],
            ["Ação", "Aventura", "Samurais"], ["Esportes", "Carros"], ["Ação", "Mistério", "Cooperativo"], ["FPS", "Ação"],
            ["Ação", "Aventura", "FPS", "Cooperativo"], ["FPS", "Estratégia", "Cooperativo"],
            ["Sobrevivência", "Aventura", "Construção"], ["Simulação", "Construção", "Vida no Campo"],
            ["Ação", "Plataforma"], ["Horror", "Assimétrico", "Cooperativo"], ["Simulação", "Vida Virtual"],
            ["Ação", "Aventura", "Máfia"], ["Sobrevivência", "Exploração"]
        ]

    def gerar_jogo(self, jogo_id):
        titulo = random.choice(self.titulos)
        desenvolvedor = random.choice(self.desenvolvedores)
        preco = round(random.uniform(10.0, 60.0), 2)  # Preço entre 10.0 e 60.0
        genero = random.choice(self.generos)

        return Jogo(jogo_id, titulo, desenvolvedor, preco, genero)

motor_busca = MotorBuscaJogos()
gerador = GeradorJogos()
quantidade_de_jogos = 15
jogos_gerados = []

for jogo_id in range(1, quantidade_de_jogos + 1):
    novo_jogo = gerador.gerar_jogo(jogo_id)
    jogos_gerados.append(novo_jogo)

for jogo in jogos_gerados:
    motor_busca.catalogo_jogos.inserir(jogo)
    motor_busca.generos.adicionar_jogo(jogo)

# PySimpleGUI Interface
layout = [
    [sg.Text('Trabalho de Classificação e Pesquisa de Dados', font=('Arial', 15, "bold"))],
    [sg.Text('Menu:')],
    [sg.Button('Listar todos os jogos')],
    [sg.Button('Listar jogos em ordem de preço')],
    [sg.Button('Pesquisar jogos por gênero')],
    [sg.Button('Pesquisar jogos por preço')],
    [sg.Button('Pesquisar jogos por intervalo de preço')],
    [sg.Button('Sair')]
]

window = sg.Window('Motor de Busca de Jogos', layout, size=(600, 350))

while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED or event == 'Sair':
        break

    if event == 'Listar todos os jogos':
        sg.Titlebar('Listar todos os jogos')
        todos_os_jogos = motor_busca.catalogo_jogos.mostrar_em_ordem()
        msg = '\n'.join([f'Título: {jogo.titulo}, Preço: {jogo.preco}, Desenvolvedor: {jogo.desenvolvedor}' for jogo in todos_os_jogos])
        sg.popup_ok(f'Todos os jogos:\n\n{msg}' + '\n\n' + 'Total de jogos: ' + str(len(todos_os_jogos)))

    if event == 'Listar jogos em ordem de preço':
        jogos_em_ordem = motor_busca.catalogo_jogos.mostrar_em_ordem()
        
        msg = '\n'.join([f"Título: {jogo.titulo}, Preço: {jogo.preco}\n" for jogo in jogos_em_ordem])
        sg.popup_ok(f'Jogos em ordem de preço:\n\n{msg}')
    
    elif event == 'Pesquisar jogos por gênero':
        generos = motor_busca.generos.listar_generos()
        genero_escolhido = sg.popup_get_text('Escolha um gênero:', generos)
        
        if genero_escolhido:
            genero_escolhido = genero_escolhido.split(',')
            genero_escolhido = [genre.strip() for genre in genero_escolhido]
            jogos_por_genero = motor_busca.generos.jogos_no_genero(genero_escolhido[0])
            if jogos_por_genero:
                sg.popup_ok(f'Jogos do gênero "{genero_escolhido[0]}":\n\n{", ".join([jogo.titulo for jogo in jogos_por_genero])}')
            else:
                sg.popup_ok(f'Nenhum jogo encontrado do gênero "{genero_escolhido[0]}".')
    
    elif event == 'Pesquisar jogos por preço':
        preco_pesquisado = sg.popup_get_text('Digite o valor a ser pesquisado:')
        if preco_pesquisado:
            preco_pesquisado = float(preco_pesquisado)
            resultados = motor_busca.catalogo_jogos.buscar_por_preco(preco_pesquisado)
            if resultados:
                sg.popup_ok(f'Jogos com preço de {preco_pesquisado}:\n\n{", ".join([jogo.titulo for jogo in resultados])}')
            else:
                sg.popup_ok(f'Nenhum jogo encontrado com preço de {preco_pesquisado}.')
    
    elif event == 'Pesquisar jogos por intervalo de preço':
        preco_minimo = sg.popup_get_text('Digite o valor mínimo:')
        preco_maximo = sg.popup_get_text('Digite o valor máximo:')
        if preco_minimo and preco_maximo:
            preco_minimo = float(preco_minimo)
            preco_maximo = float(preco_maximo)
            resultados = motor_busca.catalogo_jogos.busca_por_faixa_preco(preco_minimo, preco_maximo)
            if resultados:
                sg.popup_ok(f'Jogos no intervalo de preço de {preco_minimo} a {preco_maximo}:\n\n{", ".join([jogo.titulo for jogo in resultados])}')
            else:
                sg.popup_ok('Nenhum jogo encontrado no intervalo de preço.')

window.close()
