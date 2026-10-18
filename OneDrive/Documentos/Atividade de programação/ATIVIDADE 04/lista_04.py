"""
LISTA 2 | Estudo dirigido: Relacionamentos entre objetos.

Nome: Alex da Costa Campos

Este e o arquivo onde voce trabalha. Siga o roteiro do documento da
Lista 4, etapa por etapa. Ao terminar cada etapa:

    1. abra o arquivo conferir.py e mude a linha ETAPA;
    2. rode conferir.py
    3. so siga em frente quando todos os testes derem OK.

CENARIO
    Uma companhia aerea. Passageiros fazem reservas; cada reserva pode
    ter um assento; cada voo nasce com os seus assentos e recebe uma
    tripulacao que tambem trabalha em outros voos.
"""


# ======================================================================
# Passageiro
# ======================================================================
class Passageiro:
    def __init__(self, nome: str, documento: str) -> None:
        # ETAPA 1: guarde nome (sem espacos sobrando) e documento
        # ETAPA 2: comece com uma lista vazia de reservas
        self.nome = nome.strip()
        self.documento = documento
        self.reservas = []

    def identificacao(self) -> str:
        # ETAPA 1: devolva algo como "Ana Souza (111)"
        return f"{self.nome} ({self.documento})"

    # ETAPA 5: escreva __eq__ (passageiros iguais = mesmo documento)
    def __eq__(self, outro) -> bool:
        return self.documento == outro.documento

# ======================================================================
# Assento
# ======================================================================
class Assento:
    def __init__(self, codigo: str) -> None:
        # ETAPA 2: guarde o codigo; o assento comeca sem passageiro
        self.codigo = codigo
        self.passageiro = None

    def esta_livre(self) -> bool:
        # ETAPA 2
        return self.passageiro is None

    def ocupar(self, passageiro: Passageiro) -> bool:
        # ETAPA 2: recuse (avise e devolva False) se ja estiver ocupado;
        #          caso contrario, guarde o passageiro e devolva True
        if self.esta_livre():
            self.passageiro = passageiro
            return True
        return False

    def liberar(self) -> None:
        # ETAPA 2
        self.passageiro = None


# ======================================================================
# Reserva
# ======================================================================
class Reserva:
    def __init__(self, codigo: str, passageiro: Passageiro) -> None:
        # ETAPA 1: guarde o codigo e o OBJETO passageiro
        # ETAPA 2: comece sem assento, e avise o passageiro desta reserva
        self.codigo = codigo
        self.passageiro = passageiro
        self.assento = None
        passageiro.reservas.append(self)
    def marcar_assento(self, assento: Assento) -> bool:
        
        if assento.ocupar(self.passageiro):
            self.assento = assento
            return True
        return False

    def cartao(self) -> str:
        # ETAPA 1: devolva "R1 | Ana Souza (111)"
        # ETAPA 2: acrescente o assento: "R1 | Ana Souza (111) | 1A"
        #          ou "R1 | Ana Souza (111) | sem assento"
       
        if self.assento is None:
            lugar = "sem assento"
        else:
            lugar = self.assento.codigo
        return f"{self.codigo} | {self.passageiro.identificacao()} | {lugar}"
       
    # ETAPA 2: escreva marcar_assento(assento)

# ======================================================================
# Tripulante
# ======================================================================
class Tripulante:
    def __init__(self, nome: str, funcao: str) -> None:
        # ETAPA 3
        self.nome = nome
        self.funcao = funcao


