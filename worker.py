import pika
import json
import time

def processar_linha(ch, method, properties, body):
    data = json.loads(body)
    linha = data['linha']
    palavras_chave = data['palavras_chave']
    
    resultados = {}
    total_encontrado = 0
    
    for palavra in palavras_chave:
        count = linha.lower().count(palavra.lower())
        if count > 0:
            resultados[palavra] = count
            total_encontrado += count

    # Se encontrou algo, publica no Tópico de Resultados (Publisher)
    if total_encontrado > 0:
        mensagem_resultado = json.dumps(resultados)
        
        # Publica no Exchange do tipo 'fanout' (broadcast para o Dashboard)
        ch.basic_publish(exchange='topico_palavras', routing_key='', body=mensagem_resultado)
        print(f"[Worker] Processou linha {data['numero_linha']}: {resultados}")
    
    # Confirma para a fila que a tarefa foi feita (ACK)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 1. Garante que a fila de entrada existe
    channel.queue_declare(queue='fila_linhas', durable=True)
    
    # 2. Garante que o Tópico de saída existe
    channel.exchange_declare(exchange='topico_palavras', exchange_type='fanout')

    # Configuração para balanceamento de carga (só recebe 1 se terminar o anterior)
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue='fila_linhas', on_message_callback=processar_linha)

    print('[*] Worker aguardando tarefas. Para sair pressione CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrompido')