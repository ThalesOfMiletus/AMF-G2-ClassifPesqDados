import random
from random import randint

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
            self.mostrar_recursivo(no.direita, lista)
            lista.append(no.jogo)
            self.mostrar_recursivo(no.esquerda, lista)

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
            "Counter-Strike 2", "Counter-Strike 1.6", "Mass Effect: Legendary Edition", "Star Wars Jedi: Fallen Order",
            "The Elder Scrolls V: Skyrim Special Edition", "Cyberpunk 2077", "Assassin's Creed Odyssey",
            "The Witcher 2: Assassins of Kings", "Dragon Age: Inquisition", "Gears 5", "Ghost of Tsushima",
            "Persona 5", "Nier: Automata", "Divinity: Original Sin 2", "Monster Hunter: World",
            "Celeste", "Hades", "Undertale", "Disco Elysium",
            "Civilization VI", "Stellaris", "Cities: Skylines", "Europa Universalis IV",
            "SimCity", "Planet Zoo", "Microsoft Flight Simulator", "Elite Dangerous",
            "DOOM (1993)", "Quake III Arena", "Half-Life 2", "Team Fortress 2",
            "Diablo III", "Path of Exile", "Torchlight II", "Grim Dawn"
        ]

        self.desenvolvedores = [
            "CD Projekt Red", "Rockstar Games", "Mojang",
            "Nintendo", "Bethesda Game Studios", "FromSoftware", "Bethesda Game Studios",
            "Bethesda Game Studios", "Infinity Ward", "EA Sports", "Ubisoft", "2K Games",
            "Naughty Dog", "Gearbox Software", "Team Cherry", "id Software", "FromSoftware",
            "Psyonix", "InnerSloth", "Blizzard Entertainment", "NetherRealm Studios",
            "Ubisoft", "Re-Logic", "ConcernedApe", "Studio MDHR", "Behaviour Interactive",
            "Maxis", "Hangar 13", "Unknown Worlds Entertainment", "Insomniac Games",
            "Bioware", "Respawn Entertainment", "Capcom", "Ubisoft Quebec",
            "Obsidian Entertainment", "Sucker Punch Productions", "Atlus", "PlatinumGames",
            "Supergiant Games", "Undertale", "Za/Um",
            "Firaxis Games", "Paradox Interactive", "Colossal Order", "Frontier Developments",
            "id Software", "Valve", "Riot Games", "Larian Studios",
            "Red Hook Studios", "Supergiant Games", "Toby Fox", "ZA/UM",
            "Firaxis Games", "Paradox Development Studio", "Colossal Order", "Frontier Developments",
            "Maxis", "Zoo Tycoon", "Microsoft", "Frontier Developments",
            "id Software", "id Software", "Valve", "Valve",
            "Blizzard Entertainment", "Grinding Gear Games", "Runic Games", "Crate Entertainment"
        ]

        self.generos = [
            ["Aventura"], ["RPG"], ["Plataforma"], ["Mundo Aberto"], ["Ficção Científica"],
            ["RPG", "Ação"], ["Ação", "Aventura"], ["Sobrevivência", "Construção"], ["RPG", "Ação"],
            ["Aventura", "RPG"], ["Ação", "Mundo Aberto"], ["RPG", "Pós-apocalíptico"], ["RPG", "Mundo Aberto"],
            ["RPG", "Ação", "Mundo Aberto"], ["Ação", "FPS"], ["Esportes", "Futebol"],
            ["Ação", "Aventura", "Vikings"], ["FPS", "Aventura"], ["Ação", "História"],
            ["Ação", "RPG", "FPS"], ["Ação", "Plataforma", "Cooperativo"], ["FPS", "Ação"],
            ["Ação", "Aventura", "Samurais"], ["Esportes", "Carros"], ["Ação", "Mistério", "Cooperativo"], ["FPS", "Ação"],
            ["Ação", "Aventura", "FPS", "Cooperativo"], ["FPS", "Estratégia", "Cooperativo"],
            ["Sobrevivência", "Aventura", "Construção"], ["Simulação", "Construção", "Vida no Campo"],
            ["Ação", "Plataforma"], ["Horror", "Assimétrico", "Cooperativo"], ["Simulação", "Vida Virtual"],
            ["Ação", "Aventura", "Máfia"], ["Sobrevivência", "Exploração"],
            ["RPG", "Ação", "Espaço"], ["Aventura", "Ficção Científica"], ["RPG", "Estratégia", "Cooperativo"], ["RPG", "Caça a Monstros"],
            ["Indie", "Aventura", "Pixel Art"], ["Indie", "Roguelike", "Ação"], ["Indie", "RPG", "Narrativo"], ["RPG", "Detetive"],
            ["Estratégia", "Civilização"], ["Estratégia", "Espaço"], ["Simulação", "Cidade"], ["Estratégia", "Histórico"],
            ["Simulação", "Construção de Parque", "Tycoon"], ["Simulação", "Zoológico"], ["Simulação", "Voo"], ["Simulação", "Espaço"],
            ["FPS", "Clássico"], ["FPS", "Arena"], ["FPS", "Ação", "Aventura"], ["FPS", "Multijogador"],
            ["RPG", "Ação", "Aventura"], ["RPG", "Ação", "Hack and Slash"], ["RPG", "Estratégia", "Cooperativo"], ["RPG", "Ação", "Caça a Monstros"]
        ]

    def gerar_jogo(self, jogo_id):
        titulo = random.choice(self.titulos)
        desenvolvedor = random.choice(self.desenvolvedores)
        preco = randint(10, 90) # Use uniform para obter números decimais
        genero = random.choice(self.generos)

        return Jogo(jogo_id, titulo, desenvolvedor, preco, genero)

