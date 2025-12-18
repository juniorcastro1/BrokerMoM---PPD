import pika
import json
import threading
import tkinter as tk
from tkinter import ttk

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard MoM - Contagem de Palavras")
        self.root.geometry("400x300")
        
        self.contadores = {} # Dicionario para guardar totais { "palavra": int }
        self.labels = {}     # Dicionario para guardar widgets da UI
        
        self.label_titulo = tk.Label(root, text="Monitoramento", font=("Arial", 14, "bold"))
        self.label_titulo.pack(pady=10)
        
        self.frame_stats = tk.Frame(root)
        self.frame_stats.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Inicia a thread do consumidor RabbitMQ
        self.rabbit_thread = threading.Thread(target=self.iniciar_consumidor, daemon=True)
        self.rabbit_thread.start()

    def atualizar_interface(self, palavra, qtd):
        # Atualiza a lógica de dados
        if palavra not in self.contadores:
            self.contadores[palavra] = 0
            # Cria UI para nova palavra
            frame = tk.Frame(self.frame_stats)
            frame.pack(fill=tk.X, pady=2)
            lbl_name = tk.Label(frame, text=f"{palavra}: ", width=15, anchor="e")
            lbl_name.pack(side=tk.LEFT)
            lbl_val = tk.Label(frame, text="0", font=("Arial", 10, "bold"), fg="blue")
            lbl_val.pack(side=tk.LEFT)
            self.labels[palavra] = lbl_val
            
        self.contadores[palavra] += qtd
        # Atualiza o texto do Label
        self.labels[palavra].config(text=str(self.contadores[palavra]))

    def callback_rabbit(self, ch, method, properties, body):
        data = json.loads(body)
        # O RabbitMQ roda em outra thread, precisamos usar after para mexer no Tkinter
        for palavra, qtd in data.items():
            self.root.after(0, self.atualizar_interface, palavra, qtd)

    def iniciar_consumidor(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declara o exchange (Tópico)
        channel.exchange_declare(exchange='topico_palavras', exchange_type='fanout')

        # Cria uma fila temporária exclusiva para este dashboard
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Liga a fila ao Tópico (Bind)
        channel.queue_bind(exchange='topico_palavras', queue=queue_name)

        print("[*] Dashboard esperando dados...")
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback_rabbit, auto_ack=True)
        channel.start_consuming()

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()