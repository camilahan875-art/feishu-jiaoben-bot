#!/usr/bin/env python3
"""
游戏脚本模板生成器
根据分析的游戏脚本模式生成标准化的脚本模板
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
import re


class GameScriptTemplateGenerator:
    """游戏脚本模板生成器"""
    
    def __init__(self):
        self.templates = {
            '水排序订单': self._generate_water_sort_template,
            '挪车载人': self._generate_parking_template,
            '猫咪庄园': self._generate_cat_manor_template,
            '通用游戏脚本': self._generate_generic_template
        }
        
        # 游戏类型规格映射
        self.game_specs = {
            '水排序订单': {
                'dimensions': ['720 X 900', '1080 X 1920'],
                'colors': ['黄色', '蓝色', '绿色', '红色'],
                'layouts': ['螺旋排列', '星星排列', '直线排列'],
                'animations': ['倒水效果', '液体荡漾', '瓶子碰撞']
            },
            '挪车载人': {
                'dimensions': ['9:16'],
                'colors': ['彩色小车', '停车线颜色'],
                'layouts': ['弯曲停车场', '直线停车场', '多层停车场'],
                'animations': ['车辆移动', '手部点击', '音效反馈']
            },
            '猫咪庄园': {
                'dimensions': ['多尺寸适配'],
                'colors': ['马卡龙色系', '温馨色调'],
                'layouts': ['合成棋盘', '场景布局', '剧情场景'],
                'animations': ['合成动画', '表情变化', '物品飞入']
            }
        }
    
    def generate_template(self, game_type: str, title: Optional[str] = None) -> Dict:
        """
        生成游戏脚本模板
        
        Args:
            game_type: 游戏类型
            title: 脚本标题
            
        Returns:
            模板字典
        """
        if game_type in self.templates:
            template_func = self.templates[game_type]
        else:
            template_func = self.templates['通用游戏脚本']
        
        if not title:
            today = datetime.now().strftime("%y%m%d")
            title = f"{today} {game_type}素材需求"
        
        return template_func(title)
    
    def _generate_water_sort_template(self, title: str) -> Dict:
        """生成水排序订单模板"""
        template = {
            'title': title,
            'sections': [
                {
                    'title': '# 平面需求',
                    'content': self._generate_water_sort_art_section()
                },
                {
                    'title': '# 视频需求',
                    'content': self._generate_water_sort_video_section()
                }
            ],
            'metadata': {
                'game_type': '水排序订单',
                'dimensions': ['720 X 900', '1080 X 1920'],
                'color_palette': ['黄色', '蓝色', '绿色', '红色', '紫色', '橙色'],
                'special_requirements': ['液体荡漾动画', '瓶子碰撞音效', '合成完成动画']
            }
        }
        return template
    
    def _generate_parking_template(self, title: str) -> Dict:
        """生成挪车载人模板"""
        template = {
            'title': title,
            'sections': [
                {
                    'title': '# 需求表格',
                    'content': self._generate_parking_requirements_table()
                },
                {
                    'title': '# 玩法说明',
                    'content': self._generate_parking_gameplay_section()
                }
            ],
            'metadata': {
                'game_type': '挪车载人',
                'dimensions': ['9:16'],
                'color_palette': ['车辆颜色', '停车位颜色', '道路颜色'],
                'special_requirements': ['手部点击动画', '车辆移动路径', '音效反馈']
            }
        }
        return template
    
    def _generate_cat_manor_template(self, title: str) -> Dict:
        """生成猫咪庄园模板"""
        template = {
            'title': title,
            'sections': [
                {
                    'title': '# 美术制作需求',
                    'content': self._generate_cat_art_section()
                },
                {
                    'title': '# 视频制作需求',
                    'content': self._generate_cat_video_section()
                },
                {
                    'title': '# 剧情需求',
                    'content': self._generate_cat_story_section()
                }
            ],
            'metadata': {
                'game_type': '猫咪庄园',
                'dimensions': ['多尺寸适配'],
                'color_palette': ['马卡龙色系', '温馨暖色调', '明亮色调'],
                'special_requirements': ['合成动画', '表情分层', '剧情连贯性']
            }
        }
        return template
    
    def _generate_generic_template(self, title: str) -> Dict:
        """生成通用游戏脚本模板"""
        template = {
            'title': title,
            'sections': [
                {
                    'title': '# 美术资源需求',
                    'content': self._generate_generic_art_section()
                },
                {
                    'title': '# 视频制作需求',
                    'content': self._generate_generic_video_section()
                },
                {
                    'title': '# 规格说明',
                    'content': self._generate_generic_specs_section()
                }
            ],
            'metadata': {
                'game_type': '通用游戏',
                'dimensions': ['标准尺寸'],
                'color_palette': ['基础色系'],
                'special_requirements': ['基础动画', '基础音效']
            }
        }
        return template
    
    def _generate_water_sort_art_section(self) -> str:
        """生成水排序美术需求部分"""
        return """<lark-table rows="4" cols="3" header-row="true" header-column="true" column-widths="86,333,486">
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      **参考和需要的**
    </lark-td>
    <lark-td>
      **需求描述**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **平面需求**
    </lark-td>
    <lark-td>
      <grid cols="2">
        <column width="50">
          <image token="reference_1" width="521" height="931" align="center"/>
          参考布局1
        </column>
        <column width="50">
          <image token="reference_2" width="277" height="462" align="center"/>
          参考瓶子样式
        </column>
      </grid>
    </lark-td>
    <lark-td>
      1. 背景：[填写背景要求]
      2. 瓶子样式：[填写瓶子具体要求]
      3. 液体颜色：[选择颜色：黄色、蓝色、绿色等]
      4. 布局要求：[填写布局规格]
      5. 动画需求：[填写动画要求]
    </lark-td>
  </lark-tr>
