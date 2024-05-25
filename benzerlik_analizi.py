from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def metin_benzerligi(metin1, metin2):
    """
    İki metin arasındaki benzerlik derecesini hesaplar.

    Args:
    - metin1 (str): İlk metin.
    - metin2 (str): İkinci metin.

    Returns:
    - float: İki metin arasındaki benzerlik derecesi (0 ile 1 arasında).
    """
    # TF-IDF vektörizer kullanarak metinleri vektörize et
    vectorizer = TfidfVectorizer().fit_transform([metin1, metin2])
    vectors = vectorizer.toarray()

    # Kosinüs benzerliği hesapla
    benzerlik_derecesi = cosine_similarity(vectors)[0, 1]

    return benzerlik_derecesi
