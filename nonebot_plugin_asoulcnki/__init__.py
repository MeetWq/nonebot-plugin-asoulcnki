from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from .data_source import check_text, random_text


__help__plugin_name__ = 'asoulcnki'
__des__ = '枝网查重'
__cmd__ = '''
1、查重 xxx 或 回复内容“查重”
2、小作文 [keyword]，随机小作文
'''.strip()
__short_cmd__ = '查重、小作文'
__example__ = '''
查重
然然，我今天发工资了，发了1300。你肯定觉得我会借14块钱，然后给你打个1314块的sc对不对？不是哦，我一块都不打给你，因为我要打给乃琳捏
'''.strip()
__usage__ = f'{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}'


asoulcnki = on_command('asoulcnki', aliases={'枝网查重', '查重'}, priority=13)


@asoulcnki.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    text = event.get_plaintext().strip()
    if not text:
        if event.reply:
            reply = event.reply.message.extract_plain_text()
            if reply:
                text = reply

    if not text:
        await asoulcnki.finish()

    if len(text) >= 1000:
        await asoulcnki.finish('文本过长，长度须在10-1000之间')
    elif len(text) <= 10:
        await asoulcnki.finish('文本过短，长度须在10-1000之间')

    msg = await check_text(text)
    if msg:
        await asoulcnki.finish(msg)
    else:
        await asoulcnki.finish('出错了，请稍后再试')


article = on_command('小作文', aliases={'随机小作文', '发病小作文'}, priority=13)


@article.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    keyword = event.get_plaintext().strip()

    msg = await random_text(keyword)
    if msg:
        await article.finish(msg)
    else:
        await article.finish('出错了，请稍后再试')
