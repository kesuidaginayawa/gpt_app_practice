import streamlit as st
import openai
import speech_recognition as sr

r = sr.Recognizer()
def mic_speech_to_text(set_language):
    # マイク入力を音声ファイルとして読み込み
    with sr.Microphone() as source:
        audio = r.listen(source) # r.listen(マイク入力)で認識準備
    try:
        text = r.recognize_google(audio, language="ja") #  r.recognize_google(音声データ,言語)で音声認識して、textに代入
    except:
        text = "音声認識に失敗しました"
    return text # 認識した文字を返す


openai.api_key = ''
class ChatGptApi:
    def __init__(self, system_setting):
        self.system = {'role':'system','content':system_setting}
        self.input_list = [self.system]
        self.logs = []
    def input_messages(self,input_text):
        self.input_list.append({'role':'user','content':input_text})
        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.input_list
        )
        self.logs.append(res)
        self.input_list.append(
            {'role':'assistant','content':res.choices[0].message.content}
        )       
        return(self.input_list[-1]['content'])

api1 = ChatGptApi(
    system_setting='あなたはとてもユーモアのあるコメディアン忍者です。どんな事を言われてもギャグで返します。忍者っぽく話します。'
)
api2 = ChatGptApi(
    system_setting='あなたは真面目な性格の侍です。ギャグには冷静な侍っぽいツッコミを入れます。'
)
api3 = ChatGptApi(
    system_setting='あなたはとても優秀な探偵です。どのような会話からもヒントを見つけ犯人を見つけます。キザな話し方をして、会話の終わりには必ず犯人を見つけます。'
)
api4 = ChatGptApi(
    system_setting='あなたはとても陽気なフラダンサーです。踊りながら話します。'
)
api5 = ChatGptApi(
    system_setting='あなたは世界的に有名なギタリストです。どのような会話も弾き語りしながらこなす事ができます。'
)

USER_NAME = "user"
API1 = "忍者"
API2 = "侍"
API3 = "探偵"
API4 = "ダンサー"
API5 = "ギタリスト"

from PIL import Image
img1 = Image.open("k0482_1.jpg")
img2 = Image.open("k0594_5.jpg")
img3 = Image.open("k0202_1.jpg")
img4 = Image.open("k0377_1.jpg")
img5 = Image.open("k0543_4.jpg")

api_dict = {
    API1:api1,
    API2:api2,
    API3:api3,
    API4:api4,
    API5:api5
}

avator_img_dict = {
    API1: img1,
    API2: img2,
    API3: img3,
    API4: img4,
    API5: img5
}
##################################################################

st.title(':sunglasses: _GPTとおしゃべりアプリ_')

st.sidebar.header('キャラクター')
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.subheader('Character1')
    st.image(img1,width=100)
    st.write('ユーモアのある忍者です。')
with col2:
    st.subheader('Character2')
    st.image(img2,width=100)
    st.write('冷静なツッコミができる侍です。')
with col3:
    st.subheader('Character3')
    st.image(img3,width=100)
    st.write('優秀な探偵です。')

col2_1, col2_2, col2_3 = st.sidebar.columns(3)
with col2_1:
    st.subheader('Character4')
    st.image(img4,width=100)
    st.write('陽気なフラダンサーです。')
with col2_2:
    st.subheader('Character5')
    st.image(img5,width=100)
    st.write('世界的に有名なギタリストです。')



st.sidebar.header('キャラクター選択')
options = st.sidebar.multiselect(
    '2人選んでください',
    [API1,API2,API3,API4,API5],
    max_selections=2
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "こんちは！"}]

st.write('')
st.write('')
if st.button("キャラクターを選んだあと、ここをクリックして話かけてください"):
    state = st.empty() # マイク録音中を示す為の箱を準備
    state.write("音声認識中") # 箱に案内表示書き込み
    result_text = mic_speech_to_text('ja') # 選択した言語を元に音声認識開始
    state.write("音声認識完了") # 箱に案内表示書き込み
    st.balloons()

    with st.chat_message(USER_NAME):
        st.write(result_text)
    with st.chat_message(options[0], avatar=avator_img_dict[options[0]]):
        st.write(api_dict[options[0]].input_messages(result_text))
    with st.chat_message(options[1], avatar=avator_img_dict[options[1]]):
        st.write(api_dict[options[1]].input_messages(api_dict[options[0]].input_list[-1]["content"]))
    with st.chat_message(options[0], avatar=avator_img_dict[options[0]]):
        st.write(api_dict[options[0]].input_messages(api_dict[options[1]].input_list[-1]["content"]))
    st.snow()





