# 네이버 로그인 설정 가이드

## 1. 네이버 개발자센터 설정

1. **네이버 개발자센터 접속**
   - https://developers.naver.com/main/ 접속
   - 네이버 아이디로 로그인

2. **애플리케이션 등록**
   - "Application" → "애플리케이션 등록" 클릭
   - 애플리케이션 이름: `Budget Ledger`
   - 사용 API: **네이버 로그인** 선택

3. **서비스 URL 설정**
   ```
   서비스 URL: http://localhost:8001
   Callback URL: http://localhost:8001/accounts/naver/login/callback/
   ```

4. **제공 정보 선택**
   - ✅ 이메일 주소 (필수)
   - ✅ 닉네임 (필수)
   - ✅ 프로필 이미지 (선택)

## 2. 환경변수 설정

네이버 개발자센터에서 발급받은 정보를 `.env` 파일에 추가:

```bash
# 네이버 소셜 로그인 설정
NAVER_CLIENT_ID=발급받은_클라이언트_ID
NAVER_CLIENT_SECRET=발급받은_클라이언트_시크릿
```

## 3. 운영 환경 설정

**운영 서버에서는 다음과 같이 설정:**

```
서비스 URL: https://yourdomain.com
Callback URL: https://yourdomain.com/accounts/naver/login/callback/
```

## 4. 테스트

1. 서버 실행: `python3 manage.py runserver 8001`
2. 브라우저에서 `http://localhost:8001/accounts/login/` 접속
3. "네이버로 로그인" 버튼 클릭하여 테스트

## 5. 주의사항

- 개발 환경에서는 localhost:8001을 사용
- 운영 환경에서는 실제 도메인으로 변경 필요
- 클라이언트 ID와 시크릿은 절대 공개하지 마세요
- `.env` 파일은 `.gitignore`에 포함되어야 합니다

## 6. 문제해결

**네이버 로그인 버튼이 보이지 않는 경우:**
1. `NAVER_CLIENT_ID`가 .env에 정확히 설정되었는지 확인
2. 서버 재시작: `Ctrl+C` 후 `python3 manage.py runserver 8001`

**콜백 오류가 발생하는 경우:**
1. 네이버 개발자센터의 Callback URL이 정확한지 확인
2. URL 끝에 슬래시(`/`)가 있는지 확인 