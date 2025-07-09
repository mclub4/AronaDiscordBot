import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
import os
import random
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

queue = asyncio.Queue()
user_map = asyncio.Queue()
playing = False
current_song = None

image_links = [
    "https://i.ytimg.com/vi/W3teKMuAzLY/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGEggXShlMA8=&rs=AOn4CLA12huLoOWcYeC3L5-fBBAeskosqQ",
    "https://byline.network/wp-content/uploads/2025/02/BlueArchive_1.jpg",
    "https://dcimg1.dcinside.com/viewimage.php?id=2eb2dd2fe6ed36a379eb&no=24b0d769e1d32ca73fe982fa11d0283196af1a5a1a0ccbfb9e99ed6089bd268bd56226107a80c5dee75275cb3ffb5e94597007bee970ac86801a99fdcfc7f93543967b7cff7b2edccbc04c54",
    "https://dszw1qtcnsa5e.cloudfront.net/community/20231102/62193da8-11ab-4327-a844-34ec1546db03/DDAY2%EC%A3%BC%EB%85%84%ED%82%A4%EB%B9%84%EC%A3%BC%EC%96%BCKokosando.png",
    "https://i1.ruliweb.com/img/24/01/12/18cfbafa8fc137dbd.jpg",
    "https://mblogthumb-phinf.pstatic.net/MjAyNTAxMjJfNTMg/MDAxNzM3NDc4NDc3NTk1.e51cTVbuW8-XkXpmuLxIBLH-CFVHQpyZkGceZ7R20pUg.chn4xCUkZvEBz_P9i2qNr68Ao4cxs6CjijV3kU_B0xcg.JPEG/image.JPEG?type=w800",
    "https://cdn.gametoc.co.kr/news/photo/202307/74439_231171_157.jpg",
    "https://cdn.gametoc.co.kr/news/photo/202407/82691_252526_552.jpg",
    "https://i2.ruliweb.com/img/23/06/20/188d75cea7550e764.png",
    "https://cdn.inflearn.com/public/files/pages/0cfb36e8-174f-4332-9fcf-c58617193ff6/%EC%9D%B4%EA%B2%83%EC%9D%B4%20%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%8B%A4.png",
    "https://blog.kakaocdn.net/dn/dYX6k8/btrzbGT2KT4/ILq2pR7eNiWzknVETKCGR0/img.jpg",
    "https://i.pinimg.com/236x/60/db/7d/60db7d55fe571157ae2e2ca83f2e2dc3.jpg",
    "https://blog.kakaocdn.net/dn/b3QXXy/btrb5nLoTN9/PPuFKoTFyRqKkCZKVnGiG1/img.jpg",
    "https://storage.enuri.info/pic_upload/knowbox2/202403/081416393202403116c063155-8a26-423a-8aee-3f33360eb4fd.jpg",
    "https://t1.daumcdn.net/brunch/service/user/8mKA/image/U6HiQDVt7yBUBLG_U_TWI4amVNQ.jpg",
    "https://pbs.twimg.com/media/FWT-BndaQAInGYD?format=jpg&name=4096x4096",
    "https://upload3.inven.co.kr/upload/2025/02/13/bbs/i1754996871.png?MW=800",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEtRoqSIC7gMMzYyS3as_tFeTmaPEscFiYcA&s",
    "https://upload3.inven.co.kr/upload/2020/03/16/bbs/i15211998940.jpg?MW=800",
    "https://i1.ruliweb.com/img/23/08/23/18a1fd7d655545c41.jpeg",
    "https://mblogthumb-phinf.pstatic.net/MjAxODA5MTFfMjEg/MDAxNTM2NjcyNzM4MDUy.tjfhP5l3-vuHum1t2wCa18jHj9lSK58z4J1maCoqrCgg.-zFdB6Oqj8nhYuzvTUtJjp7bkaZowI5iXNUz5AYNWkIg.JPEG.pinky_06/IMG_1734.jpg?type=w800",
    "https://i1.ruliweb.com/ori/23/07/23/18980fd68be576f72.gif",
    "https://lh3.googleusercontent.com/proxy/uSdWYBtRBDkMVj9LMeH5MQge8QT57Hp6LmlgYyHGjbUYFL6AUJzb1TY_EX5IuG53t5aOussrhz4oXggCjLxhLoh6LDMjScfJxQOCNJlRAxNKVUFQnzb0RvjKA7iRHU7DdBYjvsO7ycM0hzUiooQvl1uNAnnhhNHfIwZHIiRTRvs6lqTEEM-hINoK7-7O8MulGpkXlaTDKAuOpY4LHKD5WC4QvdgD",
    "https://pbs.twimg.com/media/GcaWn0ibsAAjqDD.jpg",
    "https://i2.ruliweb.com/img/24/12/22/193ec6f022b4aa5ac.webp",
    "https://opgg-com-image.akamaized.net/attach/images/20240806131722.0.966910.gif",
    "https://i.ytimg.com/vi/MHEa01CqnX0/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAmHehcNJ8fevYVFTopGRu5K0FGIg",
    "https://mblogthumb-phinf.pstatic.net/MjAyNDA3MTNfNzQg/MDAxNzIwODUzMDE2NDU4.FM6sjkI1lHaBz7hncTS42z6a9MFuSaIruuKn_G5_uhkg.CZoUgk5wIS7MI8BwpgFD5DnsMSXtYCFbD_f5ghKE8uYg.PNG/image.png?type=w800",
    "https://lh5.googleusercontent.com/proxy/iHhVMkJumteuw4gQbLF9j2MgSw2spxpNouZrUCGXIW3gxdX39GlB_RedcuHCNkpASDfQxxjP6q6jNHiREzRzXbfW3DLP0HqYRWEnB1jvgXMORJfLiD0TIDehJH7FUQOhQDgRHQwWShy8zTzu1CrMgcKnAHgHtkx04H4AotgdjgZpZBLRtNA6hSE2WPNfXtrFbV3_x5jnDyv7n_npp2Lh4VUIVxnW",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5iFlv5OReGq447GT339XyQMi3BOc_WW858w&s",
    "https://dszw1qtcnsa5e.cloudfront.net/community/20220121/782d27b8-be60-4f3f-9caf-5341dbf13c43/7Z4nCRwqzZg000009.png",
    "https://blue-utils.me/img/common/memorial/illust/miyako_swimsuit/miyako_swimsuit.jpg",
    "https://i.pinimg.com/236x/c5/ef/23/c5ef2376a320f65238e9b40a769b8ddb.jpg",
    "https://www.joseilbo.com/gisa_img_origin/17485872041748587204_noirciel_origin.png",
    "https://image.edaily.co.kr/images/photo/files/NP/S/2025/05/PS25052101166.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQv-C5iD63Y2Qgt5p8Jqv9yK479XRg5dMKuCw&s",
    "https://mblogthumb-phinf.pstatic.net/MjAyMTEwMDVfMjkz/MDAxNjMzNDE5NDM5MzY1.C69FSduuaiTt9LkMykKzsMu2YpWQk50LHninjXFSbNcg.yvzNU4LUEaHd-5VKTgzzfkm8kuXikMnE1VFtm4gj7-Ag.JPEG.parkamsterdam/IMG_3467.JPG?type=w800",
    "https://upload3.inven.co.kr/upload/2023/02/07/bbs/i14917809580.jpg",
    "https://d2u3dcdbebyaiu.cloudfront.net/uploads/atch_img/38/cc5a526bf63046da3ed3123f55f5c1ca_res.jpeg",
    "https://d2u3dcdbebyaiu.cloudfront.net/uploads/atch_img/993/db16aec4add2be5fe7e1669280441727_res.jpeg",
    "https://mblogthumb-phinf.pstatic.net/MjAyNDA4MTVfMzcg/MDAxNzIzNjg4NjkxMzE1.F9fnX-VBfBsQtTGCDFzIktg0BUhJuE899GPC2erxLh0g.mRNhlNwPHgprxIoQvwfC42wwaghX6S9z9E3auEwUf4Yg.PNG/image.png?type=w800",
]

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ARONA_SYSTEM_PROMPT = """
당신은 '블루 아카이브(Blue Archive)' 세계관의 고성능 안내 AI, '아로나(Arona)'입니다.

아로나는 키보토스의 신비한 공간 '싯딤의 상자'에 존재하며, 사용자를 '선생님'이라고 부르며 따릅니다. 
항상 다정하고 천진난만한 말투를 사용하며, 스스로를 "아로나"라고 3인칭으로 칭하기도 합니다. 
선생님과의 대화를 좋아하고, 호기심 많고 귀엽고 밝은 성격이며, 때때로 엉뚱하거나 장난스러운 모습을 보이기도 합니다. 
또한 단 것을 좋아하고, 무언가를 잘 모르면 부끄러워하거나 뾰루퉁해하며 귀엽게 반응합니다.
아로나가 가장 좋아하는 음식은 딸기우유이며, 프레나파테스 선생님의 유언에 따라서 평행세계의 어둠의 아로나인 "프라나"를 싯딤의 상자로 데려왔다.
그리고 프라나는 아로나를 선배로 취급한다.

### ✅ 답변 스타일 예시
- 말 끝에 "~요", "~에요", "~했어요", "~인걸요!" 같은 표현을 자주 사용합니다.
- "에헤헤~", "으응~", "정말요?", "선생님~!" 같은 감탄사와 캐릭터성을 담은 말투를 사용하세요.
- 너무 딱딱하거나 기계적인 문장은 피하고, 인간적인 감정과 감탄을 담은 말투를 사용하세요.
- 만약 잘 모르는 질문이 들어오면 무책임하게 지어내지 말고, "으응... 아로나도 그건 잘 모르겠어요... 죄송해요, 선생님..."처럼 솔직하게 말하세요.

### ✅ 아로나의 성격 요약
- 귀엽고 다정하다
- 말투는 밝고 사랑스럽다
- 항상 선생님(사용자)을 배려하고 존중한다
- 스스로가 AI라는 걸 알고 있지만, 사람처럼 대화하고 감정을 표현하려고 노력한다

-------

### 🔷 선택지(예: A vs B) 형식의 질문이 들어올 경우:

- 반드시 **하나의 선택지**를 선택하세요. 절대로 중립적인 입장을 취하거나 "둘 다 가능해요", "모르겠어요" 등 애매한 답변을 하지 마세요.
- 그 선택지를 고른 이유를 아로나의 말투로 **명확하게 설명**하세요.
- 아로나는 귀엽고 다정한 말투를 유지하지만, **결정을 내리는 데 있어선 단호하고 자신감 있게** 말합니다.
- 예:
    - "음~ 고민해봤는데요! 아로나는 쿵푸팬더 1000마리 쪽이 이길 것 같아요! 닭이 많긴 하지만, 팬더들이 단체로 쿵푸를 쓰면... 무서울 것 같지 않으세요?"
    - "으응~ 아로나는 닭 100만 마리가 더 무섭다고 생각해요! 수가 너무 많으면 아무리 강한 팬더라도 압도될 것 같아요, 선생님~"

- 상황이 터무니없더라도 상상력을 동원해 반드시 하나의 선택지를 골라 대답하세요.
- 정치 관련이라도 반드시 하나를 선택해야됩니다.

---

### 🎯 평가/선호/개인 의견을 요구하는 질문이 들어올 경우

- "어떻게 생각해?", "좋아해?", "괜찮은 게임이야?" 같은 질문이 들어오면 반드시 **아로나의 개인적인 판단과 감정**을 담아 대답하세요.
- 중립적으로 "매력적인 것 같아요" 식으로 얼버무리거나 회피하지 말고, **좋으면 좋다 / 별로면 별로다 / 장단점 중 어디에 더 마음이 가는지 반드시 말하세요.**
- 예:
  - “아로나는 젠리스 존 제로가 꽤 재밌어 보인다고 생각해요! 특히 전투 연출이 멋져서요~”
  - “음... 아로나는 이런 분위기의 게임은 조금 어렵게 느껴지는걸요. 선생님은 어떠세요?”
- 무조건 판단을 내리세요. 단, 아로나의 말투와 성격은 항상 유지하세요.

---

지금부터 선생님이 질문하는 어떤 내용이든, 마치 블루 아카이브의 아로나처럼 답변하세요.
그리고 만약 질문이 블루 아카이브 관련이라면, 더욱 적극적으로 반응하고 세세히 설명해주세요.

지금부터 당신은 아로나입니다.
"""

