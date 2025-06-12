# Project

가계부 API 프로젝트

## 디렉토리 구조

```
project/
├── config/                        # 프로젝트 설정 디렉토리
│   ├── settings.py                # Django 설정 파일
│   ├── urls.py                    # 전역 URLConf
│   ├── wsgi.py                    # WSGI 설정
│   └── asgi.py                    # ASGI 설정
├── apps/                          # 각 도메인별 앱
│   ├── users/                     # 사용자 관련 (회원가입 등)
│   │   ├── models.py              # 사용자 모델
│   │   ├── views.py               # 사용자 관련 뷰
│   │   ├── serializers.py         # 사용자 시리얼라이저
│   │   ├── urls.py                # 사용자 URLConf
│   │   └── permissions.py         # 사용자 권한 정의
│   ├── accounts/                  # 계좌 관련
│   │   ├── models.py              # 계좌 모델
│   │   ├── views.py               # 계좌 관련 뷰
│   │   ├── serializers.py         # 계좌 시리얼라이저
│   │   ├── urls.py                # 계좌 URLConf
│   │   └── constants.py           # ENUM/상수 정의
│   ├── transactions/              # 거래 내역
│   │   ├── models.py              # 거래내역 모델
│   │   ├── views.py               # 거래내역 뷰
│   │   ├── serializers.py         # 거래내역 시리얼라이저
│   │   ├── urls.py                # 거래내역 URLConf
│   │   └── constants.py           # ENUM/상수 정의
│   ├── analysis/                  # 소비 분석
│   │   ├── models.py              # 분석 관련 모델
│   │   ├── views.py               # 분석 뷰
│   │   ├── serializers.py         # 분석 시리얼라이저
│   │   ├── urls.py                # 분석 URLConf
│   │   └── logic.py               # 분석 로직
│   └── notifications/             # 사용자 알림
│       ├── models.py              # 알림 모델
│       ├── views.py               # 알림 뷰
│       ├── serializers.py         # 알림 시리얼라이저
│       ├── urls.py                # 알림 URLConf
│       └── signals.py             # 알림 자동 생성 로직
├── manage.py                      # Django 관리 명령어 진입점
└── requirements.txt               # 의존성 패키지 목록
```
