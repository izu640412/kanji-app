import streamlit as st
import random
from data import KANJI_LIST

# --- 1. 状態の初期化 ---
if 'all_kanji_data' not in st.session_state:
    st.session_state.all_kanji_data = KANJI_LIST
if 'wrong_list' not in st.session_state:
    st.session_state.wrong_list = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'test_data' not in st.session_state:
    st.session_state.test_data = []

# --- 2. ページ構成 ---
with st.sidebar:
    st.title("🍀 メニュー")
    menu = st.radio("メニューを選んでね", ["🏠 ホーム", "✍️ テスト開始", "🔥 復習モード"])
    st.write(f"現在の苦手漢字: {len(st.session_state.wrong_list)} 個")

# --- 3. メイン処理 ---
if menu == "🏠 ホーム":
    st.title("漢字クイズアプリ")
    st.write("メニューからモードを選んでください。")

elif menu == "✍️ テスト開始":
    st.title("✍️ 実力テスト")
    
    # テスト開始時のデータ抽出（問題数固定）
    if st.button("テストをリセットして開始"):
        st.session_state.test_data = random.sample(st.session_state.all_kanji_data, min(len(st.session_state.all_kanji_data), 10))
        st.session_state.current_question_idx = 0
        st.session_state.score = 0
        st.session_state.wrong_list = [] # 必要に応じてリセット
        st.rerun()

    if st.session_state.test_data:
        idx = st.session_state.current_question_idx
        if idx < len(st.session_state.test_data):
            current_q = st.session_state.test_data[idx]
            st.write(f"第 {idx + 1} 問: {current_q['kanji']}")
            
            user_input = st.text_input("読みを入力してください", key=f"input_{idx}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("回答", key=f"ans_{idx}"):
                    if user_input == current_q['read']:
                        st.success("正解！")
                        st.session_state.score += 1
                    else:
                        st.error(f"不正解。正解は {current_q['read']}")
                        if current_q not in st.session_state.wrong_list:
                            st.session_state.wrong_list.append(current_q)
                    st.session_state.current_question_idx += 1
                    st.rerun()
            
            with col2:
                # 「わからない」ボタン（固有IDを設定してエラー回避）
                if st.button("わからない", key=f"skip_{idx}"):
                    if current_q not in st.session_state.wrong_list:
                        st.session_state.wrong_list.append(current_q)
                    st.session_state.current_question_idx += 1
                    st.rerun()
        else:
            st.write(f"テスト終了！スコア: {st.session_state.score} / {len(st.session_state.test_data)}")

elif menu == "🔥 復習モード":
    st.title("🔥 苦手克服")
    if st.session_state.wrong_list:
        for w in st.session_state.wrong_list:
            st.write(f"・{w['kanji']}（{w['read']}）")
    else:
        st.success("完璧！苦手な漢字はありません。")
