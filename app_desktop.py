import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from src.parser import extract_text_from_pdf
from src.matcher import calculate_ats_score
from src.analyzer import get_ai_suggestions

# Tema ayarları
ctk.set_appearance_mode("System")  # Sistem temasını takip et (Koyu/Açık)
ctk.set_default_color_theme("blue")

class CVAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Destekli Yerel CV & ATS Analiz Sistemi")
        self.geometry("900x650")
        self.minsize(800, 600)

        self.selected_file_path = ""

        # --- GRID DÜZENİ ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SOL PANEL (Girdiler) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="📄 CV Analiz Paneli", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # CV Seçme Butonu
        self.upload_btn = ctk.CTkButton(self.sidebar_frame, text="CV Seç (PDF)", command=self.load_pdf)
        self.upload_btn.grid(row=1, column=0, padx=20, pady=10)

        self.file_label = ctk.CTkLabel(self.sidebar_frame, text="Dosya seçilmedi", text_color="gray", wraplength=260)
        self.file_label.grid(row=2, column=0, padx=20, pady=5)

        # İş İlanı Başlığı
        self.jd_label = ctk.CTkLabel(self.sidebar_frame, text="İş İlanı Metni:", anchor="w")
        self.jd_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        # İş İlanı Metin Kutusu
        self.jd_textbox = ctk.CTkTextbox(self.sidebar_frame, height=220)
        self.jd_textbox.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        # Analiz Et Butonu
        self.analyze_btn = ctk.CTkButton(self.sidebar_frame, text="Analizi Başlat", fg_color="green", hover_color="darkgreen", command=self.start_analysis_thread)
        self.analyze_btn.grid(row=5, column=0, padx=20, pady=20)

        # --- SAĞ PANEL (Sonuçlar) ---
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=1)

        # Skor Alanı
        self.score_frame = ctk.CTkFrame(self.right_frame, height=80)
        self.score_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.score_frame.grid_columnconfigure(1, weight=1)

        self.score_title = ctk.CTkLabel(self.score_frame, text="ATS Uyumluluk Puanı:", font=ctk.CTkFont(size=16, weight="bold"))
        self.score_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.score_value = ctk.CTkLabel(self.score_frame, text="-%", font=ctk.CTkFont(size=24, weight="bold"), text_color="dodgerblue")
        self.score_value.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        # Yapay Zeka Önerileri Başlığı
        self.ai_title = ctk.CTkLabel(self.right_frame, text="💡 Yapay Zeka Önerileri & Eksik Analizi", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        self.ai_title.grid(row=1, column=0, sticky="w", pady=(0, 5))

        # AI Yanıt Metin Kutusu (Scrollable)
        self.ai_textbox = ctk.CTkTextbox(self.right_frame, wrap="word")
        self.ai_textbox.grid(row=2, column=0, sticky="nsew")
        self.ai_textbox.insert("0.0", "Analiz sonuçları burada görünecek...")
        self.ai_textbox.configure(state="disabled") # Kullanıcı doğrudan yazamasın

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Dosyaları", "*.pdf")])
        if file_path:
            self.selected_file_path = file_path
            file_name = file_path.split("/")[-1]
            self.file_label.configure(text=f"Seçilen: {file_name}", text_color="green")

    def start_analysis_thread(self):
        if not self.selected_file_path:
            messagebox.showwarning("Uyarı", "Lütfen önce bir CV (PDF) seçin!")
            return
        
        jd_text = self.jd_textbox.get("1.0", "end-1c").strip()
        if not jd_text:
            messagebox.showwarning("Uyarı", "Lütfen iş ilanı metnini girin!")
            return

        # Arayüz donmasın diye analizi arka plan iş parçacığına (thread) atıyoruz
        self.analyze_btn.configure(state="disabled", text="Analiz Ediliyor...")
        self.ai_textbox.configure(state="normal")
        self.ai_textbox.delete("1.0", "end")
        self.ai_textbox.insert("1.0", "CV okunuyor ve Ollama yapay zeka modeli analiz yapıyor, lütfen bekleyin...")
        self.ai_textbox.configure(state="disabled")

        threading.Thread(target=self.run_analysis, args=(jd_text,), daemon=True).start()

    def run_analysis(self, jd_text):
        try:
            # 1. Metin Çıkarımı
            with open(self.selected_file_path, "rb") as f:
                cv_text = extract_text_from_pdf(f)

            # 2. ATS Skoru
            ats_score = calculate_ats_score(cv_text, jd_text)

            # 3. AI Önerileri (Ollama)
            ai_feedback = get_ai_suggestions(cv_text, jd_text)

            # Sonuçları arayüze aktar (Ana thread üzerinden)
            self.after(0, lambda: self.update_ui(ats_score, ai_feedback))

        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def update_ui(self, score, feedback):
        self.score_value.configure(text=f"%{score}")
        if score >= 75:
            self.score_value.configure(text_color="green")
        elif score >= 50:
            self.score_value.configure(text_color="orange")
        else:
            self.score_value.configure(text_color="red")

        self.ai_textbox.configure(state="normal")
        self.ai_textbox.delete("1.0", "end")
        self.ai_textbox.insert("1.0", feedback)
        self.ai_textbox.configure(state="disabled")

        self.analyze_btn.configure(state="normal", text="Analizi Başlat")

    def show_error(self, err_msg):
        messagebox.showerror("Hata", f"İşlem sırasında bir hata oluştu:\n{err_msg}")
        self.analyze_btn.configure(state="normal", text="Analizi Başlat")

if __name__ == "__main__":
    app = CVAnalyzerApp()
    app.mainloop()