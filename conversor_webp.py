"""Conversor de imagens para formato WebP com interface gráfica."""
import tkinter as tk
import threading
from tkinter import filedialog, ttk, scrolledtext
from pathlib import Path
from PIL import Image


class ConversorWebP:
    """Aplicação para conversão de imagens PNG/JPG para formato WebP."""

    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Imagens para WebP")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variáveis
        self.diretorio_selecionado = tk.StringVar()
        self.qualidade = tk.IntVar(value=80)
        self.convertendo = False

        # Configurar interface
        self.criar_interface()

    def criar_interface(self):
        """Cria e configura a interface gráfica da aplicação."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid para expansão
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Título
        titulo = ttk.Label(main_frame, text="Conversor de Imagens para WebP",
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Seleção de diretório
        ttk.Label(main_frame, text="Diretório:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.diretorio_selecionado, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(main_frame, text="Escolher Pasta", command=self.escolher_diretorio).grid(
            row=1, column=2, padx=5, pady=5)

        # Controle de qualidade
        ttk.Label(main_frame, text="Qualidade (0-100):").grid(row=2, column=0, sticky=tk.W, pady=5)
        qualidade_frame = ttk.Frame(main_frame)
        qualidade_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.qualidade_scale = ttk.Scale(qualidade_frame, from_=0, to=100,
                                         variable=self.qualidade, orient=tk.HORIZONTAL)
        self.qualidade_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.qualidade_label = ttk.Label(qualidade_frame, text="80", width=4)
        self.qualidade_label.pack(side=tk.LEFT, padx=(10, 0))

        # Atualizar label quando o slider muda
        self.qualidade_scale.config(command=self.atualizar_qualidade_label)

        # Botão de conversão
        self.btn_converter = ttk.Button(main_frame, text="🚀 Iniciar Conversão",
                                       command=self.iniciar_conversao, style='Accent.TButton')
        self.btn_converter.grid(row=3, column=0, columnspan=3, pady=20)

        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Área de log
        ttk.Label(main_frame, text="Log de Conversão:", font=('Arial', 10, 'bold')).grid(
            row=5, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))

        self.log_area = scrolledtext.ScrolledText(main_frame, height=15, width=70,
                                                  state='disabled', wrap=tk.WORD)
        self.log_area.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Configurar tag para cores no log
        self.log_area.tag_config('sucesso', foreground='green')
        self.log_area.tag_config('erro', foreground='red')
        self.log_area.tag_config('info', foreground='blue')
        self.log_area.tag_config('resumo', foreground='purple', font=('Arial', 10, 'bold'))

        # Expandir área de log
        main_frame.rowconfigure(6, weight=1)

    def atualizar_qualidade_label(self, value):
        """Atualiza o label com o valor da qualidade"""
        self.qualidade_label.config(text=str(int(float(value))))

    def escolher_diretorio(self):
        """Abre diálogo para escolher diretório"""
        diretorio = filedialog.askdirectory(title="Selecione a pasta com as imagens")
        if diretorio:
            self.diretorio_selecionado.set(diretorio)
            self.adicionar_log(f"📁 Pasta selecionada: {diretorio}", 'info')

    def adicionar_log(self, mensagem, tipo='normal'):
        """Adiciona mensagem ao log"""
        self.log_area.config(state='normal')
        if tipo != 'normal':
            self.log_area.insert(tk.END, mensagem + '\n', tipo)
        else:
            self.log_area.insert(tk.END, mensagem + '\n')
        self.log_area.see(tk.END)  # Auto-scroll
        self.log_area.config(state='disabled')
        self.root.update_idletasks()

    def iniciar_conversao(self):
        """Inicia o processo de conversão em uma thread separada"""
        if not self.diretorio_selecionado.get():
            self.adicionar_log("⚠️ Por favor, selecione um diretório primeiro!", 'erro')
            return

        if self.convertendo:
            self.adicionar_log("⚠️ Conversão já em andamento!", 'erro')
            return

        # Limpar log anterior
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')

        # Iniciar conversão em thread separada para não travar a interface
        self.convertendo = True
        self.btn_converter.config(state='disabled')
        self.progress.start(10)

        thread = threading.Thread(target=self.converter_imagens, daemon=True)
        thread.start()

    def converter_imagens(self):
        """Converte todas as imagens do diretório e subdiretórios para WebP"""
        try:
            path_origem = Path(self.diretorio_selecionado.get())
            extensoes_validas = {'.png', '.jpg', '.jpeg'}
            qualidade = self.qualidade.get()

            # Contadores
            convertidos = 0
            erros = 0
            total_economia = 0

            self.adicionar_log(f"🚀 Iniciando conversão em: {path_origem.resolve()}", 'info')
            self.adicionar_log(f"🎯 Qualidade configurada: {qualidade}%", 'info')
            self.adicionar_log("-" * 70)

            # Percorrer todas as pastas e subpastas recursivamente
            for arquivo in path_origem.rglob('*'):
                if arquivo.is_file() and arquivo.suffix.lower() in extensoes_validas:
                    try:
                        # Carrega a imagem
                        with Image.open(arquivo) as img:
                            # Define o nome de saída (ex: imagem.png -> imagem.webp)
                            arquivo_saida = arquivo.with_suffix('.webp')

                            # Conversão e Salvamento
                            # 'optimize=True' força o codificador a tentar achar a melhor estratégia
                            img.save(arquivo_saida, 'webp', quality=qualidade, optimize=True)

                            # Cálculo de eficiência
                            tamanho_orig = arquivo.stat().st_size
                            tamanho_novo = arquivo_saida.stat().st_size
                            economia = tamanho_orig - tamanho_novo

                            if economia > 0:
                                total_economia += economia
                                percentual = (economia / tamanho_orig) * 100
                                self.adicionar_log(
                                    f"✅ {arquivo.relative_to(path_origem)} → "
                                    f"{arquivo_saida.name} ({tamanho_novo/1024:.1f}KB, "
                                    f"economia: {percentual:.1f}%)",
                                    'sucesso'
                                )
                            else:
                                self.adicionar_log(
                                    f"✅ {arquivo.relative_to(path_origem)} → "
                                    f"{arquivo_saida.name} ({tamanho_novo/1024:.1f}KB)",
                                    'sucesso'
                                )

                            convertidos += 1

                    except (OSError, ValueError) as e:
                        self.adicionar_log(f"❌ Erro ao converter {arquivo.name}: {str(e)}", 'erro')
                        erros += 1

            # Resumo final
            self.adicionar_log("-" * 70)
            self.adicionar_log("🏁 Conversão finalizada!", 'resumo')
            self.adicionar_log(f"✅ {convertidos} imagens convertidas com sucesso", 'resumo')
            if erros > 0:
                self.adicionar_log(f"❌ {erros} erros encontrados", 'resumo')
            self.adicionar_log(
                f"💾 Espaço economizado: {total_economia / 1024 / 1024:.2f} MB",
                'resumo'
            )

        except (OSError, ValueError) as e:
            self.adicionar_log(f"❌ Erro fatal: {str(e)}", 'erro')

        finally:
            # Restaurar interface
            self.convertendo = False
            self.btn_converter.config(state='normal')
            self.progress.stop()


def main():
    """Função principal para executar a aplicação"""
    root = tk.Tk()
    ConversorWebP(root)
    root.mainloop()


if __name__ == "__main__":
    main()