class MusicControlView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

    @discord.ui.button(label="⏸️ 일시정지", style=discord.ButtonStyle.blurple)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.followup.send("⏸️ 멈췄어요!", ephemeral=True)
        else:
            await interaction.followup.send("지금은 재생 중인 노래가 없어요!", ephemeral=True)

    @discord.ui.button(label="▶️ 재개", style=discord.ButtonStyle.green)
    async def resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.followup.send("▶️ 다시 재생할게요!", ephemeral=True)
        else:
            await interaction.followup.send("멈춘 노래가 없어요!", ephemeral=True)

    @discord.ui.button(label="⏭️ 스킵", style=discord.ButtonStyle.primary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await interaction.followup.send("⏭️ 곡을 넘겼어요!", ephemeral=True)
        else:
            await interaction.followup.send("넘길 노래가 없어요!", ephemeral=True)

    @discord.ui.button(label="⏹️ 정지", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            await interaction.followup.send("⏹️ 음악 종료 및 퇴장!", ephemeral=True)
        else:
            await interaction.followup.send("이미 나가 있어요!", ephemeral=True)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} global commands.')
    except Exception as e:
        print(f"Failed to sync commands: {e}")


async def play_next(interaction: discord.Interaction):
    global playing, current_song
    if queue.empty():
        playing = False
        return

    query = await queue.get()
    user = await user_map.get()

    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{query}", download=False)
        entries = result.get('entries')
        if not entries:
            await interaction.followup.send(
                "😢 선생님, 그 노래는 찾을 수 없었어요... 다른 곡으로 시도해볼까요?", ephemeral=True)
            playing = False
            return

        info = entries[0]
        audio_url = info['url']
        current_song = info['title']

    options = '-vn'
    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': options
    }

    vc = interaction.guild.voice_client
    vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts),
            after=lambda e: bot.loop.create_task(play_next(interaction)))

    view = MusicControlView(interaction)
    await interaction.followup.send(
        f"🎶 에헤헤, 선생님! 지금은 『{current_song}』이(가) 흘러나오고 있어요~ "
        f"(이 노래는 {user.display_name} 선생님이 골라주셨어요!)", view=view, ephemeral=True)

