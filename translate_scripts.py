import os
import glob
import re
import asyncio
import aiofiles
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key="", base_url="https://api.deepseek.com")

translate_prompt = """把下面的技术文档内容翻译地道、流畅自然的中文，文档中提到的人名和技术或其他常见名词不进行翻译，必须符合中文表达习惯，必须使用和原文排版一致的markdown格式输出。"""


def is_chinese(text):
    sample = text[:100]
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', sample)
    # 是否存在中文字符
    ratio = len(chinese_chars)
    return ratio > 1

async def translate_text(text):
    prompt = translate_prompt + f"```{text}```"
    messages = [{"role": "user", "content": prompt}]
    response = await client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True
    )

    translated = ""
    reasoning_content = ""
    async for chunk in response:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            translated += delta.content
        if hasattr(delta, "reasoning_content") and delta.reasoning_content:
            reasoning_content += delta.reasoning_content
            print(f"🔍 推理内容: {reasoning_content}")
    return translated

async def process_file(file_path, semaphore):
    async with semaphore:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()

        if is_chinese(content):
            return  # 跳过中文文件

        print(f"🔄 正在翻译: {file_path}")
        try:
            translated = await translate_text(content)
            # 处理翻译结果
            match = re.search(r'```markdown\s*(.*?)\s*```', translated, re.DOTALL)
            markdown = match.group(1) if match else translated
            # 保存翻译内容（覆盖原文件）
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(markdown)

            print(f"✅ 翻译完成并保存: {file_path}")
        except Exception as e:
            print(f"❌ 处理失败: {file_path}，错误: {e}")
            return

        # 删除源文件（已经覆盖，此处可略）
        # os.remove(file_path)  # 如不想覆盖原文件可改为新文件名后保留旧文件

def find_md_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return glob.glob(os.path.join(current_dir, '**', '*.md'), recursive=True)

async def main():
    md_files = find_md_files()
    semaphore = asyncio.Semaphore(8)  # 限制最多8个并发任务
    tasks = [process_file(fp, semaphore) for fp in md_files]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
