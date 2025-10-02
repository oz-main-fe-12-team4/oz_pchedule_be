import os
from better_profanity import profanity

# badwords.txt 경로 (같은 디렉토리에 있다고 가정)
BADWORDS_FILE = os.path.join(os.path.dirname(__file__), "badwords.txt")

# 영어 욕설 로드
profanity.load_censor_words()

# 한글 욕설 로드 (메모리에 저장)
with open(BADWORDS_FILE, encoding="utf-8-sig") as f:
    KOREAN_BADWORDS = [line.strip() for line in f if line.strip()]


def contains_profanity(text: str) -> bool:
    # 영어 → better-profanity 그대로
    if profanity.contains_profanity(text):
        return True

    # 한글 → 포함 여부 체크
    return any(word in text for word in KOREAN_BADWORDS)