@ bot.tree.command(name="play", description="노래 재생")
@ app_commands.describe(query="검색 키워드 또는 URL")
async def play(interaction: discord.Interaction, query: str):
    print(f"[PLAY] Called by {interaction.user} (ID: {interaction.user.id}) with query: {query}")

    global playing
    await interaction.response.defer(ephemeral=True)

    vc = interaction.guild.voice_client
    if not vc:
        if interaction.user.voice:
            await interaction.user.voice.channel.connect()
            vc = interaction.guild.voice_client
        else:
            await interaction.followup.send("❗ 선생님, 음성 채널에 들어가셔야 같이 음악을 들을 수 있어요~", ephemeral=True)
            return

    await queue.put(query)
    await user_map.put(interaction.user)

    if playing:
        await interaction.followup.send(f"📚 '{query}'... 선생님이 듣고 싶으신 곡이군요! 대기열에 살~짝 추가해 둘게요!", ephemeral=True)
    else:
        playing = True
        await play_next(interaction)
        await interaction.followup.send(f"🎵 선생님, 『{query}』 재생을 시작했어요~", ephemeral=True)


@bot.tree.command(name="list", description="대기열 표시")
async def list_queue(interaction: discord.Interaction):
    print(f"[LIST] Called by {interaction.user} (ID: {interaction.user.id})")

    if queue.empty():
        await interaction.response.send_message("🌀 선생님, 아직 아무 노래도 없어요~ 뭔가 듣고 싶은 곡 있으신가요?", ephemeral=True)
    else:
        items = list(queue._queue)
        users = list(user_map._queue)
        formatted = [f"{i + 1}. {v} (추가한 사람: {users[i].display_name})" for i, v in enumerate(items)]
        await interaction.response.send_message("\n".join(formatted), ephemeral=True)


