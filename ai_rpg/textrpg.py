# pip install python-dotenv
# pip install gradio
# pip install ibm-watsonx-ai
# pip install pillow
# bash 에 설치 할 명령어 pip install python-dotenv gradio ibm-watsonx-ai pillow
from dotenv import load_dotenv
import os
import random
import gradio as gr

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference


# =========================
# WatsonX 설정
# =========================
load_dotenv()

apikey = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
watsonx_ai_url = os.getenv("WATSONX_URL")

credentials = Credentials(
    url=watsonx_ai_url,
    api_key=apikey,
)

client = APIClient(credentials)

model = ModelInference(
    model_id="meta-llama/llama-3-3-70b-instruct",
    api_client=client,
    project_id=project_id,
    params={"max_tokens": 3000},
)


# =========================
# 기본 스탯 생성
# =========================
def create_stats():
    return {
        "kindness": 0,
        "morality": 0,
        "ambition": 0,
        "revenge": 0,
        "faith": 0,
        "diligence": 0,
        "power": 0,

        # 숨겨진 내부 수치
        "corruption": 0,
        "stress": 0,
        "fame": 0,
        "fear": 0,
        "trust": 0
    }


# =========================
# 게임 상태 저장
# =========================
game_state = {
    "step": "name",
    "name": "",
    "personality": "",
    "dream": "",
    "stats": {},
    "logs": []
}


# =========================
# 초기 성격 보정
# =========================
def apply_personality_bonus(personality):
    bonus = {
        "착한": {"kindness": 10, "morality": 5},
        "악한": {"corruption": 10, "fear": 5},
        "야망 있는": {"ambition": 10, "fame": 5},
        "복수심에 가득찬": {"revenge": 10, "stress": 5},
        "신실한": {"faith": 10, "morality": 5},
        "성실한": {"diligence": 10, "trust": 5},
    }

    if personality in bonus:
        for stat, value in bonus[personality].items():
            game_state["stats"][stat] += value


# =========================
# 유년기 랜덤 이벤트
# =========================
def childhood_random_event():

    events = [
        {
            "text": "과거 용사 파티의 전사가 당신의 전투 재능을 알아보았습니다.",
            "effect": {
                "power": 15,
                "fame": 5,
                "morality": 5
            }
        },

        {
            "text": "은퇴한 궁정 마법사가 당신 안에 흐르는 마력과 학습 재능을 발견했습니다.",
            "effect": {
                "diligence": 15,
                "power": 10
            }
        },

        {
            "text": "떠돌이 상인이 당신의 빠른 계산력과 거래 감각을 알아보았습니다.",
            "effect": {
                "ambition": 15,
                "trust": 10
            }
        },

        {
            "text": "수상한 연금술사가 당신의 위험한 호기심을 흥미롭게 바라보았습니다.",
            "effect": {
                "diligence": 10,
                "ambition": 10,
                "corruption": 5
            }
        },

        {
            "text": "이단심문관이 당신 안에 깃든 파마의 재능을 알아보았습니다.",
            "effect": {
                "faith": 20,
                "morality": 5,
                "stress": 10,
                "fear": 10
            }
        }
    ]

    event = random.choice(events)

    for stat, value in event["effect"].items():
        game_state["stats"][stat] += value

    game_state["logs"].append(event["text"])

    return event["text"]


# =========================
# 장래희망 이벤트
# =========================
def apply_dream_bonus(dream):

    effects = {

        "기사": {
            "morality": 10,
            "power": 10
        },

        "성기사": {
            "faith": 15,
            "morality": 10
        },

        "마법사": {
            "diligence": 15,
            "power": 10
        },

        "상인": {
            "ambition": 15,
            "trust": 10
        },

        "왕": {
            "ambition": 15,
            "fame": 10
        },

        "마을 사람": {
            "stress": -5,
            "trust": 5
        }
    }

    effect = effects[dream]

    for stat, value in effect.items():
        game_state["stats"][stat] += value

    # 마을 사람 선택 시 power 초기화
    if dream == "마을 사람":
        game_state["stats"]["power"] = 0

    text = f"당신은 어린 시절부터 '{dream}'이 되고 싶다고 생각했습니다."

    game_state["logs"].append(text)

    return text


