
import streamlit as st
from transformers import MarianMTModel, MarianTokenizer

# 모델과 토크나이저 로드
model_name = "Helsinki-NLP/opus-mt-ko-en"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

# Streamlit 앱 제목 설정
st.title("한국어 → 영어 번역기")

# 사용자가 입력할 한국어 텍스트 받기
korean_text = st.text_area("한국어 텍스트를 입력하세요", height=150)

# 번역 버튼 클릭 시 번역 수행
if st.button("번역하기"):
    if korean_text:
        # 텍스트 토큰화
        translated = tokenizer(korean_text, return_tensors="pt", padding=True)

        # 번역 수행
        translation = model.generate(**translated)

        # 결과 디코딩
        translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)

        # 번역된 텍스트 출력
        st.subheader("번역 결과:")
        st.write(translated_text)
    else:
        st.warning("번역할 텍스트를 입력해주세요.")
