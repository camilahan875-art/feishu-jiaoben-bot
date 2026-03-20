#!/usr/bin/env python3
"""
游戏脚本结构解析与创意发散器
用于自动识别、解析游戏脚本文档的组织结构，并结合大模型进行创意脑洞发散
基于分析的真实游戏脚本模式：
1. 水排序订单需求 - 颜色分类游戏
2. 挪车载人素材需求 - 停车场游戏
3. 猫咪庄园素材需求 - 合成装修游戏
"""

import re
import json
import os
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class DocumentStructure(Enum):
    """文档结构类型枚举"""
    TABLE = "table"  # 表格结构
    TIMELINE = "timeline"  # 时间线结构
    FUNCTIONAL_MODULE = "functional_module"  # 功能模块结构
    MIXED = "mixed"  # 混合结构


@dataclass
class DocumentSection:
    """文档段落信息"""
    section_type: str
    title: str
    content: str
    level: int = 1
    parent: Optional[str] = None


@dataclass
class TableStructure:
    """表格结构信息"""
    headers: List[str]
    rows: List[List[str]]
    title: Optional[str] = None
    column_widths: Optional[List[int]] = None
    row_count: Optional[int] = None
    col_count: Optional[int] = None


@dataclass
class GameScriptAnalysis:
    """游戏脚本分析结果"""
    script_title: str
    game_type: str
    structure_type: str
    total_tables: int
    total_sections: int
    file_references: List[str]
    image_references: int
    video_requirements: int
    art_requirements: int
    timeline_sections: List[Dict]
    functional_modules: List[Dict]
    tables_data: List[Dict]
    specification_patterns: Dict[str, Any]
    ai_semantic_analysis: Dict[str, Any] = None  # 新增：AI分析结果


