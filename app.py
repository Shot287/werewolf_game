import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import random

# Streamlit SecretsからFirebase認証情報を取得
firebase_credentials = st.secrets["firebase"]
cred = credentials.Certificate(firebase_credentials)

# Firebaseの初期化（既に初期化されていない場合のみ）
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# プレイヤー名入力
st.title("人狼ゲーム（テストモード）")
player_name = st.text_input("あなたの名前を入力してください:")

# 役職をランダムに割り当てる
if player_name:
    roles = ["村人", "人狼", "占い師", "騎士", "狂人"]
    assigned_role = random.choice(roles)

    # Firestoreに役職を保存
    player_role_ref = db.collection("werewolf_game").document(player_name)
    player_role_ref.set({"role": assigned_role})

    st.write(f"あなたの役職はランダムに {assigned_role} に決まりました。")

    # 人狼の場合のチャット画面表示（仮）
    if assigned_role == "人狼":
        st.write("あなたは人狼です。チャットで他の人狼と会話しましょう。")
