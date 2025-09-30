import os
from better_profanity import profanity

# badwords.txt 경로 (같은 디렉토리에 있다고 가정)
BADWORDS_FILE = os.path.join(os.path.dirname(__file__), "badwords.txt")

# 기본 영어 비속어 로드
profanity.load_censor_words()

# 한국어 비속어 txt 로드
with open(BADWORDS_FILE, encoding="utf-8") as f:
    korean_badwords = [line.strip() for line in f if line.strip()]
    profanity.add_censor_words(korean_badwords)


def contains_profanity(text: str) -> bool:
    """비속어 포함 여부만 True/False 반환"""
    return profanity.contains_profanity(text)


def censor_text(text: str) -> str:
    """욕설을 ***로 치환"""
    return profanity.censor(text)
