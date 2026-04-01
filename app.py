import streamlit as st
import google.generativeai as genai
import functions as func

#secrets.tomlを使う場合
#社内共有用については下記で説明
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("APIキーが設定されていません。")
else:
    genai.configure(api_key=api_key)

st.set_page_config(page_title="原稿生成システム", layout="wide")

st.title("原稿生成")
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("取材情報")
    interview_log = st.text_area("取材メモ・インタビュー内容", placeholder='取材内容を入力', height=200)

    #value=func.MAIN_TEMPLATESに関してはユーザー側によって直感的に触れるようにしたいので開放している
    with st.expander("詳細設定を開く", expanded=True):
        recruitment_templates = st.text_area("参照テンプレート", value=func.MAIN_TEMPLATES, height=100)
        company_info = st.text_area("会社補足情報", height=80)
       
        st.subheader("アピールポイント (3つ推奨)")
        selected_appeal_points = []
        for point in func.APPEAL_POINTS:
            if st.checkbox(point, key=point):
                detail = st.text_input(f"└ {point} の詳細", key=f"text_{point}")
                selected_appeal_points.append({"選択したもの": point, "加えたい指示": detail})
       
        template_instructions = st.text_area("構成への指示", placeholder="例：①会社の紹介", height=80)
        sample_message = st.text_area("サンプル原稿", placeholder="真似したい文体", height=150)

        #求人原稿であまりにも逸脱したクリエイティブな表現は不要なので、温度感の上限を設けることにした
        catch_temp = st.slider(
        "キャッチコピー温度感", 
        min_value=0.0, 
        max_value=0.15, 
        value=0.15
        )

        body_temp = st.slider(
        "本文温度感", 
        min_value=0.0, 
        max_value=0.50, 
        value=0.35
        )
        
generate_btn = st.button("原稿を生成する", disabled=not api_key)

with col2:
    st.header("生成結果")
    #ユーザー側の操作によってストプットが消えてしうので、ここで保持できるようにする。
    if "result" not in st.session_state:
        st.session_state.result = ""

    #APIを利用する生成においては（特にgeminiは）クオータによる制限が頻発しているのでtry, exceptで予防線を張る    
    if generate_btn:
        if not interview_log:
            st.error("取材情報を入力してください。")
        else:
            with st.spinner('原稿執筆中'):
                try:
                    st.session_state.result = func.call_generate(interview_log, company_info, template_instructions, sample_message, selected_appeal_points, catch_temp, body_temp)
                    st.success("生成完了")
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

    #出力にhtmlの<br>が表示されることがあったのでここでも置換を通している
    if st.session_state.result:
        final_text = st.session_state.result.replace('<br>', '\n\n').replace('<br><br>', '\n')
        st.markdown(final_text)
        st.code(final_text)
        
#以下は社内共有の際に、システムの入口でセキュリティを整えたもの
#最初に社内のメンバーだけがシステムにアクセスできるように設定
#with st.sidebar:
    #user_input=st.text_input("パスを入力", placeholder="ここに入力", type="password")

#ここで入場用のパスワードを定義
#CORRECT_PASSWORD =""

#if user_input != CORRECT_PASSWORD:
   #st.warning("パスを入力して入場")
   #st.stop()
#else:
    #st.success("原稿生成システムへようこそ")

#ここはサイドバーからAPI_KEYを入力する場合のロジック
#with st.sidebar:
   #user_inputkey=st.text_input("API_KEYを入力", placeholder="API_KEYを入力してください", type="password")
   #api_key=user_inputkey
