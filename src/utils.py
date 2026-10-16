import re

def clean_text(text):
    """Metin içerisindeki fazla boşlukları ve gereksiz karakterleri temizler."""
    if not text:
        return ""
    # Birden fazla boşluk veya alt alta boş satırları düzenleme
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def format_score_color(score):
    """ATS puanına göre arayüzde renkli uyarı döndürmek için yardımcı fonksiyon."""
    if score >= 75:
        return "success"
    elif score >= 50:
        return "warning"
    else:
        return "error"