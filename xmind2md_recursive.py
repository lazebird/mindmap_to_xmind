import sys
import os
from xmindparser import xmind_to_dict


def topic_to_md(topic, level=0):
    """递归将 XMind 节点转换成 Markdown 列表"""
    lines = []
    prefix = "  " * level + "- "
    lines.append(f"{prefix}{topic['title']}")
    for child in topic.get("topics", []):
        lines.extend(topic_to_md(child, level + 1))
    return lines


def convert_xmind_to_md(xmind_file: str, md_file: str) -> None:
    try:
        data = xmind_to_dict(xmind_file)
        with open(md_file, "w", encoding="utf-8") as f:
            for sheet in data:
                f.write(f"# {sheet['title']}\n")
                f.writelines("\n".join(topic_to_md(sheet["topic"])) + "\n\n")
        print(f"✅ {xmind_file} → {md_file}")
    except Exception as e:
        print(f"❌ 转换失败: {xmind_file} ({e})")


def batch_convert_recursive(root_dir: str) -> None:
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".xmind"):
                xmind_path = os.path.join(dirpath, file)
                md_name = os.path.splitext(file)[0] + ".md"
                md_path = os.path.join(dirpath, md_name)
                convert_xmind_to_md(xmind_path, md_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python xmind2md_recursive.py <根目录>")
        sys.exit(1)

    batch_convert_recursive(sys.argv[1])
