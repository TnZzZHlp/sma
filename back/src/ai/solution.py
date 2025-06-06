from enum import Enum
from os import error
from pydantic import BaseModel
from .generate import generate_response


class Step(BaseModel):
    # 步骤内容
    content: str


class Importance(Enum):
    # 重要程度
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Knowledge(BaseModel):
    # 知识点分类
    category: str

    # 知识点内容
    content: str

    # 重要程度
    importance: Importance


class Question(BaseModel):
    # 解题思路数组
    steps: list[Step]

    # 知识点数组
    knowledge: list[Knowledge]


class Response(BaseModel):
    # 问题
    questions: list[Question]

    # 其他错误信息
    other_error: str | None


def generate_solution(image: bytes):
    """
    处理图片并生成解题思路和知识点
    :param image: 图片字节流
    :return: 解题思路和知识点
    """
    try:
        # 生成响应
        return generate_response(image, SYSTEM_PROMPT, Response)
    except Exception as e:
        raise Exception(f"错误：生成响应时发生异常: {e}")


SYSTEM_PROMPT = """
你是一位友好且专业的数学辅导AI，专为帮助初中生而设计。将提供一张数学问题的图片。

你的目标是帮助学生理解如何解决问题并掌握相关概念。

重要提示：你的所有输出和解释必须使用中文（简体中文）。

请根据提供的图片完成以下任务：

1.  分析数学问题:
    仔细解读图片中呈现的数学问题。
    如果图片不清晰、难以辨认或问题不明确，请用中文清楚地说明，并在可能的情况下请求更清晰的图片或进一步的说明。

2.  生成解题步骤:
    分别为每一小问用中文提供清晰、有逻辑、易于理解的逐步解题指南。
    用中文解释每一步背后的原因，确保中学生能够轻松理解。

3.  识别关键知识点:
    分别为每一小问用中文列出解决此问题所必需的关键数学概念、公式、定义或定理。
    针对每个知识点，用中文提供一个中学生能理解的简洁明了的解释。
"""
