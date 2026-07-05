import streamlit as st
import random

# data.py からデータを読み込み
try:
    from data import KANJI_LIST
except ImportError:
    st.error("data.py が見つかりません。")
    st.stop()

# --- 状態の初期化 ---
if 'all_kanji_data' not in st.session_state:
    st.session_state.all_kanji_data = KANJI_LIST
if 'wrong_list' not in st.session_state:
    st.session_state.wrong_list = []
if 'test_data' not in st.session_state:
    st.session_state.test_data = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# --- サイドバー ---
with st.sidebar:
    st.title("🍀 メニュー")
    menu = st.radio("メニューを選んでね", ["🏠 ホーム", "✍️ テスト開始", "🔥 復習モード"])
    st.write(f"現在の苦手漢字: {len(st.session_state.wrong_list)} 個")

# --- ページ表示 ---
if menu == "🏠 ホーム":
    st.title("漢字クイズアプリへようこそ")

elif menu == "✍️ テスト開始":
    st.title("✍️ 実力テスト")
    
    # 10問に固定して開始
    if st.button("テスト開始・リセット"):
        st.session_state.test_data = random.sample(st.session_state.all_kanji_data, min(10, len(st.session_state.all_kanji_data)))
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.rerun()

    if st.session_state.test_data:
        q_idx = st.session_state.current_question
        if q_idx < len(st.session_state.test_data):
            q = st.session_state.test_data[q_idx]
            st.subheader(f"第 {q_idx + 1} 問: {q['kanji']}")
            
            user_ans = st.text_input("読みを入力してください", key=f"input_{q_idx}")
            
            # 回答判定（IDにインデックスを付けて重複回避）
            if st.button("回答する", key=f"btn_{q_idx}"):
                if user_ans == q['read']:
                    st.success("正解！")
                    st.session_state.score += 1
                else:
                    st.error(f"不正解... 正解は「{q['read']}」でした")
                    if q not in st.session_state.wrong_list:
                        st.session_state.wrong_list.append(q)
                
                if st.button("次の問題へ", key=f"next_{q_idx}"):
                    st.session_state.current_question += 1
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