motor_busca = MotorBuscaJogos()
gerador = GeradorJogos()
quantidade_de_jogos = 100
jogos_gerados = []

for jogo_id in range(1, quantidade_de_jogos + 1):
    novo_jogo = gerador.gerar_jogo(jogo_id)
    jogos_gerados.append(novo_jogo)
    motor_busca.catalogo_jogos.inserir(novo_jogo)
    motor_busca.generos.adicionar_jogo(novo_jogo)

# Se o número de jogos gerados for menor que a quantidade desejada, continua gerando jogos
while len(jogos_gerados) < quantidade_de_jogos:
    jogo_id += 1
    novo_jogo = gerador.gerar_jogo(jogo_id)
    jogos_gerados.append(novo_jogo)
    motor_busca.catalogo_jogos.inserir(novo_jogo)
    motor_busca.generos.adicionar_jogo(novo_jogo)

while True:
    print("\nMenu:")
    print("1. Listar todos os jogos")
    print("2. Listar jogos em ordem de preço")
    print("3. Pesquisar jogos por gênero")
    print("4. Pesquisar jogos por preço")
    print("5. Pesquisar jogos por intervalo de preço")
    print("6. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        todos_os_jogos = motor_busca.catalogo_jogos.mostrar_em_ordem()
        for jogo in todos_os_jogos:
            print(f'\nJogo ID: {jogo.jogo_id}, Título: {jogo.titulo}, Preço: {jogo.preco}, Desenvolvedor: {jogo.desenvolvedor}')
        print('Total de jogos:', quantidade_de_jogos)

    elif escolha == '2':
        jogos_em_ordem = motor_busca.catalogo_jogos.mostrar_em_ordem()
        for jogo in jogos_em_ordem:
            print(f"Título: {jogo.titulo}, Preço: {jogo.preco}")
    
    elif escolha == '3':
        generos = motor_busca.generos.listar_generos()
        print("Escolha um gênero:")
        for i, genero in enumerate(generos, start=1):
            print(f"{i}. {genero}")
        escolha_genero = int(input())
        genero_escolhido = generos[escolha_genero - 1]
        jogos_por_genero = motor_busca.generos.jogos_no_genero(genero_escolhido)
        if jogos_por_genero:
            print(f'Jogos do gênero "{genero_escolhido}": {", ".join([jogo.titulo for jogo in jogos_por_genero])}')
        else:
            print(f'Nenhum jogo encontrado do gênero "{genero_escolhido}".')

    elif escolha == '4':
        preco_pesquisado = float(input('Digite o valor a ser pesquisado: '))
        resultados = motor_busca.catalogo_jogos.buscar_por_preco(preco_pesquisado)
        if resultados:
            print(f'Jogos com preço de {preco_pesquisado}: {", ".join([jogo.titulo for jogo in resultados])}')
        else:
            print(f'Nenhum jogo encontrado com preço de {preco_pesquisado}.')

    elif escolha == '5':
        preco_minimo = float(input('Digite o valor mínimo: '))
        preco_maximo = float(input('Digite o valor máximo: '))
        resultados = motor_busca.catalogo_jogos.busca_por_faixa_preco(preco_minimo, preco_maximo)
        if resultados:
            print(f'Jogos no intervalo de preço de {preco_minimo} a {preco_maximo}: {", ".join([jogo.titulo for jogo in resultados])}')
        else:
            print('Nenhum jogo encontrado no intervalo de preço.')

    elif escolha == '6':
        break
    else:
        print("Escolha inválida. Tente novamente.")
