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

# ログイン用変数とデータベースコレクション
login_status = st.session_state.get("login_status", False)
is_host = st.session_state.get("is_host", False)

# ホストかプレイヤーのログイン
if not login_status:
    st.title("人狼ゲーム ログイン")
    role = st.radio("あなたはホストですか？", ("ホスト", "プレイヤー"))

    player_name = st.text_input("名前を入力してください:")
    login_button = st.button("ログイン")

    if login_button and player_name:
        st.session_state.login_status = True
        if role == "ホスト":
            st.session_state.is_host = True
            st.write("ホストとしてログインしました。")
        else:
            st.session_state.is_host = False
            # プレイヤーを登録
            players_ref = db.collection("werewolf_game").document(player_name)
            players_ref.set({"name": player_name, "role": None})
            st.write(f"プレイヤーとして {player_name} でログインしました。")

# ログイン後の処理
if login_status:
    if is_host:
        st.subheader("現在のプレイヤー:")
        players = db.collection("werewolf_game").stream()
        player_list = []
        for player in players:
            player_list.append(player.to_dict().get("name", "名前がありません"))
        
        st.write(player_list)
        
        if st.button("ゲーム開始") and len(player_list) == 5:
            st.write("ゲームが開始されました！")

        # 強制ログアウト機能
        player_to_remove = st.selectbox("強制ログアウトさせるプレイヤーを選択:", player_list)
        if st.button("強制ログアウト"):
            db.collection("werewolf_game").document(player_to_remove).delete()
            st.write(f"{player_to_remove} がログアウトさせられました。")

    else:
        st.subheader(f"プレイヤー {st.session_state['login_status']} としてログイン中")
        st.write("ゲームがホストによって開始されるのを待っています。")

# 役職のランダム割り当て
if st.session_state.login_status:
    st.write("役職のランダム割り当て")
    roles = ["村人", "人狼", "占い師", "騎士", "狂人"]
    if is_host:
        st.write("ホストは役職の割り当てを管理します。")
    else:
        assigned_role = random.choice(roles)
        player_name = st.session_state["login_status"]
        player_role_ref = db.collection("werewolf_game").document(player_name)
        player_role_ref.set({"role": assigned_role}, merge=True)
        st.write(f"あなたの役職は {assigned_role} です。")

    # 人狼同士のチャット機能
    if assigned_role == "人狼":
        st.write("あなたは人狼です。他の人狼とチャットで会話できます。")
        chat_input = st.text_input("チャットメッセージ:")
        if st.button("送信"):
            st.write(f"送信メッセージ: {chat_input}")
            # Firestoreなどでチャットデータを管理する処理を追加

