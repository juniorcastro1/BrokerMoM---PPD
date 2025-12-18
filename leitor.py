import pika
import sys
import json
import time

def iniciar_leitor(arquivo, modo, palavras_chave):
    # Conexão o Rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declara a fila de tarefas 
    channel.queue_declare(queue='fila_linhas', durable=True)

    print(f"[*] Leitor de linhas {modo} iniciado. Lendo {arquivo}...")

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for index, linha in enumerate(f):
                processar = False
                
                if modo == 'par' and index % 2 == 0:
                    processar = True
                elif modo == 'impar' and index % 2 != 0:
                    processar = True

                if processar:
                    mensagem = {
                        'linha': linha.strip(),
                        'palavras_chave': palavras_chave,
                        'numero_linha': index + 1
                    }
                    
                    # Publica na Fila (Produtor)
                    channel.basic_publish(
                        exchange='',
                        routing_key='fila_linhas',
                        body=json.dumps(mensagem),
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # Torna a mensagem persistente
                        ))
                    # Pequeno sleep para não entupir a fila instantaneamente e podermos ver o fluxo
                    time.sleep(0.01) 

        print(f"[x] Leitura {modo} finalizada.")

    except FileNotFoundError:
        print(f"Erro: Arquivo {arquivo} não encontrado.")
    finally:
        connection.close()

if __name__ == "__main__":
    # Argumentos via linha de comando
    if len(sys.argv) < 4:
        print("Uso: python leitor.py <arquivo> <modo> <palavra1,palavra2...>")
    else:
        arq = sys.argv[1]
        mod = sys.argv[2]
        keywords = sys.argv[3].split(',')
        iniciar_leitor(arq, mod, keywords)