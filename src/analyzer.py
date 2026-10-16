import requests
import json

def get_ai_suggestions(cv_text, jd_text):
    prompt = f"""
    Aşağıdaki CV ile İş İlanını karşılaştır. 
    1. CV'deki eksik yetkinlikleri ve becerileri listele.
    2. Adayın işe kabul şansını artırmak için net ve pratik öneriler ver.
    
    İŞ İLANI:
    {jd_text}
    
    CV:
    {cv_text}
    """
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3", # Bilgisayarında yüklü olan model adı
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "AI yanıt döndüremedi.")
        else:
            return "Ollama bağlantı hatası! Ollama'nın açık olduğundan emin ol."
    except Exception as e:
        return f"Bağlantı kurulamadı: {str(e)}. Ollama servisinin çalıştığını kontrol et (ollama run llama3)."