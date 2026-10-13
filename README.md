# 🤖 AI Destekli Yerel CV & ATS Analiz Sistemi

Bu proje; harici, ücretli yapay zeka API'lerine (OpenAI vb.) ihtiyaç duymadan, **tamamen yerel (local) kaynaklarla** çalışan ve sıfır maliyetle geliştirilmiş bir **CV ve İş İlanı Eşleştirme (ATS) Sistemidir**. 

Kullanıcıların yükledikleri PDF formatındaki farklı farklı CV'leri hedef iş ilanlarıyla karşılaştırarak anlamsal uyumluluk puanı hesaplar ve yerel dil modelleri aracılığıyla detaylı eksik analizi ile kariyer önerileri sunar.

Projede iş ilanına göre ATS uyumluluğu düşük farklı CV'ler kullanılmıştır.

---

## 🚀 Temel Özellikler

- **100% Ücretsiz ve Çevrimdışı:** Bulut tabanlı hiçbir ücretli API kullanılmaz; verileriniz tamamen kendi bilgisayarınızda işlenir.
- **PDF Metin Çıkarıcı:** `pypdf` kütüphanesi ile PDF formatındaki özgeçmişleri akıllıca okur.
- **ATS Uyumluluk Puanı:** `scikit-learn` ve TF-IDF kullanarak CV ile iş ilanı arasındaki anlamsal benzerliği yüzde bazlı hesaplar.
- **Yapay Zeka Önerileri:** **Ollama** entegrasyonu (Llama 3, gemma 3b vb.) sayesinde adayın eksik yetkinliklerini tespit eder ve geliştirme tavsiyeleri verir.
- **Profesyonel Web Arayüzü:** **FastAPI** backend mimarisi ve şık, renkli **Bootstrap 5 (Glassmorphism & Gradient)** ön yüz tasarımıyla modern bir deneyim sunar.
- **Masaüstü Uygulama Desteği:** İsteğe bağlı olarak **CustomTkinter** altyapısıyla tarayıcı bağımlılığı olmadan, yerel bir masaüstü yazılımı olarak da çalıştırılabilir.

---

<img width="1108" height="837" alt="image" src="https://github.com/user-attachments/assets/100e918e-acd9-490e-b94f-66b1272713d1" />

Masaüstü Uygulaması: Sistem; sol taraftaki PDF yükleme ve iş ilanı giriş paneli ile sağ taraftaki anlamsal ATS puanı ve Ollama yapay zeka önerileri ekranını tek bir modern sayfada buluşturur.


<img width="1917" height="1021" alt="image" src="https://github.com/user-attachments/assets/3ba8ed4b-f616-4aea-8966-130fe7eebd82" />

Web Arayüzü: FastAPI ve Bootstrap 5 ile geliştirilen, şık glassmorphism efektlerine ve gradient tasarıma sahip web arayüzü görünümü