class GameScriptStructureParser:
    """游戏脚本结构解析器 (融合基础解析与AI创意发散)"""
    
    def __init__(self, api_key: str = None):
        # ================= 原有基础规则配置 =================
        self.structure_patterns = {
            'table': [
                r'<lark-table[^>]*>.*?</lark-table>',
                r'\|.*\|',  # Markdown表格
                r'\+[-+]+\+'  # ASCII表格
            ],
            'timeline': [
                r'#\s*\d{6}',  # 日期格式标题
                r'#\s*\d+年',  # 年份标题
                r'\d{2}-\d{2}-\d{2}',  # 日期格式
            ],
            'functional_module': [
                r'#{1,3}\s*\d{6}-\d+',  # 功能模块编号
                r'#{1,3}\s*平面需求',  # 平面需求
                r'#{1,3}\s*视频需求',  # 视频需求
            ]
        }
        
        # 游戏类型识别模式
        self.game_type_patterns = {
            '水排序订单': ['颜色分类', '倒水', '货柜', '瓶子', '液体'],
            '挪车载人': ['停车场', '出车', '停车位', '车辆', '移动'],
            '猫咪庄园': ['合成', '装修', '剧情', '猫咪', '合成面板']
        }
        
        # ================= 新增 AI 大模型配置 =================
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.system_prompt = """
            你是一位资深的海外买量创意总监兼素材数据打标专家。
            你的任务是接收用户的基础创意脑洞，自动发散细节，并输出结构化的 JSON 数据。
            
            【核心要求】
            1. 极度关注“黄金前3秒钩子”，尤其是屏幕UI文字（如嘲讽文案）、失败反馈等强吸睛元素。
            2. 关注核心玩法的展示，必须带有强烈的情绪驱动标签（如 relaxing, anti stress, satisfying, offline, free 等），这对于下载量驱动极强的市场至关重要。
            
            必须严格输出纯 JSON 格式（不要加 ```json 代码块标签），必须包含以下字段：
            {
              "game_type": "推测的游戏类型(如:水排序订单/挪车/解谜等)",
              "creative_concept": "用一句话概括发散后的核心脑洞",
              "video_hook_type": "提取前3秒视频吸睛钩子描述",
              "target_emotion": "目标情绪驱动词",
              "art_requirements": [
                {"type": "核心物件/背景/UI", "name_desc": "资产名称与详细描述", "status": "需求状态(如:需新建/复用等)"}
              ],
              "video_script": [
                {"time": "0-3s", "visual": "画面表现与运镜", "audio": "音效", "text_ui": "屏幕文案钩子", "purpose": "核心目的"}
              ]
            }
            """
            self.model = genai.GenerativeModel(
                model_name='gemini-1.5-pro',
                system_instruction=self.system_prompt
            )
        else:
            self.model = None

    # ================= AI 提取方法 =================
    def generate_ai_analysis(self, content: str) -> Dict:
        """调用 Gemini Pro 进行深度语义与创意拆解"""
        if not self.model:
            return {"error": "未配置大模型 API Key"}
        try:
            # temperature=0.6 让模型有适度的创意发散能力
            response = self.model.generate_content(
                content,
                generation_config=genai.types.GenerationConfig(temperature=0.6)
            )
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return {"error": "JSON解析失败"}
        except Exception as e:
            return {"error": str(e)}

    # ================= 原有基础解析方法 =================
    def detect_structure(self, content: str) -> DocumentStructure:
        """检测文档结构类型"""
        structure_scores = {
            'table': 0,
            'timeline': 0,
            'functional_module': 0
        }
        
        for structure_type, patterns in self.structure_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
                structure_scores[structure_type] += len(matches)
        
        max_score = max(structure_scores.values())
        
        if max_score == 0:
            return DocumentStructure.MIXED
        
        dominant_structures = [
            struct for struct, score in structure_scores.items() 
            if score == max_score
        ]
        
        if len(dominant_structures) == 1:
            if dominant_structures[0] == 'table':
                return DocumentStructure.TABLE
            elif dominant_structures[0] == 'timeline':
                return DocumentStructure.TIMELINE
            elif dominant_structures[0] == 'functional_module':
                return DocumentStructure.FUNCTIONAL_MODULE
        
        return DocumentStructure.MIXED
    
    def extract_table_data(self, content: str) -> List[TableStructure]:
        """提取表格数据"""
        tables = []
        lark_table_matches = re.finditer(r'<lark-table([^>]*)>(.*?)</lark-table>', content, re.DOTALL)
        
        for match in lark_table_matches:
            table_attrs = match.group(1)
            table_html = match.group(2)
            table = self._parse_lark_table(table_html, table_attrs)
            if table:
                tables.append(table)
        
        markdown_tables = self._parse_markdown_tables(content)
        tables.extend(markdown_tables)
        return tables
    
    def _parse_lark_table(self, table_html: str, table_attrs: str) -> Optional[TableStructure]:
        """解析飞书表格"""
        try:
            attrs = {}
            attr_patterns = [
                (r'rows="(\d+)"', 'rows'),
                (r'cols="(\d+)"', 'cols'),
                (r'header-row="(true|false)"', 'header_row'),
                (r'header-column="(true|false)"', 'header_column'),
                (r'column-widths="([^"]+)"', 'column_widths')
            ]
            
            for pattern, key in attr_patterns:
                match = re.search(pattern, table_attrs)
                if match:
                    attrs[key] = match.group(1)
            
            rows = re.findall(r'<lark-tr>(.*?)</lark-tr>', table_html, re.DOTALL)
            if not rows:
                return None
            
            headers = self._extract_lark_cells(rows[0])
            data_start = 1 if attrs.get('header_row') == 'true' else 0
            data_rows = []
            
            for i in range(data_start, len(rows)):
                cells = self._extract_lark_cells(rows[i])
                if cells:
                    if attrs.get('header_column') == 'true' and len(cells) > 1:
                        data_rows.append(cells[1:])
                    else:
                        data_rows.append(cells)
            
            column_widths = None
            if 'column_widths' in attrs:
                column_widths = [int(w) for w in attrs['column_widths'].split(',')]
            
            return TableStructure(
                headers=headers,
                rows=data_rows,
                column_widths=column_widths,
                row_count=int(attrs.get('rows', len(rows))),
                col_count=int(attrs.get('cols', len(headers)))
            )
        except Exception as e:
            print(f"解析飞书表格时出错: {e}")
            return None
    
    def _extract_lark_cells(self, row_html: str) -> List[str]:
        """提取飞书表格单元格内容"""
        cells = []
        cell_matches = re.findall(r'<lark-td[^>]*>(.*?)</lark-td>', row_html, re.DOTALL)
        for cell_content in cell_matches:
            clean_content = re.sub(r'<[^>]+>', '', cell_content)
            clean_content = re.sub(r'<text[^>]*>', '', clean_content)
            clean_content = re.sub(r'</text>', '', clean_content)
            clean_content = clean_content.strip()
            cells.append(clean_content)
        return cells
    
    def _parse_markdown_tables(self, content: str) -> List[TableStructure]:
        """解析Markdown表格"""
        tables = []
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
                table_lines = []
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i].strip())
                    i += 1
                if len(table_lines) >= 2:
                    table = self._parse_markdown_table_lines(table_lines)
                    if table:
                        tables.append(table)
            else:
                i += 1
        return tables
    
    def _parse_markdown_table_lines(self, lines: List[str]) -> Optional[TableStructure]:
        """解析Markdown表格行"""
        try:
            headers = [cell.strip() for cell in lines[0].split('|') if cell.strip()]
            data_rows = []
            for line in lines[2:]:
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if cells:
                    data_rows.append(cells)
            return TableStructure(headers=headers, rows=data_rows)
        except Exception as e:
            print(f"解析Markdown表格时出错: {e}")
            return None
    
    def extract_timeline_sections(self, content: str) -> List[DocumentSection]:
        """提取时间线段落"""
        sections = []
        lines = content.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            timeline_match = re.match(r'^(#{1,6})\s*(\d{6}(?:-\d+)?)\s*(.*)', line)
            if timeline_match:
                if current_section and section_content:
                    current_section.content = '\n'.join(section_content)
                    sections.append(current_section)
                level = len(timeline_match.group(1))
                title = timeline_match.group(2) + ' ' + timeline_match.group(3)
                section_content = []
                current_section = DocumentSection(
                    section_type="timeline", title=title.strip(), content="", level=level
                )
            elif current_section:
                section_content.append(line)
                
        if current_section and section_content:
            current_section.content = '\n'.join(section_content)
            sections.append(current_section)
        return sections
    
    def extract_functional_modules(self, content: str) -> List[DocumentSection]:
        """提取功能模块段落"""
        sections = []
        lines = content.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            module_match = re.match(r'^(#{1,6})\s*([\u4e00-\u9fff]+需求)\s*(.*)', line)
            if module_match:
                if current_section and section_content:
                    current_section.content = '\n'.join(section_content)
                    sections.append(current_section)
                level = len(module_match.group(1))
                title = module_match.group(2) + module_match.group(3)
                section_content = []
                section_type = "functional_module"
                if "平面需求" in title: section_type = "art_requirements"
                elif "视频需求" in title: section_type = "video_requirements"
                
                current_section = DocumentSection(
                    section_type=section_type, title=title.strip(), content="", level=level
                )
            elif current_section:
                section_content.append(line)
                
        if current_section and section_content:
            current_section.content = '\n'.join(section_content)
            sections.append(current_section)
        return sections
    
    def detect_game_type(self, content: str) -> str:
        """检测游戏类型"""
        content_lower = content.lower()
        for game_type, keywords in self.game_type_patterns.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    return game_type
        return "未知类型"
    
    def extract_file_references(self, content: str) -> List[str]:
        """提取文件路径引用"""
        file_patterns = [
            r'\\\\[^\s]+', r'/[\w/.-]+', r'http[s]?://[^\s]+', r'\\[^\\\s]+'
        ]
        references = []
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            references.extend(matches)
        return references
    
    def extract_image_references(self, content: str) -> List[str]:
        """提取图片引用"""
        image_pattern = r'<image[^>]*token="([^"]+)"[^>]*>'
        matches = re.findall(image_pattern, content)
        return matches
    
    def generate_specification_patterns(self, content: str) -> Dict[str, Any]:
        """生成规格模式分析"""
        patterns = {
            'dimension_specs': [], 'color_specs': [], 'layout_specs': [],
            'timing_specs': [], 'animation_specs': []
        }
        
        dimension_patterns = [r'(\d+)x(\d+)', r'(\d+)\s*像素', r'(\d+)\s*px', r'宽度\s*[:：]\s*(\d+)', r'高度\s*[:：]\s*(\d+)']
        for pattern in dimension_patterns: patterns['dimension_specs'].extend(re.findall(pattern, content))
            
        color_patterns = [r'(红色|黄色|蓝色|绿色|白色|黑色|棕色)', r'RGB[A]?\s*\([^)]+\)', r'#[0-9A-Fa-f]{6}', r'饱和(度)?\s*(高|低|适中)']
        for pattern in color_patterns: patterns['color_specs'].extend(re.findall(pattern, content, re.IGNORECASE))
            
        layout_patterns = [r'(\d+)x(\d+)\s*布局', r'(\d+)\s*列', r'(\d+)\s*行', r'居中|左对齐|右对齐', r'网格\s*布局']
        for pattern in layout_patterns: patterns['layout_specs'].extend(re.findall(pattern, content))
            
        timing_patterns = [r'(\d+)秒', r'(\d+)-(\d+)秒', r'(\d+)[sS]', r'时长\s*[:：]\s*(\d+)']
        for pattern in timing_patterns: patterns['timing_specs'].extend(re.findall(pattern, content))
            
        return patterns

    # ================= 核心分析方法 =================
    def analyze_document_structure(self, content: str) -> Dict:
        """
        全面分析文档结构
        融合基础文档解析与 AI 脑洞创意拆解
        """
        structure_type = self.detect_structure(content)
        
        analysis_result = {
            'structure_type': structure_type.value,
            'game_type': self.detect_game_type(content),
            'tables': [],
            'timeline_sections': [],
            'functional_modules': [],
            'file_references': self.extract_file_references(content),
            'image_references': self.extract_image_references(content),
            'statistics': {
                'total_tables': 0,
                'total_timeline_sections': 0,
                'total_functional_modules': 0,
                'document_length': len(content),
                'file_references_count': 0,
                'image_references_count': 0
            }
        }
        
        # 1. 提取基础信息
        tables = self.extract_table_data(content)
        analysis_result['tables'] = [
            {
                'headers': table.headers, 'rows': table.rows, 'title': table.title,
                'column_widths': table.column_widths, 'row_count': table.row_count, 'col_count': table.col_count
            }
            for table in tables
        ]
        analysis_result['statistics']['total_tables'] = len(tables)
        
        timeline_sections = self.extract_timeline_sections(content)
        analysis_result['timeline_sections'] = [{'section_type': s.section_type, 'title': s.title, 'content_length': len(s.content), 'level': s.level} for s in timeline_sections]
        analysis_result['statistics']['total_timeline_sections'] = len(timeline_sections)
        
        functional_modules = self.extract_functional_modules(content)
        analysis_result['functional_modules'] = [{'section_type': s.section_type, 'title': s.title, 'content_length': len(s.content), 'level': s.level} for s in functional_modules]
        analysis_result['statistics']['total_functional_modules'] = len(functional_modules)
        
        analysis_result['statistics']['file_references_count'] = len(analysis_result['file_references'])
        analysis_result['statistics']['image_references_count'] = len(analysis_result['image_references'])
        
        # 2. 调用大模型进行 AI 创意拆解 (合并到最终结果中)
        if self.model:
            print("⏳ 正在调用 Gemini 引擎进行创意发散与拆解...")
            ai_data = self.generate_ai_analysis(content)
            analysis_result['ai_semantic_analysis'] = ai_data
            
            # 智能覆写：如果AI识别出了更精准的游戏类型，则优先使用AI的
            if ai_data and 'game_type' in ai_data and ai_data['game_type'] != "未知类型":
                analysis_result['game_type'] = ai_data['game_type']
        else:
            analysis_result['ai_semantic_analysis'] = {"error": "未配置大模型 API Key"}
            
        return analysis_result


