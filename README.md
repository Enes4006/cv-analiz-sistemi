# 🤖 AI Destekli Yerel CV & ATS Analiz Sistemi

Bu proje; harici, ücretli yapay zeka API'lerine (OpenAI vb.) ihtiyaç duymadan, **tamamen yerel (local) kaynaklarla** çalışan ve sıfır maliyetle geliştirilmiş bir **CV ve İş İlanı Eşleştirme (ATS) Sistemidir**. 

Kullanıcıların yükledikleri PDF formatındaki CV'leri hedef iş ilanlarıyla karşılaştırarak anlamsal uyumluluk puanı hesaplar ve yerel dil modelleri aracılığıyla detaylı eksik analizi ile kariyer önerileri sunar.

---

## 🚀 Temel Özellikler

- **100% Ücretsiz ve Çevrimdışı:** Bulut tabanlı hiçbir ücretli API kullanılmaz; verileriniz tamamen kendi bilgisayarınızda işlenir.
- **PDF Metin Çıkarıcı:** `pypdf` kütüphanesi ile PDF formatındaki özgeçmişleri akıllıca okur.
- **ATS Uyumluluk Puanı:** `scikit-learn` ve TF-IDF kullanarak CV ile iş ilanı arasındaki anlamsal benzerliği yüzde bazlı hesaplar.
- **Yapay Zeka Önerileri:** **Ollama** entegrasyonu (Llama 3, gemma 3b vb.) sayesinde adayın eksik yetkinliklerini tespit eder ve geliştirme tavsiyeleri verir.
- **Profesyonel Web Arayüzü:** **FastAPI** backend mimarisi ve şık, renkli **Bootstrap 5 (Glassmorphism & Gradient)** ön yüz tasarımıyla modern bir deneyim sunar.

---
