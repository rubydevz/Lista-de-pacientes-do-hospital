# Com os dados de cor e numero do cartao do paciente e
# cria um ponteiro apontando para o proximo paciente da lista
class elemento:
    def __init__(self, cor, numero):
        self.cor = cor
        # Garante que o número é um inteiro para comparação correta
        self.numero = int(numero) 
        self.proximo = None

    # metodo para obter a representacao do objeto
    def __repr__(self):
        return f"({self.cor},{self.numero})"

# criacao da lista encadeada
class lista:
    def __init__(self):
        self.head = None

    # Metodo para representar a lista completa
    def __repr__(self):
        nodo = self.head
        nodos_str = []
        while nodo is not None:
            nodos_str.append(str(nodo)) 
            nodo = nodo.proximo
        nodos_str.append("None")
        return " -> ".join(nodos_str)

    # transforma o objeto em iteracionavel
    def __iter__(self):
        nodo = self.head
        while nodo is not None:
            yield nodo
            nodo = nodo.proximo

    # FUNÇÃO AMARELO: Insere 'A' por prioridade de MENOR NÚMERO, antes de qualquer 'V'
    def inserirComPrioridade(self, novo_nodo):
        
        # 1. Se a lista está vazia, o 'A' se torna o head
        if self.head is None:
            self.head = novo_nodo
            return

        # 2. Se o novo 'A' tem prioridade máxima (menor número OU head é 'V')
        if self.head.cor == 'V' or \
           (self.head.cor == 'A' and novo_nodo.numero < self.head.numero):
            novo_nodo.proximo = self.head
            self.head = novo_nodo
            return

        # 3. Percorrer para encontrar o último 'A' que tenha número menor que o novo
        nodo_anterior = self.head
        
        while nodo_anterior.proximo is not None and \
              nodo_anterior.proximo.cor == 'A' and \
              novo_nodo.numero >= nodo_anterior.proximo.numero:
            
            nodo_anterior = nodo_anterior.proximo
        
        # Insere o novo 'A'
        novo_nodo.proximo = nodo_anterior.proximo
        nodo_anterior.proximo = novo_nodo
        return

    # FUNÇÃO VERDE: Insere 'V' por prioridade de MENOR NÚMERO, após todos os 'A'
    def inserirSemPrioridade(self, novo_nodo):
        
        # 1. Encontrar o ponto de início da seção 'V'
        if self.head is None:
            self.head = novo_nodo
            return

        # Começa a busca pelo início (head)
        nodo_anterior = self.head
        
        # Primeiro, percorre todos os 'A'
        while nodo_anterior.proximo is not None and nodo_anterior.proximo.cor == 'A':
            nodo_anterior = nodo_anterior.proximo
        
        # Agora, 'nodo_anterior' é o último 'A' ou o 'head' se o 'head' for 'V' ou 'None'
        
        # Se 'nodo_anterior.proximo' for 'None' (lista só tem 'A's, ou 'V's, ou é vazia)
        if nodo_anterior.proximo is None and nodo_anterior.cor == 'V':
            # Caso especial: lista só tem 'V's, começa do head
            nodo_anterior = self.head

        elif nodo_anterior.proximo is not None and nodo_anterior.proximo.cor == 'V':
             # Pula o último 'A' para começar a busca de inserção no primeiro 'V'
             nodo_anterior = nodo_anterior.proximo
             
        # Se o novo 'V' tiver menor número que o primeiro 'V' (se houver V's)
        if nodo_anterior.cor == 'V' and novo_nodo.numero < nodo_anterior.numero:
            # Caso especial: Inserir V antes do primeiro V
            if nodo_anterior == self.head:
                novo_nodo.proximo = self.head
                self.head = novo_nodo
                return
            
            # Percorre a lista novamente para encontrar o nó ANTERIOR ao primeiro V
            temp_anterior = self.head
            while temp_anterior.proximo != nodo_anterior:
                 temp_anterior = temp_anterior.proximo
            
            novo_nodo.proximo = nodo_anterior
            temp_anterior.proximo = novo_nodo
            return

        # 2. Percorrer a seção 'V' para encontrar a posição correta de inserção
        
        # Se o último 'A' (ou head) for 'A', o próximo é o início da seção 'V'
        if nodo_anterior.proximo is not None and nodo_anterior.proximo.cor == 'V':
            # O loop de busca deve começar DO PRÓXIMO NÓ do último 'A'
            while nodo_anterior.proximo is not None and \
                  nodo_anterior.proximo.cor == 'V' and \
                  novo_nodo.numero >= nodo_anterior.proximo.numero:
                
                nodo_anterior = nodo_anterior.proximo

        # 3. Insere o novo 'V'
        novo_nodo.proximo = nodo_anterior.proximo
        nodo_anterior.proximo = novo_nodo
        return

    # a funcao atende o primeiro paciente da lista de espera e o retira
    def atenderPaciente(self):
        if self.head is None:
            print("A lista de espera está vazia.")
            return

        paciente_atendido = self.head
        self.head = self.head.proximo
        print(f"Atendendo paciente: {paciente_atendido}. Removido da lista.")
        return

# Programa e menu principal
inserir = lista()
print("Seja bem vindo ao programa do hospital")
print("Escolha uma das opcoes abaixo: ")
while True:
    print("\n")
    print("1 - Adicionar Paciente")
    print("2 - Imprimir lista de espera")
    print("3 - Atender paciente")
    print("4 - Sair")

    try:
        opcao = int(input("escolha uma opcao: "))
    except ValueError:
        print("Opção inválida. Por favor, digite um número.")
        continue
    
    if opcao == 1:
        # pergunta qual o grau do paciente e o atribui a sua lista equivalente
        cor = input("informe a cor do cartao (V/A): ").strip().upper()        
        if cor == "A" or cor == "V":
            # --- VALIDACAO DO NUMERO ---
            while True:
                numero_str = input("informe o numero do cartao (inteiro): ")
                try:
                    # Tenta converter para inteiro, garantindo que a entrada é válida
                    numero = int(numero_str)
                    # Sai do loop se a conversão for bem-sucedida
                    break 
                except ValueError:
                    # Mensagem de erro se a conversão falhar
                    print(" Entrada inválida. Por favor, digite um NÚMERO INTEIRO para o cartão.")
            # --- FIM DA VALIDACAO ---            
            # Agora 'numero' é garantidamente um inteiro
            if cor == "A":
                inserir.inserirComPrioridade(elemento(cor, numero))
                print(f"Paciente {cor}{numero} adicionado com alta prioridade.")         
            elif cor == "V":
                inserir.inserirSemPrioridade(elemento(cor, numero))
                print(f"Paciente {cor}{numero} adicionado com baixa prioridade.")
        else:
            print("Cor inválida. Use 'A' ou 'V'.")

    # imprime a lista de espera com o grau e numero do paciente
    elif opcao == 2:
        print("Lista de Espera: ", inserir)
    elif opcao == 3:
        # Chama a função para atender o primeiro da fila
        inserir.atenderPaciente()    
    elif opcao == 4:
        print("O hospital agradece sua preferencia\nencerrando programa...")
        break
    else:
        print("Selecione uma opcao valida!\n")
