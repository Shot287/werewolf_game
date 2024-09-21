import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import random

# Streamlit SecretsからFirebaseの認証情報を取得
firebase_config = st.secrets["firebase"]

# Firebaseの初期化
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# タイトル
st.title("人狼ゲーム（テストモード）")

# プレイヤー登録
player_name = st.text_input("あなたの名前を入力してください:")

# 役職リスト（ランダムに割り当てるため）
roles = ["人狼", "人狼", "占い師", "騎士", "村人"]

# "/" を含む名前を排除し、空白を削除
player_name = player_name.replace("/", "").strip()

# プレイヤーの役職を初期化
role = None

# プレイヤー名が空でないか確認
if player_name:
    try:
        # すでに役職が割り当てられているか確認
        player_role_ref = db.collection("werewolf_game").document(player_name).get()

        if player_role_ref.exists:
            role = player_role_ref.to_dict()["role"]
            st.write(f"あなたの役職はすでに: {role} です。")
        else:
            # ランダムに役職を割り当てる
            random_role = random.choice(roles)
            db.collection("werewolf_game").document(player_name).set({
                "role": random_role
            })
            role = random_role  # ランダムに割り当てた役職を変数に保存
            st.write(f"あなたの役職はランダムに {role} に決まりました。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.error("プレイヤー名を入力してください。")

# 夜のターン: 人狼のチャット機能
if role == "人狼":
    st.subheader("あなたは人狼です。他の人狼と協力して襲撃対象を決めてください。")

    # チャットメッセージの送信
    chat_message = st.text_input("メッセージを入力してください:")

    if st.button("送信"):
        db.collection("werewolf_chat").add({
            "player": player_name,
            "message": chat_message
        })

    # チャット履歴の表示
    st.write("人狼チャット:")
    chat_docs = db.collection("werewolf_chat").stream()
    for doc in chat_docs:
        chat = doc.to_dict()
        st.write(f"{chat['player']}: {chat['message']}")
