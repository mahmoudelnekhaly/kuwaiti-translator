import json
import os
import re
import streamlit as st
from collections import Counter

dict_file = "kuwaiti_dict.json"

# تحميل القاموس
if os.path.exists(dict_file):
    with open(dict_file, "r", encoding="utf-8") as f:
        kuwaiti_dict = json.load(f)
else:
    kuwaiti_dict = {}

# عينات من Gumar Corpus وتمثيل YouTube
gumar_data = [
    {"dialect": "kuwaiti", "text": "ليش تأخرت علينا؟"},
    {"dialect": "kuwaiti", "text": "تدري ان الجمعية مسكرة؟"},
    {"dialect": "kuwaiti", "text": "أبي أطلع مشوار وبعدين أرد"},
]

youtube_transcripts = [
    "السلام عليكم شباب، اليوم بنسولف عن الزحمة في الشوارع",
    "ترى الحر مو طبيعي اليوم بالكويت",
    "شلون الواحد يتحمل الصيف؟"
]

def extract_words(text):
    text = re.sub(r"[^؀-ۿ\s]", "", text)
    words = text.split()
    return [w.strip().lower() for w in words if len(w) > 2]

def update_dict_from_sources(gumar, youtube):
    word_counter = Counter()
    for entry in gumar:
        if entry["dialect"] == "kuwaiti":
            word_counter.update(extract_words(entry["text"]))
    for line in youtube:
        word_counter.update(extract_words(line))

    new_entries = 0
    for word in word_counter:
        if word not in kuwaiti_dict:
            kuwaiti_dict[word] = ""
            new_entries += 1

    with open(dict_file, "w", encoding="utf-8") as f:
        json.dump(kuwaiti_dict, f, ensure_ascii=False, indent=2)

    return new_entries

# واجهة Streamlit
st.set_page_config(page_title="مترجم كويتي → فصحى", layout="wide")
st.title("📘 مترجم من اللهجة الكويتية إلى العربية الفصحى")

tab1, tab2, tab3 = st.tabs(["🔤 الترجمة", "📚 تحرير القاموس", "📥 تحديث تلقائي"])

with tab1:
    user_input = st.text_area("أدخل نصاً باللهجة الكويتية", height=150)
    if st.button("ترجم"):
        translated = " ".join(kuwaiti_dict.get(word, word) for word in user_input.split())
        st.subheader("📝 الترجمة إلى الفصحى")
        st.write(translated)

with tab2:
    st.subheader("📖 تحرير القاموس اليدوي")
    updated = False
    for key in list(kuwaiti_dict.keys()):
        new_val = st.text_input(f"{key}:", kuwaiti_dict[key])
        if new_val != kuwaiti_dict[key]:
            kuwaiti_dict[key] = new_val
            updated = True
    if updated:
        with open(dict_file, "w", encoding="utf-8") as f:
            json.dump(kuwaiti_dict, f, ensure_ascii=False, indent=2)
        st.success("✅ تم حفظ القاموس بنجاح!")

with tab3:
    st.subheader("📥 تحديث تلقائي من Gumar + YouTube")
    if st.button("تحديث القاموس من البيانات"):
        added = update_dict_from_sources(gumar_data, youtube_transcripts)
        st.success(f"✅ تم إضافة {added} مفردة جديدة من Gumar و YouTube.")