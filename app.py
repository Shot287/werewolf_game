import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import random

# FirebaseのSecrets情報を辞書形式で取得
firebase_credentials = {
    "type": st.secrets["firebase"]["type"],
    "project_id": st.secrets["firebase"]["project_id"],
    "private_key_id": st.secrets["firebase"]["private_key_id"],
    "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["firebase"]["client_email"],
    "client_id": st.secrets["firebase"]["client_id"],
    "auth_uri": st.secrets["firebase"]["auth_uri"],
    "token_uri": st.secrets["firebase"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
}

cred = credentials.Certificate(firebase_credentials)

# Firebaseの初期化
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



<<<<<<< HEAD
        # githubデスクトップから開けた!テストで編集出来るかやろうか

        #おー！！！
=======
        # githubデスクトップから開けた!テストで編集出来るかやろうかaaaa
        
>>>>>>> f36ecb4377cf6cf0800534eb296acf0bcfaee416
