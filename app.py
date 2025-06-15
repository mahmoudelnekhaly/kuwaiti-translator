import json
import os
import streamlit as st
import requests
from bs4 import BeautifulSoup

dict_file = "kuwaiti_dict.json"

# تحميل القاموس
if os.path.exists(dict_file):
    with open(dict_file, "r", encoding="utf-8") as f:
        kuwaiti_dict = json.load(f)
else:
    kuwaiti_dict = {}

# وظيفة التحديث اليدوي
def load_gumar_sample():
    sample_sentences = [
        "ليش تأخرت وايد؟",
        "تبي أوديك السوق؟",
        "ما قلنا لك من قبل؟",
        "ترى الجو حلو اليوم بالكويت"
    ]
    return sample_sentences

def scrape_forum_example():
    try:
        url = "https://www.q8yat.com/forumdisplay.php?f=5"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("a", class_="threadtitle")
        return [post.get_text(strip=True) for post in posts][:10]
    except:
        return []

def update_dictionary(sentences):
    new_entries = 0
    for sentence in sentences:
        for word in sentence.strip().split():
            word = word.strip("؟!.,،").lower()
            if word not in kuwaiti_dict and len(word) > 2:
                kuwaiti_dict[word] = ""
                new_entries += 1
    return new_entries

# واجهة Streamlit
st.set_page_config(page_title="مترجم كويتي → فصحى", layout="wide")
st.title("📘 مترجم من اللهجة الكويتية إلى العربية الفصحى")

tab1, tab2, tab3 = st.tabs(["🔤 الترجمة", "📚 تحرير القاموس", "🔄 تحديث يدوي"])

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
    st.subheader("🔄 تحديث القاموس من مصادر تلقائية")
    if st.button("تحديث القاموس الآن"):
        sentences = load_gumar_sample() + scrape_forum_example()
        added = update_dictionary(sentences)
        with open(dict_file, "w", encoding="utf-8") as f:
            json.dump(kuwaiti_dict, f, ensure_ascii=False, indent=2)
        st.success(f"✅ تم تحديث القاموس وإضافة {added} كلمة جديدة.")