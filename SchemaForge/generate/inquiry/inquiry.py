import json
from datetime import datetime, timedelta, timezone
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

# --- 日本時間 (JST) の定義 ---
JST = timezone(timedelta(hours=9), "JST")

def now_jst() -> datetime:
    return datetime.now(JST)

# --- 共通設定: 未定義のフィールドを許可しない ---
STRICT_CONFIG = ConfigDict(extra='forbid')

# --- 1. サブモデル: 電話番号 ---
class PhoneNumbers(BaseModel):
    model_config = STRICT_CONFIG
    fixed: Optional[str] = Field(None, description="固定電話番号")
    mobile: Optional[str] = Field(None, description="携帯電話番号")

# --- 2. サブモデル: 顧客情報 ---
class CustomerInfo(BaseModel):
    model_config = STRICT_CONFIG
    name: str = Field(..., description="顧客の氏名")
    name_kana: str = Field(..., description="顧客の氏名（カナ）")
    email: str = Field(..., description="メールアドレス")
    phones: Optional[PhoneNumbers] = Field(None, description="電話番号情報")

# --- 3. サブモデル: 物件情報 ---
class Property(BaseModel):
    model_config = STRICT_CONFIG
    id: Optional[str] = Field(None, description="物件ID")
    name: Optional[str] = Field(None, description="物件名称")

# --- 4. サブモデル: 検索・希望条件 ---
class Conditions(BaseModel):
    model_config = STRICT_CONFIG
    budget: Optional[int] = Field(None, description="家賃予算(上限)")
    areas: Optional[List[str]] = Field(None, description="希望エリア")
    lines: Optional[List[str]] = Field(None, description="希望沿線")
    layouts: Optional[List[str]] = Field(None, description="希望間取り")
    others: Optional[List[str]] = Field(None, description="その他の希望条件")
    instruments: Optional[List[str]] = Field(None, description="使用楽器の種類")

# --- 5. サブモデル: 問い合わせ概要 ---
class InquiryOutline(BaseModel):
    model_config = STRICT_CONFIG
    type: Optional[Literal["空室状況確認", "内見希望", "詳細確認", "非掲載写真確認希望", "その他", "募集時連絡希望", "オーナー", "物件検索依頼"]] = Field(None, description="具体的なお問い合わせ内容")
    contact_method: Literal["メール", "電話", "どちらでも"] = Field(..., description="希望する連絡方法")
    is_leisurely: Optional[bool] = Field(None, description="気ながに検索フラグ")
    move_in_plan: Optional[str] = Field(None, description="入居希望時期")

# --- 6. サブモデル: 問い合わせ詳細 ---
class InquiryDetail(BaseModel):
    model_config = STRICT_CONFIG
    property: Optional[Property] = Field(None, description="物件情報")
    conditions: Optional[Conditions] = Field(None, description="検索・希望条件")
    outline: InquiryOutline = Field(..., description="問い合わせ概要(種別/連絡/時期/ペース)")
    category: Literal["物件別", "物件リクエスト", "SUUMO", "オーナー", "その他"] = Field(..., description="お問い合わせの流入元/カテゴリ")
    message: Optional[str] = Field(None, description="お問い合わせ内容")

# --- 7. ルートモデル ---
class RealEstateInquiry(BaseModel):
    model_config = STRICT_CONFIG
    submitted_at: datetime = Field(default_factory=now_jst, description="問い合わせ日時(ISO8601形式, JST)")
    customer: CustomerInfo = Field(..., description="顧客情報")
    inquiries: List[InquiryDetail] = Field(..., description="問い合わせ詳細のリスト")

# JSON Schema生成
if __name__ == "__main__":
    print(json.dumps(RealEstateInquiry.model_json_schema(), indent=2, ensure_ascii=False))
