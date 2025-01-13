import random
import spacy

# Spacy 모델 로드
nlp = spacy.load("en_core_web_lg")

#################### cc hard negative ####################
def shuffle_all_words(text):
    words = text.split()
    original = words[:]
    random.shuffle(words)
    if words == original and len(words) > 1:  # 원본과 동일한 경우
        # 첫 번째와 두 번째 단어 순서만 바꿈
        words[0], words[1] = words[1], words[0]
    return " ".join(words)


def shuffle_nouns_adjs(text):
    doc = nlp(text)
    
    # 명사(NOUN)와 형용사(ADJ)를 분리
    nouns_adjs = [(token.text, token.pos_) for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    original_nouns_adjs = nouns_adjs[:]
    
    # 명사와 형용사끼리만 섞기
    random.shuffle(nouns_adjs)
    if nouns_adjs == original_nouns_adjs:  # 원본과 동일하면 앞부분만 교환
        if len(nouns_adjs) > 1:
            nouns_adjs[0], nouns_adjs[1] = nouns_adjs[1], nouns_adjs[0]
    
    # 결과 텍스트 생성
    result = []
    noun_adj_index = 0
    for token in doc:
        if token.pos_ in ["NOUN", "ADJ"]:
            # 섞인 명사 또는 형용사 삽입
            result.append(nouns_adjs[noun_adj_index][0])
            noun_adj_index += 1
        else:
            # 문법적으로 다른 단어는 그대로 삽입
            result.append(token.text)
    
    return " ".join(result)


def shuffle_except_nouns_adjs(text):
    doc = nlp(text)
    others = [token.text for token in doc if token.pos_ not in ["NOUN", "ADJ"]]
    original = others[:]
    random.shuffle(others)
    if others == original and len(others) > 1:  # 원본과 같으면 앞부분 두 개만 섞기
        others[0], others[1] = others[1], others[0]
    
    result = []
    for token in doc:
        if token.pos_ in ["NOUN", "ADJ"]:
            result.append(token.text)
        else:
            result.append(others.pop(0))
    return " ".join(result)


def shuffle_trigrams(text):
    words = text.split()
    trigrams = [words[i:i + 3] for i in range(0, len(words), 3)]

    # 마지막 남은 단어들 처리
    if len(words) % 3 != 0:
        remainder = trigrams.pop()  # 남은 단어를 추출
        trigrams.append(remainder)  # 남은 단어를 마지막 삼중어 그룹으로 간주

    original = trigrams[:]
    random.shuffle(trigrams)
    if trigrams == original and len(trigrams) > 1:  # 원본과 동일한 경우
        # 첫 번째와 두 번째 청크 순서만 바꿈
        trigrams[0], trigrams[1] = trigrams[1], trigrams[0]

    shuffled = [word for trigram in trigrams for word in trigram]
    return " ".join(shuffled)


def shuffle_within_trigrams(text):
    words = text.split()
    trigrams = [words[i:i + 3] for i in range(0, len(words), 3)]

    # 마지막 남은 단어들 처리
    if len(words) % 3 != 0:
        remainder = trigrams.pop()  # 남은 단어를 추출
        trigrams.append(remainder)  # 남은 단어를 마지막 삼중어 그룹으로 간주

    original = [trigram[:] for trigram in trigrams]
    for trigram in trigrams:
        random.shuffle(trigram)
    if trigrams == original and len(trigrams) > 1:  # 원본과 동일한 경우
        # 첫 번째와 두 번째 청크 순서만 바꿈
        trigrams[0], trigrams[1] = trigrams[1], trigrams[0]

    shuffled = [word for trigram in trigrams for word in trigram]
    return " ".join(shuffled)

#################### ocr hard negative ####################

def duplicate_random_word(text):
    words = list(text)  # 한 글자 단위로 처리
    index = random.randint(0, len(words) - 1)  # 중복할 위치 선택
    return "".join(words[:index] + [words[index]] + words[index:])  # 중복 삽입

###########################################################


cc_hard_negative_generators = {
    "shuffle_all_words": shuffle_all_words,
    "shuffle_nouns_adjs": shuffle_nouns_adjs,
    "shuffle_except_nouns_adjs": shuffle_except_nouns_adjs,
    "shuffle_trigrams": shuffle_trigrams,
    "shuffle_within_trigrams": shuffle_within_trigrams,
}


ocr_hard_negative_generators = {
    "duplicate_random_word": duplicate_random_word,
}
