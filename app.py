import os
import json
import re
import requests
import tarfile
import streamlit as st
from collections import Counter

dict_file = "kuwaiti_dict.json"
gumar_url = "https://github.com/CAMeL-Lab/Gumar-Ngrams/releases/download/v1.0/KW.tar.xz"
gumar_archive = "KW.tar.xz"
gumar_file = "KW/1-grams_KW.tsv"
extracted_file = "kuwaiti_gumar_dict.json"

# تحميل القاموس الأساسي
if os.path.exists(dict_file):
    with open(dict_file, "r", encoding="utf-8") as f:
        kuwaiti_dict = json.load(f)
else:
    kuwaiti_dict = {}

def download_and_extract_gumar():
    if not os.path.exists(gumar_archive):
        with requests.get(gumar_url, stream=True) as r:
            with open(gumar_archive, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    if not os.path.exists("KW"):
        with tarfile.open(gumar_archive) as tar:
            tar.extractall()

def extract_words_from_gumar():
    gumar_dict = {}
    with open(gumar_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                gumar_dict[parts[0]] = ""
            if i >= 20000:
                break
    with open(extracted_file, "w", encoding="utf-8") as f:
        json.dump(gumar_dict, f, ensure_ascii=False, indent=2)
    return gumar_dict

def merge_with_main_dict(new_words):
    added = 0
    for word in new_words:
        if word not in kuwaiti_dict:
            kuwaiti_dict[word] = ""
            added += 1
    with open(dict_file, "w", encoding="utf-8") as f:
        json.dump(kuwaiti_dict, f, ensure_ascii=False, indent=2)
    return added

# واجهة Streamlit
st.set_page_config(page_title="مترجم كويتي مع Gumar", layout="wide")
st.title("📘 مترجم اللهجة الكويتية إلى العربية الفصحى")

tab1, tab2, tab3 = st.tabs(["🔤 الترجمة", "📚 تحرير القاموس", "📥 تحديث من Gumar"])

with tab1:
    text = st.text_area("🗣️ أدخل نصًا باللهجة الكويتية:", height=150)
    if st.button("ترجم"):
        translation = " ".join(kuwaiti_dict.get(word, word) for word in text.split())
        st.subheader("✅ الترجمة إلى العربية الفصحى")
        st.write(translation)

with tab2:
    st.subheader("📚 تحرير القاموس")
    changed = False
    for key in list(kuwaiti_dict.keys()):
        new_val = st.text_input(f"{key}", kuwaiti_dict[key])
        if new_val != kuwaiti_dict[key]:
            kuwaiti_dict[key] = new_val
            changed = True
    if changed:
        with open(dict_file, "w", encoding="utf-8") as f:
            json.dump(kuwaiti_dict, f, ensure_ascii=False, indent=2)
        st.success("✅ تم تحديث القاموس")

with tab3:
    st.subheader("📥 تحميل ودمج مفردات Gumar")
    if st.button("ابدأ التحديث من Gumar"):
        with st.spinner("📦 جاري تحميل البيانات..."):
            download_and_extract_gumar()
            new_words = extract_words_from_gumar()
            added = merge_with_main_dict(new_words)
        st.success(f"✅ تم إضافة {added} مفردة جديدة من Gumar إلى القاموس.")