</lark-table>"""
    
    def _generate_water_sort_video_section(self) -> str:
        """生成水排序视频需求部分"""
        return """<lark-table rows="3" cols="2" column-widths="100,854">
  <lark-tr>
    <lark-td>
      **视频需求**
    </lark-tr>
    <lark-tr>
    <lark-td>
      视频1
    </lark-td>
    <lark-td>
      **30秒视频脚本**
      **0-10秒：开场动画**
      - 【画面】瓶子内液体荡漾动画
      - 【音效】玻璃碰撞清脆音效
      **11-20秒：倒水过程**
      - 【画面】颜色分类倒水
      - 【动画】液体荡漾、水花效果
      **21-30秒：完成效果**
      - 【画面】合成完成动画
      - 【结束】画面模糊+logo浮现
      BGM：舒缓咖啡厅风格
    </lark-td>
  </lark-tr>
</lark-table>"""
    
    def _generate_parking_requirements_table(self) -> str:
        """生成停车场需求表格"""
        return """<lark-table rows="5" cols="4" header-row="true" header-column="true" column-widths="100,185,401,314">
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      摆放参考
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      需求1
    </lark-td>
    <lark-td>
      <image token="reference_bottom" width="749" height="1050" align="center"/>
      下半部分参考素材
      <image token="reference_top" width="548" height="292" align="center"/>
      上半部分参考素材
    </lark-td>
    <lark-td>
      参考右边图片排列停车场素材
      9:16放不下的话可以适当缩小一部分密集范围
      但是弯曲的路一定要展示出来 
    </lark-td>
    <lark-td>
      在摆放好的基础上制作游戏玩法
      出车的时候，从侧边一条进人，然后车开走
      <text bgcolor="light-yellow">玩法过程：</text>顺利出车和点击错误的车交替出现
      点击了后排车，发出撞击声
      点击了不对的颜色的车就停留在停车位上
      加手和音效
      不加bgm
    </lark-td>
  </lark-tr>
</lark-table>"""
    
    def _generate_parking_gameplay_section(self) -> str:
        """生成停车场玩法说明"""
        return """## 游戏玩法规则

1. **基本规则**：
   - 玩家需要点击正确的车辆让其开出
   - 错误的点击会导致车辆停留在停车位
   - 四个停车位全部停满视为失败

2. **动画要求**：
   - 车辆移动动画要流畅
   - 点击反馈要明显
   - 音效与动作同步

