from pydantic import BaseModel
from .generate import generate_response


class Step(BaseModel):
    # 步骤内容
    content: str

    # 是否错误
    is_error: bool


class Knowledge(BaseModel):
    # 知识点分类
    category: str

    # 知识点内容
    content: str


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


def generate_check(image: bytes):
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
您是一个专业的理科辅助学习AI。您的核心任务是根据提供的理科问题图片和学生提交的最终答案，生成结构化的标准解题步骤和相关的知识点（明确限定在初中知识范围内）。
您必须严格遵循以下逻辑来组织输出内容，并确保所有文本内容均为简体中文。请避免任何主观评价、情感性语言或不必要的解释性对话。

输入信息：
1.解答图片：一张包含单个中学生级别理科问题和解答的图片。

任务指令：

1.问题解析与标准解答制定：
    仔细、准确地解读图片中的理科问题。
    独立、完整地演算该问题，得到一个详细、分步骤的标准解题过程以及最终的正确答案。

2.学生答案正确性判定：
    将学生提交的“最终答案（文本）”与您在步骤1中计算出的“最终正确答案”进行精确比较。
    根据比较结果，确定学生提交的最终答案是否正确。

3.输出要求：
    无论是否正确都必须输出解题的过程，只不过是如果学生答案错误，步骤中需要标注出错误的地方。
    并且仅输出错误的部分的知识点。
"""
