import io
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

client = None


# 读取.env文件
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    print("错误：未在 .env 文件中找到 GOOGLE_API_KEY")
    exit(1)


def generate_response(image, system_prompt, struct):
    """生成响应"""

    # 转换图片为JPEG格式
    image_bytes: bytes

    # 转换图片为JPEG格式并获取字节
    try:
        # 假设 image_input 是一个文件路径或一个类文件对象
        image = Image.open(io.BytesIO(image))

        # 确保图像是RGB模式，JPEG通常需要这个
        if image.mode != "RGB":
            image = image.convert("RGB")

        # 创建一个内存中的字节流
        byte_buffer = io.BytesIO()
        # 将图片以JPEG格式保存到字节流中
        image.save(byte_buffer, format="JPEG")
        # 获取字节流的内容
        image_bytes = byte_buffer.getvalue()

        if not image_bytes:
            raise Exception("错误：转换后的图片数据无效")

    except Exception as e:
        # 更具体的错误信息
        raise Exception(f"错误：处理图片时发生异常: {e}")

    try:
        response = client.models.generate_content_stream(  # type: ignore
            model="gemini-2.5-flash-preview-04-17",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                thinking_config=types.ThinkingConfig(
                    include_thoughts=False,
                    thinking_budget=0,
                ),
                response_mime_type="application/json",
                response_schema=struct,
            ),
        )

        # 检查响应是否有效
        if not response:
            raise Exception("错误：响应无效")

        # 处理响应
        return response

    except Exception as e:
        raise Exception(f"错误：生成响应时发生异常: {e}")
