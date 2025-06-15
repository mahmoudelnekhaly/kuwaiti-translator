# 🇰🇼 Kuwaiti Dialect Translator (اللهجة الكويتية → العربية الفصحى)

تطبيق بسيط لتحويل الجمل من اللهجة الكويتية إلى اللغة العربية الفصحى باستخدام Streamlit وقاموس قابل للتعديل.

## 📦 الملفات

- `app.py` - التطبيق الرئيسي
- `kuwaiti_dict.json` - القاموس اليدوي
- `requirements.txt` - الحزم المطلوبة

## 🚀 طريقة التشغيل المحلي

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 طريقة النشر على Streamlit Cloud

1. ارفع الملفات إلى GitHub
2. ادخل إلى https://streamlit.io/cloud
3. اربط بحساب GitHub، وحدد `app.py` كملف رئيسي
4. اضغط "Deploy"

## ✍️ تطوير مستقبلي

- دعم نموذج ذكاء اصطناعي تلقائي
- دعم قواعد بيانات لتخزين القاموس
- دعم لهجات خليجية أخرى