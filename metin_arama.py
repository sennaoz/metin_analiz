def kelime_ara(metin, kelime):
    """
    Verilen metin içinde belirli bir kelimeyi arar ve kelimenin geçtiği tüm pozisyonları döner.
    """
    pozisyonlar = []
    index = metin.find(kelime)

    while index != -1:
        pozisyonlar.append(index)
        index = metin.find(kelime, index + 1)

    return pozisyonlar
