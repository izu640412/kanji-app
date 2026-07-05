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

# 回答後の画面キープ用
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""

# --- 選択肢生成関数 ---
def get_choices(correct_read):
    # すべての読みを取得して正解以外のリストを作る
    all_reads = [item['read'] for item in st.session_state.all_kanji_data]
    other_reads = list(set([r for r in all_reads if r != correct_read]))
    
    # ダミーを最大3つ選び、正解と混ぜてシャッフルする
    num_wrong = min(len(other_reads), 3)
    wrong_choices = random.sample(other_reads, num_wrong)
    choices = wrong_choices + [correct_read]
    random.shuffle(choices)
    return choices

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
    
    # 出題形式の選択
    practice_type = st.radio("出題形式を選んでください", ["入力で答える", "選択肢から選ぶ"])

    if st.button("テストをリセットして開始"):
        # ランダムに10問選出
        st.session_state.test_data = random.sample(st.session_state.all_kanji_data, min(len(st.session_state.all_kanji_data), 10))
        st.session_state.current_question_idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.wrong_list = [] # テスト開始時に苦手リストをリセット
        st.rerun()

    if st.session_state.test_data:
        idx = st.session_state.current_question_idx
        if idx < len(st.session_state.test_data):
            current_q = st.session_state.test_data[idx]
            st.write(f"第 {idx + 1} 問: {current_q['kanji']}")
            
            # -----------------------------------
            # 回答した後の結果表示画面
            # -----------------------------------
            if st.session_state.answered:
                if st.session_state.last_result == "correct":
                    st.success("⭕ 正解！")
                elif st.session_state.last_result == "wrong":
                    st.error(f"❌ 不正解。正解は「{current_q['read']}」でした。")
                else:
                    st.warning(f"「{current_q['kanji']}」を苦手リストに追加しました。（正解は「{current_q['read']}」）")
                
                # 次へ進むボタン
                if st.button("次の問題へ 👉", key=f"next_{idx}", type="primary"):
                    st.session_state.current_question_idx += 1
                    st.session_state.answered = False
                    st.rerun()
            
            # -----------------------------------
            # 回答する前の画面
            # -----------------------------------
            else:
                # 【入力形式モード】
                if practice_type == "入力で答える":
                    user_input = st.text_input("読みを入力してください", key=f"input_{idx}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("回答", key=f"ans_{idx}"):
                            st.session_state.answered = True
                            if user_input == current_q['read']:
                                st.session_state.last_result = "correct"
                                st.session_state.score += 1
                            else:
                                st.session_state.last_result = "wrong"
                                if current_q not in st.session_state.wrong_list:
                                    st.session_state.wrong_list.append(current_q)
                            st.rerun()
                    with col2:
                        if st.button("わからない", key=f"skip_{idx}"):
                            st.session_state.answered = True
                            st.session_state.last_result = "skipped"
                            if current_q not in st.session_state.wrong_list:
                                st.session_state.wrong_list.append(current_q)
                            st.rerun()
                
                # 【選択形式モード】
                else:
                    # その問題の選択肢を生成してセッションに保持（再描画で変わらないようにするため）
                    if f"choices_{idx}" not in st.session_state:
                        st.session_state[f"choices_{idx}"] = get_choices(current_q['read'])
                    
                    choices = st.session_state[f"choices_{idx}"]
                    
                    # 4つの選択肢ボタンを表示
                    for i, choice in enumerate(choices):
                        if st.button(choice, key=f"choice_{idx}_{i}", use_container_width=True):
                            st.session_state.answered = True
                            if choice == current_q['read']:
                                st.session_state.last_result = "correct"
                                st.session_state.score += 1
                            else:
                                st.session_state.last_result = "wrong"
                                if current_q not in st.session_state.wrong_list:
                                    st.session_state.wrong_list.append(current_q)
                            st.rerun()
                    
                    # わからないボタン
                    st.write("---")
                    if st.button("わからない", key=f"skip_choice_{idx}", use_container_width=True):
                        st.session_state.answered = True
                        st.session_state.last_result = "skipped"
                        if current_q not in st.session_state.wrong_list:
                            st.session_state.wrong_list.append(current_q)
                        st.rerun()
        else:
            st.success(f"テスト終了！スコア: {st.session_state.score} / {len(st.session_state.test_data)}")

elif menu == "🔥 復習モード":
    st.title("🔥 苦手克服")
    if st.session_state.wrong_list:
        for w in st.session_state.wrong_list:
            st.write(f"・{w['kanji']}（{w['read']}）")
    else:
        st.success("完璧！苦手な漢字はありません。")
