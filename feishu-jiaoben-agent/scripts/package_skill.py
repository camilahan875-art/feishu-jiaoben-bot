#!/usr/bin/env python3
"""
游戏脚本分析器技能打包脚本
用于验证和打包技能为.skill文件
"""

import os
import sys
import json
import zipfile
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class SkillPackager:
    """技能打包器"""
    
    def __init__(self):
        self.required_files = ["SKILL.md"]
        self.required_dirs = ["scripts", "references", "assets"]
        self.supported_extensions = [".py", ".md", ".json", ".txt", ".yaml", ".yml"]
    
    def validate_skill(self, skill_path: Path) -> List[str]:
        """
        验证技能结构
        
        Args:
            skill_path: 技能目录路径
            
        Returns:
            错误消息列表，空列表表示验证通过
        """
        errors = []
        
        # 检查技能目录是否存在
        if not skill_path.exists():
            errors.append(f"技能目录不存在: {skill_path}")
            return errors
        
        if not skill_path.is_dir():
            errors.append(f"技能路径不是目录: {skill_path}")
            return errors
        
        # 检查必需文件
        for required_file in self.required_files:
            file_path = skill_path / required_file
            if not file_path.exists():
                errors.append(f"缺少必需文件: {required_file}")
        
        # 检查SKILL.md的YAML frontmatter
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            frontmatter_errors = self._validate_skill_md(skill_md_path)
            errors.extend(frontmatter_errors)
        
        # 检查目录结构
        for required_dir in self.required_dirs:
            dir_path = skill_path / required_dir
            if not dir_path.exists():
                # 目录不存在不是错误，只是警告
                print(f"警告: 推荐目录不存在: {required_dir}")
        
        return errors
    
    def _validate_skill_md(self, skill_md_path: Path) -> List[str]:
        """验证SKILL.md文件的YAML frontmatter"""
        errors = []
        
        try:
            content = skill_md_path.read_text(encoding='utf-8')
            
            # 检查是否有YAML frontmatter
            if not content.startswith('---\n'):
                errors.append("SKILL.md必须以YAML frontmatter开始（---）")
                return errors
            
            # 提取YAML部分
            parts = content.split('---\n', 2)
            if len(parts) < 3:
                errors.append("SKILL.md必须包含完整的YAML frontmatter（开始和结束标记）")
                return errors
            
            yaml_content = parts[1]
            
            # 解析YAML
            frontmatter = yaml.safe_load(yaml_content)
            
            # 检查必需字段
            required_fields = ["name", "label", "description"]
            for field in required_fields:
                if field not in frontmatter:
                    errors.append(f"SKILL.md frontmatter缺少必需字段: {field}")
            
            # 检查字段内容
            if "name" in frontmatter and not frontmatter["name"]:
                errors.append("SKILL.md frontmatter中name字段不能为空")
            
            if "label" in frontmatter and not frontmatter["label"]:
                errors.append("SKILL.md frontmatter中label字段不能为空")
            
            if "description" in frontmatter and not frontmatter["description"]:
                errors.append("SKILL.md frontmatter中description字段不能为空")
            
            # 检查描述长度
            if "description" in frontmatter:
                desc = frontmatter["description"]
                if len(desc) < 50:
                    errors.append("SKILL.md description字段应至少50个字符，详细描述技能用途")
            
        except yaml.YAMLError as e:
            errors.append(f"SKILL.md YAML解析错误: {e}")
        except Exception as e:
            errors.append(f"SKILL.md验证错误: {e}")
        
        return errors
    
    def package_skill(self, skill_path: Path, output_dir: Optional[Path] = None) -> Optional[Path]:
        """
        打包技能
        
        Args:
            skill_path: 技能目录路径
            output_dir: 输出目录路径（可选）
            
        Returns:
            打包后的.skill文件路径，失败返回None
        """
        # 验证技能
        errors = self.validate_skill(skill_path)
        if errors:
            print("技能验证失败:")
            for error in errors:
                print(f"  - {error}")
            return None
        
        # 确定输出目录
        if output_dir is None:
            output_dir = skill_path.parent
        
        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 确定技能名称
        skill_name = skill_path.name
        
        # 创建.skill文件路径
        skill_file = output_dir / f"{skill_name}.skill"
        
        try:
            # 创建zip文件
            with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 添加所有文件
                for root, dirs, files in os.walk(skill_path):
                    # 跳过隐藏文件和目录
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    files = [f for f in files if not f.startswith('.')]
                    
                    for file in files:
                        file_path = Path(root) / file
                        
                        # 检查文件扩展名
                        if file_path.suffix not in self.supported_extensions:
                            print(f"警告: 跳过不支持的文件类型: {file}")
                            continue
                        
                        # 计算相对路径
                        rel_path = file_path.relative_to(skill_path)
                        
                        # 添加到zip
                        zipf.write(file_path, rel_path)
                        print(f"添加文件: {rel_path}")
            
            print(f"\n技能打包成功!")
            print(f"技能文件: {skill_file}")
            print(f"文件大小: {skill_file.stat().st_size / 1024:.2f} KB")
            
            # 显示技能信息
            self._display_skill_info(skill_path)
            
            return skill_file
            
        except Exception as e:
            print(f"打包失败: {e}")
            if skill_file.exists():
                skill_file.unlink()
            return None
    
    def _display_skill_info(self, skill_path: Path):
        """显示技能信息"""
        skill_md_path = skill_path / "SKILL.md"
        
        if skill_md_path.exists():
            try:
                content = skill_md_path.read_text(encoding='utf-8')
                parts = content.split('---\n', 2)
                
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    frontmatter = yaml.safe_load(yaml_content)
                    
                    print("\n技能信息:")
                    print(f"  名称: {frontmatter.get('name', '未知')}")
                    print(f"  标签: {frontmatter.get('label', '未知')}")
                    
                    desc = frontmatter.get('description', '')
                    if len(desc) > 100:
                        desc = desc[:97] + "..."
                    print(f"  描述: {desc}")
            except:
                pass
        
        # 统计文件
        total_files = 0
        for root, dirs, files in os.walk(skill_path):
            # 跳过隐藏文件和目录
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            total_files += len(files)
        
        print(f"  总文件数: {total_files}")
        
        # 检查目录
        for required_dir in self.required_dirs:
            dir_path = skill_path / required_dir
            if dir_path.exists():
                dir_files = len([f for f in dir_path.iterdir() if not f.name.startswith('.')])
                print(f"  {required_dir}/: {dir_files} 个文件")
            else:
                print(f"  {required_dir}/: (不存在)")
    
    def extract_skill(self, skill_file: Path, output_dir: Path) -> Optional[Path]:
        """
        解压.skill文件
        
        Args:
            skill_file: .skill文件路径
            output_dir: 输出目录路径
            
        Returns:
            解压后的技能目录路径，失败返回None
        """
        if not skill_file.exists():
            print(f"技能文件不存在: {skill_file}")
            return None
        
        if skill_file.suffix != '.skill':
            print(f"文件扩展名不是.skill: {skill_file}")
            return None
        
        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 解压文件
            with zipfile.ZipFile(skill_file, 'r') as zipf:
                # 获取技能名称（从第一个文件的路径推断）
                file_list = zipf.namelist()
                if not file_list:
                    print("技能文件为空")
                    return None
                
                # 假设第一个文件在技能根目录
                first_file = Path(file_list[0])
                if len(first_file.parts) > 1:
                    skill_name = first_file.parts[0]
                else:
                    skill_name = skill_file.stem
                
                # 解压到技能目录
                skill_dir = output_dir / skill_name
                zipf.extractall(skill_dir)
                
                print(f"技能解压成功!")
                print(f"技能目录: {skill_dir}")
                
                # 验证解压后的技能
                errors = self.validate_skill(skill_dir)
                if errors:
                    print("警告: 解压后的技能验证失败:")
                    for error in errors:
                        print(f"  - {error}")
                
                return skill_dir
                
        except Exception as e:
            print(f"解压失败: {e}")
            return None


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python package_skill.py <技能目录路径> [输出目录路径]")
        print("示例: python package_skill.py ./game-script-analyzer")
        print("示例: python package_skill.py ./game-script-analyzer ./dist")
        return
    
    skill_path = Path(sys.argv[1])
    
    if len(sys.argv) >= 3:
        output_dir = Path(sys.argv[2])
    else:
        output_dir = None
    
    packager = SkillPackager()
    
    # 检查是打包还是解压
    if skill_path.suffix == '.skill':
        # 解压模式
        if output_dir is None:
            output_dir = skill_path.parent / "extracted"
        
        print(f"解压技能: {skill_path}")
        print(f"输出到: {output_dir}")
        
        extracted_dir = packager.extract_skill(skill_path, output_dir)
        if extracted_dir:
            print(f"技能已解压到: {extracted_dir}")
        else:
            print("技能解压失败")
    else:
        # 打包模式
        print(f"打包技能: {skill_path}")
        
        if output_dir:
            print(f"输出到: {output_dir}")
        
        skill_file = packager.package_skill(skill_path, output_dir)
        if skill_file:
            print(f"技能已打包为: {skill_file}")
        else:
            print("技能打包失败")


if __name__ == "__main__":
    main()