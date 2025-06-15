import json
import os
import streamlit as st

# ملف القاموس
dict_file = "kuwaiti_dict.json"

# تحميل القاموس أو إنشاؤه
if os.path.exists(dict_file):
    with open(dict_file, "r", encoding="utf-8") as f:
        kuwaiti_dict = json.load(f)
else:
    kuwaiti_dict = {
        "وايد": "كثيراً",
        "شفيك": "ما بك",
        "زحمة": "ازدحام",
        "تآخرت": "تأخرت"
    }

# واجهة Streamlit
st.set_page_config(page_title="مترجم كويتي → فصحى", layout="wide")
st.title("📘 مترجم من اللهجة الكويتية إلى العربية الفصحى")

tab1, tab2 = st.tabs(["🔤 الترجمة", "📚 تحرير القاموس"])

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