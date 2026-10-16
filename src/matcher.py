from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats_score(cv_text, jd_text):
    if not cv_text.strip() or not jd_text.strip():
        return 0.0
        
    # Metinleri vektörlere dönüştür ve benzerlik hesapla
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([cv_text, jd_text])
    
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score = round(float(similarity) * 100, 2)
    return score