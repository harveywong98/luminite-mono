import sys
import os
from fontTools.ttLib import TTFont

def ensure_dir(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)

def process_font(input_path, output_path):
    """
    加载字体，(未来在此处添加整合逻辑)，然后保存
    """
    try:
        font = TTFont(input_path)
        
        # --- 这里的空间留给未来的整合逻辑 ---
        # 例如: font_merger.merge(font, other_font)
        # --------------------------------

        # 获取字体名称用于日志
        name = font['name'].getDebugName(1) or "Unknown"
        print(f"正在处理: {name} -> {os.path.basename(output_path)}")
        
        font.save(output_path)
        
    except Exception as e:
        print(f"处理 {input_path} 时发生错误: {e}")
        # 在流水线中，通常希望遇到错误就停止，或者记录错误
        raise e

def main():
    # 定义路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 指向 submodule 中预编译好的官方字体文件作为基底
    # 我们基于这些成品进行 Patch，而不是从 sources/ 目录下的 .ufo 源码重新构建
    source_dir = os.path.join(project_root, "upstream", "ibm-plex", "packages", "ibm-plex-mono", "fonts", "complete", "ttf")
    dist_dir = os.path.join(project_root, "dist")

    ensure_dir(dist_dir)

    # 扫描源目录下的所有 .ttf 文件
    if os.path.exists(source_dir) and os.listdir(source_dir):
        for filename in os.listdir(source_dir):
            if filename.lower().endswith(".ttf"):
                input_path = os.path.join(source_dir, filename)
                output_path = os.path.join(dist_dir, filename)
                process_font(input_path, output_path)
    else:
        print(f"错误: 找不到源文件，目录为空或不存在: {source_dir}")
        print("提示: 请尝试运行 'git submodule update --init --recursive' 拉取上游代码")
        sys.exit(1)

    print("构建完成。产物位于 dist/ 目录。")

if __name__ == "__main__":
    main()
