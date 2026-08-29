# 🦠 تحلیل داده‌های پاندمی COVID-19

![COVID-19 Pandemic Data Analysis](./COVID-19-Analysis.jpg)

این پروژه یک چارچوب قابل‌بازتولید برای دریافت، استانداردسازی، پاک‌سازی، تحلیل و مصورسازی داده‌های تاریخی روزانه COVID-19 است.

[English README](./README.md)

## ✨ ویژگی‌های اصلی

- بارگذاری متمرکز و قابل‌استفاده‌مجدد فایل‌های CSV.
- استانداردسازی تغییرات تاریخی Schema و نام ستون‌ها.
- استخراج تاریخ گزارش و ساخت Time Series در سطح کشور.
- مدیریت محتاطانه مقادیر گمشده و داده‌های نامعتبر.
- شناسایی Duplicateهای دقیق و Duplicateهای مبتنی بر کلیدهای اداری.
- توابع مستقل برای Visualization جهانی، کشوری و مقایسه کشورهای برتر.
- تست‌های خودکار و بررسی کیفیت کد با GitHub Actions.
- نگهداری Dataset خام خارج از Git برای حفظ حجم و بازتولیدپذیری Repository.

## 🧱 ساختار پروژه

```text
.
├── .github/workflows/ci.yml
├── data/
│   ├── raw/                 # داده خام؛ توسط Git نادیده گرفته می‌شود
│   ├── interim/             # داده‌های میانی
│   ├── processed/           # داده‌های پردازش‌شده
│   └── README.md
├── docs/
│   ├── schema_analysis.md
│   └── data_quality_pipeline.md
├── scripts/
│   └── download_data.py
├── src/
│   ├── config.py
│   ├── schema.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── visualization.py
│   └── data_loader.py
├── tests/
│   └── test_data_loader.py
├── COVID-19_Analysis_Notebook.ipynb
├── pyproject.toml
├── requirements.txt
├── README.md
└── README_fa.md
```

## 🔄 معماری

```text
CSVهای خام
   ↓
data_loader.py
   ↓
schema.py
   ↓
cleaning.py
   ↓
analysis.py
   ↓
visualization.py
   ↓
Jupyter Notebook
```

نوت‌بوک عمدتاً برای EDA، تفسیر نتایج و ارائه بصری استفاده می‌شود و منطق قابل‌استفاده‌مجدد در `src/` قرار دارد.

## 🚀 نصب و اجرا

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 📦 Dataset

فایل‌های خام در Repository قرار نمی‌گیرند و در `data/raw/` دانلود می‌شوند. پروژه برای گزارش‌های روزانه آرشیوشده Johns Hopkins CSSE طراحی شده است.

نمونه:

```bash
python scripts/download_data.py 01-01-2021 01-02-2021 01-03-2021
```

برای بازتولید دقیق یک تحلیل، بازه تاریخ و Revision منبع مورد استفاده باید ثبت شود.

## ▶️ اجرای Notebook

پس از قرار دادن CSVهای موردنیاز در `data/raw/`، فایل `COVID-19_Analysis_Notebook.ipynb` را با Jupyter Lab، Jupyter Notebook یا Google Colab اجرا کنید.

## 🧪 تست‌ها

```bash
pytest -q
```

## 🧹 کیفیت کد

پروژه از Black، isort و Ruff استفاده می‌کند و GitHub Actions در هر Push یا Pull Request، Formatting، ترتیب Importها، Lint و تست‌ها را بررسی می‌کند.

```bash
black src tests
isort src tests
ruff check src tests
pytest -q
```

## 📊 مصورسازی

توابع reusable در `src/visualization.py` برای موارد زیر در دسترس هستند:

- روند تجمعی جهانی.
- روند یک کشور مشخص.
- رتبه‌بندی کشورهای برتر بر اساس شاخص انتخابی.

## 📚 مستندات

- [`docs/schema_analysis.md`](./docs/schema_analysis.md) — تفاوت‌های Schema در گزارش‌های تاریخی.
- [`docs/data_quality_pipeline.md`](./docs/data_quality_pipeline.md) — سیاست تاریخ، پاک‌سازی، تجمیع و Duplicateها.

## 📄 مجوز

پیش از توزیع کد یا داده، مجوز مناسب پروژه و شرایط استفاده از Dataset منبع را مشخص کنید.