3. **视觉要求**：
   - 弯曲道路必须清晰展示
   - 彩色小人要有区分度
   - 整体布局要美观"""
    
    def _generate_cat_art_section(self) -> str:
        """生成猫咪庄园美术需求"""
        return """<lark-table rows="6" cols="4" header-row="true" header-column="true" column-widths="92,337,377,402">
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      psd参考
    </lark-td>
    <lark-td>
      psd需求
    </lark-td>
    <lark-td>
      视频需求
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      美术需求
    </lark-td>
    <lark-td>
      <grid cols="3">
        <column width="30">
          <image token="scene_reference" width="317" height="388" align="center"/>
          场景参考 
        </column>
        <column width="34">
          <image token="character_female" width="593" height="632" align="center"/>
          女性角色
        </column>
        <column width="34">
          <image token="character_male" width="737" height="795" align="center"/>
          男性角色
        </column>
      </grid>
    </lark-td>
    <lark-td>
      1. 角色：[填写角色设计要求]
      2. 场景：[填写场景设计要求]  
      3. 道具：[填写道具设计要求]
      4. 分层要求：[填写分层具体要求]
    </lark-td>
    <lark-td>
      参考视频链接
    </lark-td>
  </lark-tr>
</lark-table>"""
    
    def _generate_cat_video_section(self) -> str:
        """生成猫咪庄园视频需求"""
        return """<lark-table rows="10" cols="5" column-widths="50,116,83,400,141">
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      画面内容
    </lark-td>
    <lark-td>
      景别 {align="center"}
    </lark-td>
    <lark-td>
      画面描述
    </lark-td>
    <lark-td>
      情绪基调 {align="center"}
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      01 {align="center"}
    </lark-td>
    <lark-td>
      **场景标题**
    </lark-td>
    <lark-td>
      特写 {align="center"}
    </lark-td>
    <lark-td>
      [填写详细画面描述]
    </lark-td>
    <lark-td>
      情绪描述 {align="center"}
    </lark-td>
  </lark-tr>
</lark-table>"""
    
    def _generate_cat_story_section(self) -> str:
        """生成猫咪庄园剧情需求"""
        return """## 剧情大纲

### 故事梗概
[填写故事主要内容]

### 角色设定
1. **主角**：[主角描述]
2. **配角**：[配角描述]
3. **反派**：[反派描述]

### 场景设计
1. **主要场景**：[场景描述]
2. **过渡场景**：[场景描述]
3. **特殊场景**：[场景描述]"""
    
    def _generate_generic_art_section(self) -> str:
        """生成通用美术需求"""
        return """## 美术资源清单

### 角色设计
- [ ] 主角设计（需要分层）
- [ ] 配角设计（需要分层）
- [ ] NPC设计（需要分层）

### 场景设计  
- [ ] 主要场景
- [ ] 次要场景
- [ ] UI界面

### 道具设计
- [ ] 主要道具
- [ ] 消耗品
- [ ] 装饰品

### 特效设计
- [ ] 技能特效
- [ ] UI特效
- [ ] 场景特效"""
    
    def _generate_generic_video_section(self) -> str:
        """生成通用视频需求"""
        return """## 视频制作需求

### 时间线规划
| 时间段 | 内容 | 时长 |
|--------|------|------|
| 0-10s | 开场动画 | 10s |
| 11-30s | 核心玩法展示 | 20s |
| 31-45s | 特色功能展示 | 15s |
| 46-60s | 结尾动画 | 15s |

### 镜头要求
1. **开场镜头**：展示游戏世界
2. **玩法镜头**：清晰展示操作
3. **特色镜头**：突出游戏亮点
4. **结尾镜头**：品牌展示

### 音效要求
- BGM：风格匹配
- 音效：动作同步
- 语音：清晰自然"""
    
    def _generate_generic_specs_section(self) -> str:
        """生成通用规格说明"""
        return """## 技术规格

### 尺寸规格
- 主要尺寸：[填写尺寸]
- 适配尺寸：[填写适配要求]

### 颜色规范
- 主色调：[填写颜色]
- 辅色调：[填写颜色]
- 强调色：[填写颜色]

