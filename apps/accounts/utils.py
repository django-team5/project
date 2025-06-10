from .constants import BANK_CODES

# 코드 → 이름 역매핑용 딕셔너리 
BANK_CODE_TO_NAME = {code: name for code, name in BANK_CODES}

def get_bank_name_by_code(code: str) -> str:
    """
    은행 코드로 한글 이름을 반환합니다. 존재하지 않으면 '알수없음' 반환.
    """
    return BANK_CODE_TO_NAME.get(code, "알수없음")
