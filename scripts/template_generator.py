#!/usr/bin/env python3
"""
游戏脚本模板生成器 (AI升级版)
专门用于将 Gemini 吐出的 JSON 结构，完美排版为飞书 Markdown
"""

import json

class GameScriptTemplateGenerator:
    def __init__(self):
        pass

    def create_lark_document(self, analysis_result: dict) -> str:
        """将 AI 生成的数据转换为飞书标准 Markdown"""
        
        # 1. 提取 Gemini 吐出的核心数据字典
        ai_data = analysis_result.get('ai_semantic_analysis', {})

        if "error" in ai_data:
            return f"❌ 抱歉，创意拆解失败：{ai_data['error']}"
        if not ai_data:
            return "❌ 系统异常：未获取到大模型分析数据，请检查网络或提示词。"

        # 2. 开始 Markdown 排版组装
        doc = []
        doc.append(f"🎬 **【{ai_data.get('game_type', '买量')}】创意脑洞与素材拆解**\n")
        
        doc.append("💡 **核心创意与买量钩子**")
        doc.append(f"> **完整创意**：{ai_data.get('creative_concept', '未生成')}")
        doc.append(f"> **前3秒钩子**：**{ai_data.get('video_hook_type', '未生成')}**")
        doc.append(f"> **情绪标签**：`{ai_data.get('target_emotion', '无')}`\n")
        
        # 渲染美术需求表
        doc.append("🎨 **美术资源需求清单**")
        doc.append("| 资产类型 | 资产名称与详细描述 | 状态说明 |")
        doc.append("| :--- | :--- | :--- |")
        for art in ai_data.get('art_requirements', []):
            _type = art.get('type', '')
            _desc = art.get('name_desc', '')
            _status = art.get('status', '')
            doc.append(f"| **{_type}** | {_desc} | {_status} |")
        doc.append("\n")

        # 渲染视频脚本表
        doc.append("🎬 **视频制作分镜脚本**")
        doc.append("| 画面时长 | 分镜画面 | 旁白/音效 | 屏幕文案UI | 目的 |")
        doc.append("| :--- | :--- | :--- | :--- | :--- |")
        for script in ai_data.get('video_script', []):
            _time = script.get('time', '')
            _visual = script.get('visual', '')
            _audio = script.get('audio', '')
            _ui = script.get('text_ui', '')
            _purpose = script.get('purpose', '')
            doc.append(f"| {_time} | {_visual} | {_audio} | **{_ui}** | {_purpose} |")

        # 将列表合并成一段完整的文本返回
        return "\n".join(doc)