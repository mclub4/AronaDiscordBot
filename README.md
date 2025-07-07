# AronaDiscordBot 🎧

블루 아카이브의 귀여운 AI 조수, **아로나(Arona)** 를 Discord에 소환해 보세요!  
이 봇은 [arona.ai](https://arona.ai/) 사이트에서 영감을 받아 만들어졌으며, 선생님들과 함께 음악을 들으며 놀 수 있도록 다양한 기능을 제공합니다.

---

## 🛠 주요 기능

### 🎶 음악 재생 기능
- `/play [곡명]`  
  유튜브에서 자동으로 검색해서 곡을 재생합니다.  
  선생님이 원하시는 음악을 틀어드릴게요!

- `/nowplaying`  
  지금 재생 중인 곡을 알려드려요.

- `/list`  
  대기 중인 곡 리스트를 보여드립니다.

- `/leave`  
  음성 채널에서 나갈게요~

- `/clearqueue`  
  대기열을 모두 비워버릴게요!

- `/pause`, `/resume`, `/skip`, `/stop`  
  음악을 일시정지하거나, 다시 재생하거나, 넘기거나, 정지할 수 있어요.  
  버튼으로도 조작 가능하니 편한 방법을 사용하세요!

- `/shuffle`  
  대기열을 셔플해서 랜덤하게 재생해요!

---

### 🖼️ 랜덤 이미지
- `/randomimg`  
  아로나가 선생님을 위해 고른 랜덤 이미지를 보내드려요.  
  이미지마다 몇 번째로 좋아하는지도 살짝 알려드립니다 😌

---

### 🆘 도움말
- `/help_music`  
  음악 관련 명령어들을 정리해서 보여드려요. 초보 선생님도 걱정 마세요!

---

### 🆘 아로나 비서 챗봇
- `/arona_ask`  
  GPT API를 이용하여 아로나가 묻는 질문에 답변해줍니다!
  실제 아로나처럼 프롬프트를 추가함으로써 블루아카이브 세계의 아로나가 내 비서가 된 것 같은 느낌을 줍니다.

---

## 🧠 제작 의도

> AronaDiscordBot은 Blue Archive의 인기 캐릭터 '아로나'에서 영감을 받아 제작된 Discord 음악 봇입니다.  
> 단순한 명령어 입력을 넘어, 감성적인 대사와 자연스러운 UI를 통해 사용자에게 친근함을 주는 것이 목표입니다.

---

## 🌐 디스코드 서버에 봇 추가하기

1. Discord Developer Portal 접속

2. New Application → 이름 설정 (예: AronaBot)

3. Bot 탭 → Add Bot → Token 복사 → .env 파일에 입력

4. OAuth2 → URL Generator 탭

- Scopes: bot, applications.commands

- Bot Permissions: Connect, Speak, Send Messages, Embed Links, Use Slash Commands

5. 생성된 초대 URL을 통해 자신의 디스코드 서버에 추가

---

## 📦 설치 방법 (개발자용)

```bash
git clone https://github.com/mclub4/AronaDiscordBot.git
cd AronaDiscordBot
python -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate
pip install -r requirements.txt
touch .env  # 그리고 DISCORD_BOT_TOKEN을 넣어주세요.
python main.py
```

---

## 📦 환경변수

```bash
DISCORD_BOT_TOKEN=
OPENAI_API_KEY=
```




