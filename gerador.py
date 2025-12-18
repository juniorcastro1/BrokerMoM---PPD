import random

# Configuração
NOME_ARQUIVO = "texto_gigante.txt"
TAMANHO_EM_MB = 50  # Mude para 100(Mb), 500(Mb)0 ou 1000(GB) se quiser estressar o sistema

# Palavras para o seu teste (para o Worker contar)
PALAVRAS = ["o", "a", "que", "de", "para", "sistema", "distribuido", 
            "computacao", "rabbit", "python", "teste", "mom", "arquitetura",
            "processamento", "paralelo", "nuvem", "docker", "mensagem"]

def gerar_arquivo():
    print(f"Gerando arquivo de {TAMANHO_EM_MB} MB...")
    
    bytes_alvo = TAMANHO_EM_MB * 1024 * 1024
    bytes_escritos = 0
    
    with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
        while bytes_escritos < bytes_alvo:
            # Gera uma linha aleatória com 10 a 20 palavras
            linha = " ".join(random.choices(PALAVRAS, k=random.randint(10, 20))) + "\n"
            f.write(linha)
            bytes_escritos += len(linha.encode('utf-8'))
            
    print(f"Sucesso! Arquivo '{NOME_ARQUIVO}' criado.")

if __name__ == "__main__":
    gerar_arquivo()