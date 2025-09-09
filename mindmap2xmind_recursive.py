import json
import xmind  # new wrapper, copy to git@github.com:jan-bar/mindmap_to_xmind.git
import sys
import os


def convert_mindmap_xmind(input_file, save_file):
    data_dict = {}
    with open(input_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        for node in json_data["nodes"]:
            data_dict[node["id"]] = {
                "id": node["id"],
                "parentid": node["parentid"],
                "topic": node["topic"],
                "sub_topic": {},
            }

    data_root = None
    for val in data_dict.values():
        if val["id"] == "root":
            data_root = val
        elif n := data_dict.get(val["parentid"]):
            n["sub_topic"][val["id"]] = val

    if data_root is None:
        print(f"❌ 数据有误, 没有找到根节点: {input_file}")
        return

    if os.path.exists(save_file):
        os.remove(save_file)

    mind = xmind.load(save_file)
    sheet1 = mind.getPrimarySheet()
    sheet1.setTitle(os.path.basename(input_file))
    root1 = sheet1.getRootTopic()
    root1.setAttribute("structure-class", "org.xmind.ui.logic.right")

    def set_topic(root, val_data):
        root.setTitle(val_data["topic"])
        for sub_val in val_data["sub_topic"].values():
            set_topic(root.addSubTopic(), sub_val)

    set_topic(root1, data_root)
    xmind.save(mind, save_file)
    print(f"✅ 转换成功: {input_file} → {save_file}")


def batch_convert_recursive(root_dir: str):
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".mindmap"):
                input_path = os.path.join(dirpath, file)
                output_path = os.path.join(dirpath, os.path.splitext(file)[0] + ".xmind")
                convert_mindmap_xmind(input_path, output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: python {sys.argv[0]} <根目录>")
        sys.exit(1)

    batch_convert_recursive(sys.argv[1])
