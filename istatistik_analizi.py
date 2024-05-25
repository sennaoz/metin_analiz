import nltk
from collections import Counter

def metin_istatistikleri(metin):
    """
    Verilen metin içindeki istatistikleri çıkarır.

    Args:
    - metin (str): Analiz edilecek metin.

    Returns:
    - dict: Metin içindeki istatistikler.
    """
    # Metni cümlelere böl
    cumleler = nltk.sent_tokenize(metin)
    cumle_sayisi = len(cumleler)

    # Metni kelimelere böl
    kelimeler = nltk.word_tokenize(metin)
    kelime_sayisi = len(kelimeler)

    # Stop kelimeleri ve noktalama işaretlerini kaldır
    stop_words = set(nltk.corpus.stopwords.words('turkish'))
    kelimeler = [kelime.lower() for kelime in kelimeler if kelime.isalnum() and kelime.lower() not in stop_words]

    # En sık kullanılan kelimeleri bul
    kelime_frekanslari = Counter(kelimeler)
    en_sik_kelimeler = kelime_frekanslari.most_common(10)

    # Ortalama cümle uzunluğu
    kelime_sayilari = [len(nltk.word_tokenize(cumle)) for cumle in cumleler]
    ortalama_cumle_uzunlugu = sum(kelime_sayilari) / cumle_sayisi

    # İstatistikleri döndür
    istatistikler = {
        "cümle sayısı": cumle_sayisi,
        "kelime sayısı": kelime_sayisi,
        "en sık kullanılan kelimeler": en_sik_kelimeler,
        "ortalama cümle uzunluğu": ortalama_cumle_uzunlugu
    }

    return istatistikler
