import os
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

app = FastAPI(title="AI CV Analiz Sistemi - FastAPI & Bootstrap 5")

# --- MODÜL FONKSİYONLARI ---

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """PDF baytlarından metin çıkarır."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF okunamadı: {str(e)}")

def calculate_ats_score(cv_text: str, jd_text: str) -> float:
    """TF-IDF ve Cosine Similarity ile ATS uyumluluk skoru hesaplar."""
    if not cv_text.strip() or not jd_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([cv_text, jd_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(similarity) * 100, 2)

def get_ai_suggestions(cv_text: str, jd_text: str) -> str:
    """Ollama (Yerel LLM) üzerinden AI önerileri ve eksik analizi alır."""
    prompt = f"""
    Aşağıdaki CV ile İş İlanını karşılaştır ve profesyonel bir kariyer koçu gibi detaylı analiz yap:
    1. CV'deki eksik yetkinlikleri ve becerileri net maddeler halinde listele.
    2. Adayın işe kabul şansını artırmak için pratik, uygulanabilir stratejik öneriler ver.
    
    İŞ İLANI:
    {jd_text}
    
    CV:
    {cv_text}
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        #"model": "phi3",  # İsterseniz llama3 de yapabilirsiniz
        #"model": "llama3:latest",
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "Yapay zeka yanıt döndüremedi.")
        else:
            return "Ollama sunucu hatası! Ollama servisinin açık olduğundan emin olun."
    except Exception as e:
        return f"Ollama bağlantı kurulamadı ({str(e)}). Lütfen terminalde 'ollama serve' komutunun çalıştığını kontrol edin."


