# W3 生词表 CSV -> 自动生成练习题
# 运行：python vocab_tool.py
# 本周扩展：① 按词性分组输出；② 读《愚公移山》语料自动出填空题。
import os
import csv
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  统一解析 data/ 路径，换目录也不会找不到文件

DATA = weekpath.data_path("生词表.csv")
CORPUS = weekpath.data_path("愚公移山.txt")  # 扩展②的语料来源


def load_words(path=DATA):
    """① 读：csv.DictReader 把每一行读成字典，表头就是键名（KeyError 的第一大来源）。"""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def filter_by_level(words, level="4"):
    """② 筛：列表推导式，只留 HSK 等级等于 level 的词。"""
    return [w for w in words if str(w["HSK等级"]) == str(level)]


def count_by_pos(words):
    """③ 统：用 dict.get 数每种词性出现几次。"""
    d = {}
    for w in words:
        d[w["词性"]] = d.get(w["词性"], 0) + 1
    return d


def group_by_pos(words):
    """扩展①：按词性分组，返回 {词性: [词汇, ...]}。用 dict.setdefault 省掉判空。"""
    groups = {}
    for w in words:
        groups.setdefault(w["词性"], []).append(w["词汇"])
    return groups


def find_sentence_with(text, word):
    """在《愚公移山》里找到含 word 的那一行，返回 (原句, 挖空句)；找不到返回 (None, None)。"""
    for line in text.split("\n"):
        line = line.strip()
        # 跳过标题行、出处行、教学提示行
        if not line or line.startswith("【") or line.startswith("-") or line.startswith("《"):
            continue
        if word in line:
            return line, line.replace(word, "＿＿＿＿", 1)
    return None, None


def gen_sentence_exercises(words, out=None):
    """基础交付：造句题，每行一道。"""
    out = out or weekpath.root_path("练习.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("=" * 46 + "\n")
        f.write("一、造句题（用指定词语造一个句子）\n")
        f.write("=" * 46 + "\n\n")
        for w in words:
            f.write(f"用“{w['词汇']}”造一个句子。（{w['词性']}；{w['释义']}）\n")
    return out


def gen_fill_blanks(words, out=None):
    """扩展②：填空题。在《愚公移山》原文/白话里找到含目标词的句子，把词挖空成 ＿＿＿＿。"""
    out = out or weekpath.root_path("填空练习.txt")
    with open(CORPUS, encoding="utf-8") as f:
        text = f.read()

    picked = []  # (词字典, 挖空句)，保持顺序
    seen = set()
    for w in words:
        if w["词汇"] in seen:
            continue
        _, blanked = find_sentence_with(text, w["词汇"])
        if blanked:
            picked.append((w, blanked))
            seen.add(w["词汇"])

    with open(out, "w", encoding="utf-8") as f:
        f.write("=" * 46 + "\n")
        f.write("二、填空题（读《愚公移山》上下文，把 ＿＿＿＿ 处补成原词）\n")
        f.write("=" * 46 + "\n\n")
        for i, (w, blanked) in enumerate(picked, 1):
            f.write(f"{i}. {blanked}\n")
            f.write(f"   【答案】{w['词汇']}（{w['词性']}，HSK{w['HSK等级']}：{w['释义']}）\n\n")
    return out, len(picked)


def report_groups(words):
    """扩展①：把 HSK4 词按词性分组打印到屏幕。"""
    groups = group_by_pos(words)
    print("\n按词性分组：")
    for pos, ws in groups.items():
        print(f"  【{pos}】{len(ws)} 个：{'、'.join(ws)}")


if __name__ == "__main__":
    words = load_words()
    lv4 = filter_by_level(words, "4")
    print(f"总词汇 {len(words)} 个，其中 HSK4 词汇 {len(lv4)} 个")
    print(f"词性分布：{count_by_pos(lv4)}")
    report_groups(lv4)

    out1 = gen_sentence_exercises(lv4)
    print(f"\n已生成造句练习：{out1}")

    out2, n = gen_fill_blanks(words)
    print(f"已生成填空练习：{out2}（共 {n} 道，来自《愚公移山》原句）")