# ======================================================================
# Voo
# ======================================================================
class Voo:
    def __init__(self, numero: str, origem: str, destino: str, fileiras: int = 5, letras: str = "ABCD") -> None:
        # ETAPA 3: guarde os dados e comece com a tripulacao vazia
        # ETAPA 4: acrescente os parametros fileiras=5 e letras="ABCD"
        #          e crie aqui dentro todos os assentos do voo
        # ETAPA 5: comece tambem com uma lista vazia de reservas
        self.numero = numero
        self.origem = origem
        self.destino = destino
        self.tripulacao = []
        self.letras = letras
        self.reservas = []

        self.assentos = []
        for fileira in range(1, fileiras + 1):
            for letra in letras:
                self.assentos.append(Assento(f"{fileira}{letra}"))



    def escalar(self, *tripulantes: Tripulante) -> None:
        # ETAPA 3: inclua o tripulante, sem repetir
        # ETAPA 5: troque para escalar(self, *tripulantes)
        for tripulante in tripulantes:
            if tripulante in self.tripulacao:
                print(f"{tripulante.nome} ja esta escalado(a) para o voo {self.numero}")
            else:
                self.tripulacao.append(tripulante)

    def dispensar(self, tripulante: Tripulante) -> None:
        # ETAPA 3
        if tripulante in self.tripulacao:
            self.tripulacao.remove(tripulante)

    def buscar_assento(self, codigo: str):
            for assento in self.assentos:
                if assento.codigo == codigo:
                    return assento
            return None
    def assentos_livres(self) -> int:
        livres = 0
        for assento in self.assentos:
            if assento.esta_livre():
                livres += 1
        return livres

    # ETAPA 5: escreva primeiro_livre(), reservar(...) e __len__
    def primeiro_livre(self):
        for assento in self.assentos:
            if assento.esta_livre():
                return assento
        return None

    def reservar(self, passageiro: Passageiro, codigo_assento=None):
        # (a) passageiro já tem reserva neste voo?
        for reserva in self.reservas:
            if reserva.passageiro == passageiro:
                print(f"{passageiro.nome} ja tem reserva no voo {self.numero}")
                return None

        # (b) escolher o assento
        if codigo_assento is None:
            assento = self.primeiro_livre()
        else:
            assento = self.buscar_assento(codigo_assento)

        # (c) assento inexistente ou ocupado (ou voo lotado)
        if assento is None or not assento.esta_livre():
            print(f"assento indisponivel no voo {self.numero}")
            return None

        # (d) criar a reserva
        codigo = f"{self.numero}-{len(self.reservas) + 1}"
        reserva = Reserva(codigo, passageiro)
        reserva.marcar_assento(assento)
        self.reservas.append(reserva)
        return reserva

    def __len__(self) -> int:
        return len(self.assentos) - self.assentos_livres()

    def mapa(self) -> str:
        n = len(self.letras)
        linhas = []                                   # ANTES do for, uma vez só
        for inicio in range(0, len(self.assentos), n):
            marcas = []                               # esta sim, nova a cada fileira
            for assento in self.assentos[inicio:inicio + n]:
                simbolo = "." if assento.esta_livre() else "X"
                marcas.append(f"{assento.codigo:>3} {simbolo}")
            linhas.append("  ".join(marcas))          # dentro do for de fora
        return "\n".join(linhas)                      # FORA do for, alinhado com "for"

    def resumo(self) -> str:
        return (f"Voo {self.numero} {self.origem}->{self.destino}: "
            f"{len(self)} ocupados, {self.assentos_livres()} livres, "
            f"{len(self.tripulacao)} tripulantes")
    
        # ETAPA 4: escreva buscar_assento(codigo) e assentos_livres()
    # ETAPA 5: escreva primeiro_livre(), reservar(...) e __len__
    # ETAPA 6: escreva mapa() e resumo()


# ======================================================================
# ETAPA 6: o programa final
# ======================================================================
if __name__ == "__main__":
    voo = Voo("AZ101", "NAT", "REC", fileiras=3)

    voo.escalar(Tripulante("Marta", "piloto"), Tripulante("Caio", "comissario"))

    ana = Passageiro("Ana Souza", "111")
    bia = Passageiro("Bia Lima", "222")
    davi = Passageiro("Davi Rocha", "333")

    r1 = voo.reservar(ana, "2C")        # a) primeiro no 2C
    r2 = voo.reservar(bia)              # b) segundo sem escolher assento
    voo.reservar(davi, "2C")            # c) recusado: 2C ocupado
    r3 = voo.reservar(davi, "3D")       #    depois no 3D
    voo.reservar(Passageiro("Ana S.", "111"))   # d) mesmo documento: recusado

    print(voo.resumo())
    print(voo.mapa())
    for reserva in (r1, r2, r3):
        print(reserva.cartao())  # monte aqui o voo descrito na etapa 6
