import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from django.core.files.base import ContentFile
from datetime import datetime
from apps.transactions.models import TransactionHistory
from .models import Analysis


class Analyzer:
    def __init__(self, user, target_type, period_type, start_date, end_date):
        self.user = user
        self.target_type = target_type  # '수입' 또는 '지출'
        self.period_type = period_type  # '일간', '주간', '월간', '연간'
        self.start_date = start_date
        self.end_date = end_date

    def get_queryset(self):
        return TransactionHistory.objects.filter(
            account__owner=self.user,
            inout_type=self.target_type,
            transaction_datetime__range=[self.start_date, self.end_date]
        )

    def to_dataframe(self, qs):
        df = pd.DataFrame(list(qs.values('transaction_datetime', 'amount')))
        if df.empty:
            return pd.DataFrame(columns=['amount'])  # 빈 데이터프레임 리턴

        df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'])
        df.set_index('transaction_datetime', inplace=True)

        if self.period_type == '일간':
            return df.resample('D').sum()
        elif self.period_type == '주간':
            return df.resample('W').sum()
        elif self.period_type == '월간':
            return df.resample('M').sum()
        elif self.period_type == '연간':
            return df.resample('Y').sum()
        else:
            raise ValueError("지원하지 않는 period_type입니다.")

    def plot_graph(self, df):
        buffer = BytesIO()

        if df.empty or 'amount' not in df.columns:
            # 데이터 없을 경우 빈 그래프 생성
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.set_title(f'{self.period_type} {self.target_type} 분석')
            ax.set_xlabel('날짜')
            ax.set_ylabel('금액')
            ax.text(0.5, 0.5, '거래 내역이 없습니다.', ha='center', va='center', fontsize=12)
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            plt.close()
            return ContentFile(buffer.getvalue())

        # 정상 데이터 시 그래프 생성
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # 숫자 변환 명시
        df.plot(y='amount', legend=False, figsize=(10, 4))
        plt.title(f'{self.period_type} {self.target_type} 분석')
        plt.xlabel('날짜')
        plt.ylabel('금액')
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        plt.close()
        return ContentFile(buffer.getvalue())


    def run(self):
        qs = self.get_queryset()
        df = self.to_dataframe(qs)

        # 빈 데이터 처리
        if df.empty:
            summary = f"{self.start_date}부터 {self.end_date}까지의 {self.target_type} 내역이 없습니다."
        else:
            summary = f"{self.start_date}부터 {self.end_date}까지의 {self.period_type}별 {self.target_type} 분석 결과입니다."

        image = self.plot_graph(df)

        analysis = Analysis.objects.create(
            user=self.user,
            target_type=self.target_type,
            period_type=self.period_type,
            start_date=self.start_date,
            end_date=self.end_date,
            summary=summary
        )
        analysis.result_image_url.save(f'analysis_{analysis.id}.png', image)
        return analysis
