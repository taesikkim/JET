# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 10:17:44 2024

@author: kicpa
"""

import streamlit as st
import pandas as pd
import io
from contextlib import redirect_stdout

# 데이터프레임 딕셔너리를 세션 상태에 저장
if 'dataframes' not in st.session_state:
    st.session_state['dataframes'] = {}

st.title("CSV 파일 로드 및 데이터프레임 조작")

# CSV 파일 업로드 및 데이터프레임 이름 입력을 사이드바로 이동
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])
df_name = st.sidebar.text_input("데이터프레임 이름")

if uploaded_file and df_name:
    try:
        # CSV 파일을 데이터프레임으로 읽기
        df = pd.read_csv(uploaded_file)
        st.session_state['dataframes'][df_name] = df
        st.success(f"데이터프레임 '{df_name}'이(가) 생성되었습니다.")
        st.write(f"### 데이터프레임 미리보기: {df_name}")
        st.dataframe(df)  # 스크롤 가능한 데이터프레임 미리보기
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

# Python 코드 입력
st.write("## Python 코드 입력")
st.write("코드 실행 시 `print` 함수를 사용하여 출력을 확인하세요. Streamlit 함수는 사용할 수 없습니다.")
code_input = st.text_area("Python 코드 입력", height=200)

if st.button("코드 실행"):
    allowed_globals = {'pd': pd}
    local_vars = st.session_state['dataframes'].copy()

    try:
        # 코드 실행 및 출력 캡처
        with io.StringIO() as output:
            with redirect_stdout(output):
                exec(code_input, allowed_globals, local_vars)
            output_value = output.getvalue()  # 출력 값을 저장합니다.

        # 변경된 데이터프레임 업데이트
        for name, df in local_vars.items():
            if isinstance(df, pd.DataFrame):
                st.session_state['dataframes'][name] = df

        # Print 출력
        st.write("### Print 출력")
        st.text(output_value)  # 저장된 출력 값을 사용합니다.

    except Exception as e:
        st.error(f"코드를 실행하는 중 오류가 발생했습니다: {e}")

# 데이터프레임 삭제 기능을 사이드바로 이동
st.sidebar.write("## 데이터프레임 삭제")
df_name_to_remove = st.sidebar.text_input("삭제할 데이터프레임 이름")

if st.sidebar.button("데이터프레임 삭제"):
    if df_name_to_remove in st.session_state['dataframes']:
        del st.session_state['dataframes'][df_name_to_remove]
        st.success(f"데이터프레임 '{df_name_to_remove}'이(가) 삭제되었습니다.")
    else:
        st.sidebar.warning(f"데이터프레임 '{df_name_to_remove}'을(를) 찾을 수 없습니다.")

# 데이터프레임 미리보기 (업데이트된 데이터프레임 표시)
if st.session_state['dataframes']:
    st.write("### 데이터프레임 미리보기")
    tab_titles = [name for name in st.session_state['dataframes'].keys()]
    tabs = st.tabs(tab_titles)

    for tab, (name, df) in zip(tabs, st.session_state['dataframes'].items()):
        with tab:
            st.write(f"#### {name}")
            st.dataframe(df)  # 스크롤 가능한 데이터프레임 미리보기
