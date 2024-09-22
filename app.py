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

# プレイヤー名入力 & ログイン
st.title("人狼ゲーム（テストモード）")
player_name = st.text_input("あなたの名前を入力してください:")
is_host = st.checkbox("私はホストです")

if st.button("ログイン"):
    if player_name:
        # プレイヤー情報をFirebaseに保存
        player_ref = db.collection("werewolf_game").document(player_name)
        player_ref.set({"name": player_name, "is_host": is_host})
        st.success(f"{player_name} としてログインしました！")
    else:
        st.error("名前を入力してください")

# 現在ログインしているプレイヤーを表示（ホストのみ）
if is_host:
    st.subheader("現在のプレイヤー:")
    players = db.collection("werewolf_game").stream()
    player_list = []
    for player in players:
        player_list.append(player.to_dict()["name"])
    
    st.write(player_list)
    
    # 5人までしかログインできないように制限
    if len(player_list) >= 5:
        st.warning("既に5人がログインしています。これ以上ログインできません。")

# ホストがゲームを開始する
if is_host and len(player_list) >= 5:
    if st.button("ゲームを開始"):
        st.write("ゲームを開始しました！")

# 強制ログアウト機能
if is_host:
    st.subheader("強制ログアウト機能")
    player_to_logout = st.selectbox("強制ログアウトするプレイヤーを選択", player_list)
    if st.button("強制ログアウト"):
        db.collection("werewolf_game").document(player_to_logout).delete()
        st.success(f"{player_to_logout} をログアウトしました")

# プレイヤー名入力と役職割り当て
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
        chat_message = st.text_input("チャットメッセージを入力")
        if st.button("送信"):
            db.collection("werewolf_game_chat").add({"name": player_name, "message": chat_message})
            st.success("メッセージを送信しました")

    # チャットの表示
    st.subheader("チャット履歴")
    messages = db.collection("werewolf_game_chat").stream()
    for message in messages:
        chat = message.to_dict()
        st.write(f"{chat['name']}: {chat['message']}")