def main():
    """主函数 - 用于测试"""
    # 如果想测试 AI 功能，请把你的 Gemini API Key 写在下面
    TEST_API_KEY = "" 
    
    parser = GameScriptStructureParser(api_key=TEST_API_KEY)
    
    # 示例内容：我们喂给它一个包含基础想法的段落
    sample_content = """
    # 260312 水排序创意测试
    帮我想个星星排列大试管的脑洞。一开始倒错水，试管上面写着嘲讽玩家的 you are the shit。
    然后立刻展示极速倾倒通关，重点要让人感觉非常解压和顺畅。
    
    <lark-table rows="2" cols="2" header-row="true" header-column="true">
      <lark-tr><lark-td>美术需求</lark-td><lark-td>psd参考</lark-td></lark-tr>
      <lark-tr><lark-td>大试管</lark-td><lark-td>参考图片.png</lark-td></lark-tr>
    </lark-table>
    """
    
    # 分析文档结构并调用 AI 发散
    result = parser.analyze_document_structure(sample_content)
    
    print("\n" + "="*40)
    print("📊 基础结构解析结果:")
    print(f"结构类型: {result['structure_type']}")
    print(f"识别游戏类型: {result['game_type']}")
    print(f"表格数量: {result['statistics']['total_tables']}")
    
    print("\n" + "="*40)
    print("🧠 Gemini AI 深度语义解析结果:")
    if 'ai_semantic_analysis' in result:
        print(json.dumps(result['ai_semantic_analysis'], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()