# --- FRONTEND (HTML / CSS / Bootstrap 5 / Modern UI) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Destekli Akıllı CV & ATS Analiz Sistemi</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-border: rgba(255, 255, 255, 0.1);
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg-gradient);
            color: #f8fafc;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .glass-panel {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 1.25rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .gradient-text {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .btn-custom-gradient {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            border: none;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .btn-custom-gradient:hover {
            opacity: 0.9;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(168, 85, 247, 0.4);
            color: white;
        }

        .form-control, .form-control:focus {
            background-color: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #f8fafc;
            border-radius: 0.75rem;
        }
        
        .form-control:focus {
            border-color: #818cf8;
            box-shadow: 0 0 0 0.25rem rgba(129, 140, 248, 0.25);
        }

        .score-circle {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            background: conic-gradient(#818cf8 var(--progress, 0deg), rgba(255,255,255,0.05) 0deg);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            position: relative;
            box-shadow: 0 0 25px rgba(129, 140, 248, 0.2);
            transition: background 1s ease-in-out;
        }

        .score-circle::before {
            content: "";
            position: absolute;
            width: 106px;
            height: 106px;
            border-radius: 50%;
            background: #121829;
        }

        .score-number {
            position: relative;
            font-size: 1.8rem;
            font-weight: 800;
        }

        .ai-result-box {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            max-height: 480px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 1.7;
        }

        .loading-spinner {
            display: none;
        }
    </style>
</head>
<body>

    <div class="container py-5">
        <!-- Header -->
        <div class="row mb-5 text-center">
            <div class="col-lg-8 mx-auto">
                <div class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-3 py-2 rounded-pill mb-3 fw-semibold">
                    <i class="fa-solid fa-wand-magic-sparkles me-2"></i> %100 Yerel & Ücretsiz AI Motoru
                </div>
                <h1 class="display-5 fw-extrabold gradient-text mb-3">AI Destekli CV & ATS Analiz Sistemi</h1>
                <p class="text-secondary lead fs-6">Özgeçmişinizi yükleyin, hedef iş ilanıyla anlamsal eşleşmesini sağlayın ve Ollama yapay zeka desteğiyle eksiklerinizi anında keşfedin.</p>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="row g-4">
            <!-- Sol Panel: Girdiler -->
            <div class="col-lg-5">
                <div class="glass-panel p-4 h-100">
                    <h4 class="fw-bold mb-4 text-white"><i class="fa-solid fa-sliders me-2 text-info"></i> Veri Girişi</h4>
                    
                    <form id="analysisForm">
                        <!-- CV Yükleme -->
                        <div class="mb-4">
                            <label class="form-label fw-semibold text-light mb-2">CV Dosyası Seç (PDF)</label>
                            <input class="form-control" type="file" id="cvFile" accept=".pdf" required>
                        </div>

                        <!-- İş İlanı Metni -->
                        <div class="mb-4">
                            <label class="form-label fw-semibold text-light mb-2">İş İlanı (Job Description)</label>
                            <textarea class="form-control" id="jdText" rows="7" placeholder="İş ilanı metnini buraya yapıştırın..." required></textarea>
                        </div>

                        <!-- Buton -->
                        <button type="submit" id="submitBtn" class="btn btn-custom-gradient w-100 py-3 rounded-pill fw-bold shadow-lg">
                            <span id="btnText"><i class="fa-solid fa-bolt me-2"></i> Analizi Başlat</span>
                            <span id="btnSpinner" class="spinner-border spinner-border-sm loading-spinner ms-2" role="status" aria-hidden="true"></span>
                        </button>
                    </form>
                </div>
            </div>

            <!-- Sağ Panel: Sonuçlar -->
            <div class="col-lg-7">
                <div class="glass-panel p-4 h-100 d-flex flex-column">
                    <h4 class="fw-bold mb-4 text-white"><i class="fa-solid fa-chart-pie me-2 text-warning"></i> Analiz Sonuçları</h4>

                    <div class="row align-items-center mb-4">
                        <div class="col-md-5 text-center mb-3 mb-md-0">
                            <div class="score-circle mb-2" id="scoreCircle" style="--progress: 0deg;">
                                <span class="score-number gradient-text" id="scoreValue">-%</span>
                            </div>
                            <span class="text-secondary small fw-semibold">ATS Uyumluluk Skoru</span>
                        </div>
                        <div class="col-md-7">
                            <div id="scoreBadgeContainer" class="p-3 rounded-3 bg-dark bg-opacity-50 border border-secondary border-opacity-25">
                                <h6 class="text-info fw-bold mb-1"><i class="fa-solid fa-circle-info me-2"></i> Durum Özeti</h6>
                                <p id="scoreStatusText" class="text-secondary small mb-0">Henüz analiz yapılmadı. Lütfen sol taraftan CV yükleyip iş ilanı girin ve analizi başlatın.</p>
                            </div>
                        </div>
                    </div>

                    <!-- AI Önerileri -->
                    <div class="flex-grow-1 d-flex flex-column">
                        <label class="form-label fw-semibold text-light mb-2"><i class="fa-solid fa-robot me-2 text-success"></i> Yapay Zeka Önerileri & Eksik Analizi</label>
                        <div class="ai-result-box p-4 text-light flex-grow-1" id="aiResultContent">
                            <span class="text-muted fst-italic">Yapay zeka analiz raporu burada görüntülenecektir...</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript & AJAX -->
    <script>
        document.getElementById('analysisForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const cvFile = document.getElementById('cvFile').files[0];
            const jdText = document.getElementById('jdText').value;

            if (!cvFile || !jdText) {
                alert("Lütfen bir CV dosyası seçin ve iş ilanı metnini girin.");
                return;
            }

            const formData = new FormData();
            formData.append("cv_file", cvFile);
            formData.append("jd_text", jdText);

            // UI Yükleniyor Durumu
            const submitBtn = document.getElementById('submitBtn');
            const btnText = document.getElementById('btnText');
            const btnSpinner = document.getElementById('btnSpinner');
            
            submitBtn.disabled = true;
            btnText.innerText = "Yapay Zeka Analiz Ediyor...";
            btnSpinner.style.display = "inline-block";
            
            document.getElementById('aiResultContent').innerHTML = '<div class="text-center py-5 text-info"><div class="spinner-border mb-3" role="status"></div><p>PDF metni işleniyor ve Ollama modeli analiz gerçekleştiriyor, lütfen bekleyin...</p></div>';

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    // Skor güncelleme
                    const score = data.ats_score;
                    document.getElementById('scoreValueinnerText', document.getElementById('scoreValue').innerText = `%${score}`);
                    
                    // Grafik açı hesaplama (360 derece üzerinden)
                    const degrees = (score / 100) * 360;
                    document.getElementById('scoreCircle').style.setProperty('--progress', `${degrees}deg`);

                    // Durum metni ve renk ayarı
                    let statusHtml = "";
                    if (score >= 75) {
                        statusHtml = `<strong class="text-success">Harika Uyum!</strong> Bu CV hedef iş ilanıyla son derece uyumlu görünüyor.`;
                    } else if (score >= 50) {
                        statusHtml = `<strong class="text-warning">Orta Düzey Uyum.</strong> Bazı anahtar yetkinlikler eksik olabilir, detaylı önerileri inceleyin.`;
                    } else {
                        statusHtml = `<strong class="text-danger">Düşük Uyum.</strong> İlan gereksinimleri ile CV içeriği arasında farklar var.`;
                    }
                    document.getElementById('scoreStatusText').innerHTML = statusHtml;

                    // AI Önerileri
                    document.getElementById('aiResultContent').innerText = data.ai_suggestions;

                } else {
                    alert("Hata: " + (data.detail || "Bilinmeyen bir hata oluştu."));
                    document.getElementById('aiResultContent').innerHTML = '<span class="text-danger">Analiz başarısız oldu.</span>';
                }

            } catch (error) {
                alert("Bağlantı hatası: " + error);
                document.getElementById('aiResultContent').innerHTML = '<span class="text-danger">Sunucuya bağlanılamadı.</span>';
            } finally {
                submitBtn.disabled = false;
                btnText.innerHTML = '<i class="fa-solid fa-bolt me-2"></i> Analizi Başlat';
                btnSpinner.style.display = "none";
            }
        });
    </script>
</body>
</html>
"""

# --- FASTAPI ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE

@app.post("/analyze")
async def analyze(cv_file: UploadFile = File(...), jd_text: str = Form(...)):
    try:
        # 1. Dosya Okuma
        file_bytes = await cv_file.read()
        cv_text = extract_text_from_pdf_bytes(file_bytes)

        # 2. ATS Skoru Hesaplama
        ats_score = calculate_ats_score(cv_text, jd_text)

        # 3. Yapay Zeka Önerileri Alma (Ollama)
        ai_suggestions = get_ai_suggestions(cv_text, jd_text)

        return {
            "ats_score": ats_score,
            "ai_suggestions": ai_suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app_bootstrap:app", host="127.0.0.1", port=8000, reload=True)