import json
import time
import httpx
import base64
import jinja2
from pathlib import Path
from nonebot.adapters.cqhttp import Message, MessageSegment

from .browser import get_new_page
from .diff import diff_text

dir_path = Path(__file__).parent
template_path = dir_path / 'template'
env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),
                         enable_async=True)


async def check_text(text):
    try:
        url = 'https://asoulcnki.asia/v1/api/check'
        async with httpx.AsyncClient() as client:
            resp = await client.post(url=url, data=json.dumps({'text': text}))
            result = resp.json()

        code = result['code']
        if code != 0:
            return None

        data = result['data']
        if not data['related']:
            return '没有找到重复的小作文捏'

        rate = data['rate']
        related = data['related'][0]
        reply_url = related['reply_url'].strip()
        reply = related['reply']
        ctime = reply['ctime']

        article = {}
        article['username'] = reply['m_name']
        article['like'] = reply['like_num']
        article['all_like'] = reply['similar_like_sum']
        article['quote'] = reply['similar_count']
        article['text'] = diff_text(text, reply['content'])
        article['time'] = time.strftime("%Y-%m-%d", time.localtime(ctime))

        image = await create_image(article)
        if not image:
            return None

        msg = Message()
        msg.append('总复制比 {:.2f}%'.format(rate * 100))
        msg.append(MessageSegment.image(
            f"base64://{base64.b64encode(image).decode()}"))
        msg.append(f'链接：{reply_url}')
        return msg
    except:
        return None


async def create_image(article):
    template = env.get_template('article.html')
    content = await template.render_async(article=article)
    async with get_new_page(viewport={"width": 500, "height": 100}) as page:
        await page.set_content(content)
        img = await page.screenshot(full_page=True)
    return img