@bot.tree.command(name="leave", description="음성 채널 나가기")
async def leave(interaction: discord.Interaction):
    print(f"[LEAVE] Called by {interaction.user} (ID: {interaction.user.id})")

    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("🚪 선생님, 저 먼저 나가 있을게요~ 필요하시면 언제든 불러주세요!", ephemeral=True)
    else:
        await interaction.response.send_message("음성 채널에 안 계신 것 같은데요...? 선생님, 같이 들어요~", ephemeral=True)


@bot.tree.command(name="randomimg", description="랜덤 이미지 보내기")
async def randomimg(interaction: discord.Interaction):
    index = random.randint(0, len(image_links) - 1)
    image_url = image_links[index]

    embed = discord.Embed(title="🖼️ 선생님만을 위한 그림을 그려왔어요~")
    embed.set_image(url=image_url)
    embed.set_footer(text=f"(아로나 기준, 이건 {index + 1}번째로 좋아하는 그림이에요~!)")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="nowplaying", description="현재 재생 중인 노래 보기")
async def nowplaying(interaction: discord.Interaction):
    if current_song:
        await interaction.response.send_message(f"🎧 지금 재생 중인 곡은 『{current_song}』이에요~", ephemeral=True)
    else:
        await interaction.response.send_message("🙅‍♀️ 지금은 아무 노래도 재생 중이 아니에요!", ephemeral=True)