# =========================
# 스탯 출력
# =========================
def format_stats():

    result = "\n\n[현재 스탯]\n"

    for key, value in game_state["stats"].items():
        result += f"- {key}: {value}\n"

    return result


# =========================
# AI 유년기 분석
# =========================
def generate_ai_summary():

    system_prompt = """
    당신은 판타지 인생 시뮬레이션 게임의 내레이션 AI입니다.

    플레이어의 유년기 사건과 성향을 보고
    짧은 판타지 스타일의 설명을 작성하세요.

    반드시 한국어로 작성하세요.
    5줄 이내로 작성하세요.
    """

    user_prompt = f"""
    이름 : {game_state["name"]}

    초기 성격 :
    {game_state["personality"]}

    장래희망 :
    {game_state["dream"]}

    사건 기록 :
    {game_state["logs"]}

    현재 스탯 :
    {game_state["stats"]}
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },

        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = model.chat(messages=messages)

    return response["choices"][0]["message"]["content"]


# =========================
# 챗봇 진행 함수
# =========================
def game_chat(message, history):

    user_input = message.strip()

    # =========================
    # 이름 입력 단계
    # =========================
    if game_state["step"] == "name":

        game_state["stats"] = create_stats()
        game_state["logs"] = []

        game_state["name"] = user_input

        game_state["step"] = "personality"

        return f"""
좋습니다.

당신의 이름은 '{user_input}' 입니다.

초기 성격을 선택해주세요.

1. 착한
2. 악한
3. 야망 있는
4. 복수심에 가득찬
5. 신실한
6. 성실한
"""

    # =========================
    # 성격 선택 단계
    # =========================
    elif game_state["step"] == "personality":

        personality_map = {
            "1": "착한",
            "2": "악한",
            "3": "야망 있는",
            "4": "복수심에 가득찬",
            "5": "신실한",
            "6": "성실한"
        }

        personality = personality_map.get(user_input, user_input)

        game_state["personality"] = personality

        apply_personality_bonus(personality)

        event_text = childhood_random_event()

        game_state["step"] = "dream"

        return f"""
초기 성격이 '{personality}'으로 설정되었습니다.

[유년기 이벤트 1 : 적성 발견]

{event_text}

당신은 어떤 사람이 되고 싶습니까?

1. 기사
2. 성기사
3. 마법사
4. 상인
5. 왕
6. 마을 사람
"""

    # =========================
    # 장래희망 단계
    # =========================
    elif game_state["step"] == "dream":

        dream_map = {
            "1": "기사",
            "2": "성기사",
            "3": "마법사",
            "4": "상인",
            "5": "왕",
            "6": "마을 사람"
        }

        dream = dream_map.get(user_input, user_input)

        game_state["dream"] = dream

        dream_text = apply_dream_bonus(dream)

        ai_summary = generate_ai_summary()

        game_state["step"] = "end"

        return f"""
[유년기 이벤트 2 : 장래희망]

{dream_text}

[AI 유년기 분석]

{ai_summary}

{format_stats()}

유년기 테스트가 종료되었습니다.
"""

    else:
        return "유년기 테스트가 종료되었습니다."


# =========================
# Gradio 실행
# =========================
demo = gr.ChatInterface(
    fn=game_chat,

    chatbot=gr.Chatbot(
        value=[
            {
                "role": "assistant",
                "content": """
AI 판타지 인생 시뮬레이션을 시작합니다.

당신의 이름은 무엇인가요?
"""
            }
        ]
    ),

    title="AI 판타지 인생 시뮬레이션",

    description="""
챗봇과 대화하며 인생을 선택하는 게임입니다.
"""
)

demo.launch()
