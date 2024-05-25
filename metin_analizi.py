import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# İlk kez çalıştırıldığında gerekli dosyaları indir

nltk.download('punkt')
nltk.download('stopwords')


def onemli_kelimeleri_cikar(metin, n=10):
    """
    Verilen metin içindeki en önemli kelimeleri çıkarır.

    Args:
    - metin (str): Analiz edilecek metin.
    - n (int): Çıkarılacak en önemli kelime sayısı. Varsayılan 10.

    Returns:
    - List[str]: En önemli kelimelerin listesi.
    """
    # Metni kelimelere böl
    kelimeler = nltk.word_tokenize(metin)

    # Stop kelimeleri ve noktalama işaretlerini kaldır
    stop_words = set(stopwords.words('turkish'))  # Türkçe stop kelimeleri
    kelimeler = [kelime for kelime in kelimeler if kelime.isalnum() and kelime.lower() not in stop_words]

    # TF-IDF vektörizer kullanarak önemli kelimeleri çıkar
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(kelimeler)])

    # TF-IDF skorlarına göre kelimeleri sırala
    tfidf_scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.sum(axis=0).tolist()[0])
    sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

    # En yüksek n skora sahip kelimeleri al
    onemli_kelimeler = [kelime for kelime, skor in sorted_scores[:n]]

    return onemli_kelimeler
