#!/usr/bin/env python3
"""
游戏脚本分析器技能初始化脚本
用于创建新的技能实例或更新现有技能
"""

import os
import sys
import json
from pathlib import Path


def init_skill(skill_name: str, output_path: str, label: str):
    """
    初始化技能目录结构
    
    Args:
        skill_name: 技能名称
        output_path: 输出目录路径
        label: 技能标签
    """
    skill_dir = Path(output_path) / skill_name
    
    # 创建目录结构
    directories = [
        skill_dir,
        skill_dir / "scripts",
        skill_dir / "references",
        skill_dir / "assets"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {directory}")
    
    # 创建SKILL.md模板
    skill_md_content = f"""---
name: {skill_name}
label: {label}
description: 专业分析游戏脚本规格，自动识别游戏类型、提取需求模式，并生成标准化的美术资源表和视频制作脚本。基于对真实游戏脚本（水排序订单、挪车载人、猫咪庄园）的分析，提供结构化解析、模板生成和规格验证功能。使用时机：1) 分析现有游戏脚本文档时，2) 根据创意想法生成新游戏脚本时，3) 验证游戏脚本规格完整性时。
---

# {label}技能

## 概述

TODO: 在这里添加技能概述

## 核心功能

TODO: 在这里描述核心功能

## 工作流程

TODO: 在这里描述工作流程

## 工具和脚本

### 主要脚本

#### `scripts/structure_parser.py`
TODO: 描述结构解析器功能

#### `scripts/template_generator.py`
TODO: 描述模板生成器功能

### 参考文档

#### `references/script_patterns.md`
TODO: 描述模式参考文档

### 资产模板

#### `assets/game_script_template.md`
TODO: 描述资产模板

## 使用场景

TODO: 在这里描述使用场景

## 游戏类型支持

TODO: 在这里列出支持的game类型

## 输出格式

TODO: 在这里描述输出格式

## 质量保证

TODO: 在这里描述质量保证措施

## 最佳实践

TODO: 在这里列出最佳实践

## 故障排除

TODO: 在这里列出常见问题和解决方案

## 扩展和定制

TODO: 在这里描述如何扩展和定制

## 版本历史

### v1.0.0 (初始版本)
- 初始技能创建
"""

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding='utf-8')
    print(f"创建文件: {skill_md_path}")
    
    # 创建示例脚本文件
    example_script = skill_dir / "scripts" / "example.py"
    example_script.write_text("""#!/usr/bin/env python3
\"\"\"
示例脚本 - 用于演示技能脚本结构
\"\"\"

def main():
    print("这是一个示例脚本")
    print("请根据实际需求修改此脚本")

if __name__ == "__main__":
    main()
""", encoding='utf-8')
    print(f"创建文件: {example_script}")
    
    # 创建示例参考文档
    example_ref = skill_dir / "references" / "example_patterns.md"
    example_ref.write_text("""# 示例模式文档

## 概述
TODO: 在这里添加模式概述

## 模式分类
TODO: 在这里描述模式分类

## 使用示例
TODO: 在这里提供使用示例

## 注意事项
TODO: 在这里列出注意事项
""", encoding='utf-8')
    print(f"创建文件: {example_ref}")
    
    # 创建示例资产文件
    example_asset = skill_dir / "assets" / "example_template.md"
    example_asset.write_text("""# 示例模板

## 概述
TODO: 在这里添加模板概述

## 模板结构
TODO: 在这里描述模板结构

## 使用说明
TODO: 在这里提供使用说明

## 变量说明
TODO: 在这里列出模板变量
""", encoding='utf-8')
    print(f"创建文件: {example_asset}")
    
    # 创建配置文件
    config = {
        "skill_name": skill_name,
        "label": label,
        "version": "1.0.0",
        "created_date": "2026-03-19",
        "author": "AI技能创建器",
        "description": "游戏脚本分析器技能"
    }
    
    config_path = skill_dir / "skill_config.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"创建文件: {config_path}")
    
    print(f"\n技能 '{skill_name}' 初始化完成！")
    print(f"技能目录: {skill_dir}")
    print("\n下一步:")
    print("1. 编辑 SKILL.md 文件，完善技能描述")
    print("2. 添加具体的脚本到 scripts/ 目录")
    print("3. 添加参考文档到 references/ 目录")
    print("4. 添加资产模板到 assets/ 目录")
    print("5. 运行 package_skill.py 打包技能")


def main():
    """主函数"""
    if len(sys.argv) < 4:
        print("用法: python init_skill.py <技能名称> <输出路径> <技能标签>")
        print("示例: python init_skill.py game-script-analyzer ./skills 游戏脚本分析器")
        return
    
    skill_name = sys.argv[1]
    output_path = sys.argv[2]
    label = sys.argv[3]
    
    init_skill(skill_name, output_path, label)


if __name__ == "__main__":
    main()