### 文件格式
- 图片格式：PNG（带透明通道）
- 视频格式：MP4（H.264）
- 音频格式：MP3/WAV

### 性能要求
- 文件大小限制：[填写限制]
- 加载时间要求：[填写要求]
- 兼容性要求：[填写要求]"""
    
    def create_lark_document(self, template_data: Dict) -> str:
        """
        创建飞书文档格式的内容
        
        Args:
            template_data: 模板数据
            
        Returns:
            飞书文档格式的字符串
        """
        sections = template_data['sections']
        title = template_data['title']
        
        doc_content = f"# {title}\n\n"
        
        for section in sections:
            doc_content += f"{section['title']}\n\n"
            doc_content += f"{section['content']}\n\n"
        
        # 添加元数据说明
        metadata = template_data.get('metadata', {})
        if metadata:
            doc_content += "---\n"
            doc_content += "## 规格说明\n\n"
            doc_content += f"- **游戏类型**: {metadata.get('game_type', '通用')}\n"
            doc_content += f"- **尺寸要求**: {', '.join(metadata.get('dimensions', ['标准尺寸']))}\n"
            doc_content += f"- **颜色规范**: {', '.join(metadata.get('color_palette', ['基础色系']))}\n"
            doc_content += f"- **特殊需求**: {', '.join(metadata.get('special_requirements', ['基础要求']))}\n"
        
        return doc_content
    
    def generate_from_analysis(self, analysis_result: Dict, creative_idea: str) -> Dict:
        """
        根据分析结果和创意想法生成脚本
        
        Args:
            analysis_result: 分析结果
            creative_idea: 创意想法
            
        Returns:
            生成的脚本数据
        """
        game_type = analysis_result.get('game_type', '通用游戏脚本')
        
        # 从创意想法中提取关键信息
        extracted_info = self._extract_info_from_idea(creative_idea)
        
        # 生成基础模板
        template = self.generate_template(game_type, extracted_info.get('title'))
        
        # 根据分析结果调整模板
        if 'specification_patterns' in analysis_result:
            specs = analysis_result['specification_patterns']
            self._apply_specifications(template, specs)
        
        # 应用创意想法
        self._apply_creative_idea(template, creative_idea, extracted_info)
        
        return template
    
    def _extract_info_from_idea(self, creative_idea: str) -> Dict:
        """从创意想法中提取信息"""
        info = {
            'title': None,
            'gameplay': [],
            'visuals': [],
            'story': []
        }
        
        # 提取标题（如果有）
        title_match = re.search(r'标题[：:]\s*(.+)', creative_idea)
        if title_match:
            info['title'] = title_match.group(1).strip()
        
        # 提取玩法关键词
        gameplay_keywords = ['玩法', '规则', '操作', '交互', '机制']
        for keyword in gameplay_keywords:
            if keyword in creative_idea:
                info['gameplay'].append(keyword)
        
        # 提取视觉关键词
        visual_keywords = ['画面', '美术', '风格', '颜色', '布局', '动画']
        for keyword in visual_keywords:
            if keyword in creative_idea:
                info['visuals'].append(keyword)
        
        # 提取故事关键词
        story_keywords = ['剧情', '故事', '角色', '情节', '对话']
        for keyword in story_keywords:
            if keyword in creative_idea:
                info['story'].append(keyword)
        
        return info
    
    def _apply_specifications(self, template: Dict, specifications: Dict):
        """应用规格要求到模板"""
        # 这里可以根据具体规格调整模板内容
        pass
    
    def _apply_creative_idea(self, template: Dict, creative_idea: str, extracted_info: Dict):
        """应用创意想法到模板"""
        # 这里可以将创意想法整合到模板中
        pass


def main():
    """主函数 - 用于测试"""
    generator = GameScriptTemplateGenerator()
    
    # 测试生成水排序订单模板
    template = generator.generate_template('水排序订单', '260320 水排序订单需求')
    
    print("生成的模板:")
    print(json.dumps(template, ensure_ascii=False, indent=2))
    
    # 生成飞书文档格式
    lark_doc = generator.create_lark_document(template)
    print("\n飞书文档格式:")
    print(lark_doc)


if __name__ == "__main__":
    main()