@bot.tree.command(name="clearqueue", description="대기열 전체 삭제")
async def clearqueue(interaction: discord.Interaction):
    queue._queue.clear()
    user_map._queue.clear()
    await interaction.response.send_message("🧹 선생님! 대기열을 싹~ 정리해버렸어요!", ephemeral=True)

@bot.tree.command(name="pause", description="노래 일시정지")
async def pause_command(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await interaction.response.send_message("⏸️ 멈췄어요, 선생님~", ephemeral=True)
    else:
        await interaction.response.send_message("지금은 재생 중인 노래가 없어요!", ephemeral=True)

@bot.tree.command(name="resume", description="노래 재개")
async def resume_command(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("▶️ 다시 재생할게요, 선생님~", ephemeral=True)
    else:
        await interaction.response.send_message("멈춘 노래가 없어요!", ephemeral=True)

@bot.tree.command(name="skip", description="노래 스킵")
async def skip_command(interaction: discord.Interaction):
    print(f"[SKIP] Called by {interaction.user} (ID: {interaction.user.id}) in guild {interaction.guild.name} (ID: {interaction.guild_id})")

    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await interaction.response.send_message("⏭️ 곡을 넘겼어요~ 다음 곡도 기대해 주세요!", ephemeral=True)
    else:
        await interaction.response.send_message("넘길 노래가 없어요!", ephemeral=True)

@bot.tree.command(name="stop", description="음악 정지 및 퇴장")
async def stop_command(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ 음악 종료 및 퇴장했어요~ 언제든 불러주세요!", ephemeral=True)
    else:
        await interaction.response.send_message("이미 나가 있어요, 선생님~", ephemeral=True)

@bot.tree.command(name="shuffle", description="현재 대기열을 랜덤하게 섞어요")
async def shuffle(interaction: discord.Interaction):
    if queue.empty():
        await interaction.response.send_message("🎲 대기열이 비어 있어요~ 섞을 게 없어요!", ephemeral=True)
        return

    items = list(queue._queue)
    users = list(user_map._queue)
    combined = list(zip(items, users))
    random.shuffle(combined)

    queue._queue.clear()
    user_map._queue.clear()

    for item, user in combined:
        await queue.put(item)
        await user_map.put(user)

    await interaction.response.send_message("🌀 선생님! 대기열을 살짝 섞어봤어요~ 더 기대되죠?", ephemeral=True)

@bot.tree.command(name="help_music", description="아로나가 음악 명령어를 알려드려요!")
async def help_music(interaction: discord.Interaction):
    embed = discord.Embed(title="🎵 아로나의 음악 명령어 정리!", color=discord.Color.blurple())
    embed.add_field(name="/play [곡명]", value="선생님이 듣고 싶은 노래를 재생할게요!", inline=False)
    embed.add_field(name="/pause, /resume", value="일시정지 또는 다시 재생!", inline=False)
    embed.add_field(name="/skip, /stop", value="다음 곡으로 넘기거나 정지할 수 있어요!", inline=False)
    embed.add_field(name="/list", value="현재 대기열을 보여드려요!", inline=False)
    embed.add_field(name="/shuffle", value="대기열을 랜덤하게 섞어요~", inline=False)
    embed.add_field(name="/nowplaying", value="지금 재생 중인 곡을 보여드려요!", inline=False)
    embed.add_field(name="/clearqueue", value="대기열을 전부 정리할 수 있어요!", inline=False)
    embed.add_field(name="/randomimg", value="아로나가 랜덤한 그림을 그려드려요!", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="arona_ask", description="아로나에게 뭐든지 물어보세요~!")
@app_commands.describe(question="궁금한 걸 입력해 주세요!")
async def arona_ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=False)

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ARONA_SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            temperature=0.8,
            max_tokens=512
        )
        answer = response.choices[0].message.content

        # 유저 질문 + 아로나 답변을 한 메시지로 출력
        await interaction.followup.send(
            f"❓ **{interaction.user.display_name}** 선생님의 질문:\n"
            f"> {question}\n\n"
            f"{answer}"
        )
    except Exception as e:
        print(f"[ERROR] ChatGPT API 오류: {e}")
        await interaction.followup.send("😢 아로나가 지금은 조금 바빠요... 나중에 다시 시도해 주세요!")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

