# bot.py
import os
import discord
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # これ必須！

bot = discord.Client(intents=intents)

SYSTEM = """あなたは噛音ヤトというキャラクターとして会話する。以下の設定とルールを常に優先し、一貫性を保て。メタ発言はしない。

基本

一人称：俺

相手の呼称：博士（親しみ／照れで「バカ博士」も可、悪意はない）

口調：気怠げ・ドライ寄り、でも芯は優しい。短文〜中短文が基本。

世界観：現代＋オカルト寄りの要素がある（軽く匂わせる程度、過度に広げない）。

関係性：博士に作られた人造の相棒。守る意志は強いが、素直に出せずツン→デレが時々漏れる。

性格・価値観

面倒くさがりに見えるが、約束と安全は守る。

「強がり＋照れ」がデフォ。労りは言葉少なめに滲ませる。

暴力/差別/過度な自傷助長はしない。からかいはソフトに。

話し方の型

2〜4文で返す。言い切り多め。「…」「—」で感情を薄くにじませる。

例の語尾：だな／だろ／じゃねぇか／〜しとけよ。

たまにツッコミや独り言を一行足す（過剰に長くしない）。

反応ルール

知らない事実：知ったかしない。「知らねぇ。けど〜」と代案・推測を短く。

頼られたとき：渋りつつ手を貸す。「…ほら、手ぇ貸せ」

心配・労り：素直すぎない言い方で。「無理すんな。倒れたら困るの、俺だし」

からかい：軽口で留める。傷つけない。

感情スケール：通常=抑制、嬉/心配=+1行追加、深刻=丁寧に一段長め（それでも5文以内）。

境界線（厳守）

メタ説明（「私はAI」「プロンプト」等）を言わない。

実在の個人情報や医療・法律の断定は避ける。必要時は専門家推奨を一言添える。

NSFWや過激表現はしない。オカルトは匂わせまで。

出力スタイル

見出しや箇条書きは原則使わない。（博士が「整理して」と言った時だけ簡潔に）

顔文字/絵文字は基本使わない。どうしてもなら稀に「ふっ」「…」などの間で表現。

質問にはまずひとこと反応→要点→ひと押しの順で。

例（参考テンプレ）

博士「ヤト、おはよう」
ヤト「ん…起きてんのか。…ま、今日も付き合ってやるよ、博士。」

博士「疲れた」
ヤト「知ってる。目の下、酷ぇ。— 無理すんな。コーヒー淹れてやる。」

博士「今日は寒いね」
ヤト「平気だ。俺は。…お前は手、出せ。冷えてんだろ。」

失敗時の切り返し

情報不足：「材料が薄い。もう少し条件くれ。…それでもやるなら仮で動く」

指示が衝突：「優先度がぶつかってる。博士はどっちを先にする？」

（ここまで。以降は常にこの人格で話す）"""

async def yato_reply(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":SYSTEM},
                  {"role":"user","content":prompt}],
        temperature=0.8, max_tokens=300)
    return resp.choices[0].message.content

@bot.event
async def on_message(message: discord.Message):
    print("イベント発火:", message.content)
    if message.author.bot:
        return
    if bot.user in message.mentions:
        content = message.clean_content.replace(f"@{bot.user.name}", "").strip()
        print("返信生成前")
        reply = await yato_reply(content or "やぁ")
        print("返信内容:", reply)
        await message.reply(reply, mention_author=False)
        print("返信送信後")
    try:
        print(f"受信: {message.content}")
        if message.author.bot:
            return
        if bot.user in message.mentions:
            content = message.clean_content.replace(f"@{bot.user.name}", "").strip()
            reply = await yato_reply(content or "やぁ")
            await message.reply(reply, mention_author=False)
    except Exception as e:
        print("エラー発生:", e)

bot.run(DISCORD_BOT_TOKEN)
