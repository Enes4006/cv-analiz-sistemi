import streamlit as st
from src.parser import extract_text_from_pdf
from src.matcher import calculate_ats_score
from src.analyzer import get_ai_suggestions

st.set_page_config(page_title="AI CV Analiz Sistemi", page_icon="📄", layout="wide")

st.title("🤖 Ücretsiz AI Destekli CV & ATS Analiz Sistemi")
st.markdown("OpenAI API maliyeti olmadan, tamamen yerel (Ollama + Hugging Face) çalışan akıllı analiz aracı.")

# Yan Menü / Form Alanları
with st.sidebar:
    st.header("Veri Girişi")
    uploaded_file = st.file_uploader("CV Yükle (PDF)", type=["pdf"])
    jd_text = st.text_area("İş İlanı Metnini Buraya Yapıştırın", height=200)
    
    analyze_btn = st.button("Analizi Başlat", type="primary")

if analyze_btn:
    if uploaded_file is not None and jd_text.strip() != "":
        with st.spinner("CV okunuyor ve yapay zeka tarafından analiz ediliyor..."):
            # 1. Metin Çıkarımı
            cv_text = extract_text_from_pdf(uploaded_file)
            
            # 2. ATS Skoru Hesaplama
            ats_score = calculate_ats_score(cv_text, jd_text)
            
            # 3. LLM Analizi
            ai_feedback = get_ai_suggestions(cv_text, jd_text)
            
        # Sonuçların Ekranı
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric(label="ATS Uyumluluk Puanı", value=f"%{ats_score}")
            if ats_score >= 75:
                st.success("Harika! Bu CV iş ilanıyla oldukça uyumlu.")
            elif ats_score >= 50:
                st.warning("Orta düzeyde uyum. Eksik anahtar kelimeler olabilir.")
            else:
                st.error("Uyum düşük. CV'yi ilana göre güncellemelisin.")
                
        with col2:
            st.subheader("💡 Yapay Zeka Önerileri & Eksik Analizi")
            st.write(ai_feedback)
            
    else:
        st.warning("Lütfen hem bir CV dosyası yükleyin hem de iş ilanı metnini girin.")