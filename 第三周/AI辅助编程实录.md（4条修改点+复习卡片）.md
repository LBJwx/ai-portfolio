# W3 AI 辅助编程实录

> 课程：《人工智能在学习环境中的应用与实践》· 第3周 Python 速成
> 纪律：AI 写初稿，我逐行读懂并改；不粘贴不理解的代码。

---

## 一、我给 AI 的提示词（四件套）

```
角色：你是我的 Python 教学结对助手。
任务：帮我写一个脚本 vocab_tool.py，读 data/生词表.csv，
      按 HSK 等级筛词、统计词性分布，然后在根目录生成 练习.txt。
要求：
  1. 只用 Python 标准库（csv / os），不要装第三方包；
  2. 中文读写一律 encoding="utf-8"；
  3. 每行加注释，说明这行在干什么；
  4. 示例输出：用"坚持"造一个句子。（动词）
```

## 二、AI 给我的初版代码（节选，未改前）

```python
import csv

words = list(csv.DictReader(open("data/生词表.csv")))
lv4 = [w for w in words if w["HSK等级"] == "4"]

d = {}
for w in lv4:
    d[w["词性"]] = d.get(w["词性"], 0) + 1
print("词性分布：", d)

with open("练习.txt", "w") as f:
    for w in lv4:
        f.write("用\"%s\"造一个句子。（%s）\n" % (w["词汇"], w["词性"]))
```

## 三、我改了什么、为什么（4 条）

### 修改点 1：路径写死 → 用 weekpath 统一解析
- **AI 初版**：`open("data/生词表.csv")`、`open("练习.txt", "w")`，路径全是相对当前目录。
- **我的改法**：改成 `weekpath.data_path("生词表.csv")` 和 `weekpath.root_path("练习.txt")`。
- **为什么**：PPT 第 10 页讲过——"从哪个目录运行都行"是硬约定；AI 写的相对路径，一旦我在别的文件夹下 `python week03_Python/vocab_tool.py`，CSV 就找不到、练习.txt 还会被甩到奇怪的地方。

### 修改点 2：漏掉 encoding → 补 utf-8
- **AI 初版**：`open(...)` 没写 `encoding=`。
- **我的改法**：所有 `open(...)` 一律加 `encoding="utf-8"`（读和写都加）。
- **为什么**：我自己 Windows 上默认是 GBK，读中文 CSV 会直接 `UnicodeDecodeError`；PPT 第 7 页"常见报错"里专门列了这一条。

### 修改点 3：一坨平铺代码 → 拆成 4 个函数各管一件事
- **AI 初版**：全部写在主流程里，一打开就是十几行连在一起。
- **我的改法**：拆成 `load_words / filter_by_level / count_by_pos / gen_sentence_exercises`，每个函数只做一件事。
- **为什么**：PPT 第 5 页"四个语法点"里专门讲了 `def`——函数是"把动作打包、后面反复调用"。拆完之后我要加"按词性分组"只要再写一个 `group_by_pos()`，不动老代码。

### 修改点 4（作业 1 新学写法）：% 格式化 → f-string；并用 str.replace() 实现填空题
- **AI 初版**：`"用\"%s\"造一个句子。（%s）\n" % (w["词汇"], w["词性"])`。
- **我的改法**：
  1. 字符串全部改成 f-string：`f"用“{w['词汇']}”造一个句子。（{w['词性']}；{w['释义']}）"`；
  2. 新增 `gen_fill_blanks()`：读《愚公移山》原文，用 `line.replace(word, "＿＿＿＿", 1)` 把目标词挖空，输出 `填空练习.txt`。
- **为什么**：这是这周精读 Python 官方教程"列表 / 字典 / 文件读写"三节时学到的——f-string 比 `%` 更直观（变量直接写在花括号里），`str.replace(旧, 新, 1)` 的第三个参数"只替换一次"正好适合做挖空，不会把同一句里的第二次出现也挖掉。

## 四、扩展功能（作业 2，两个都做了）

| 功能 | 函数 | 产物 |
|------|------|------|
| ① 按词性分组输出 | `group_by_pos()` / `report_groups()` | 终端打印：【动词】商量、感动、坚持 |
| ② 填空题（句子挖空） | `find_sentence_with()` / `gen_fill_blanks()` | `填空练习.txt`，共 9 道，全部来自《愚公移山》原句 |

## 五、最终运行结果

```
总词汇 13 个，其中 HSK4 词汇 4 个
词性分布：{'名词': 1, '动词': 3}
按词性分组：
  【名词】1 个：把字句
  【动词】3 个：商量、感动、坚持
已生成造句练习：练习.txt
已生成填空练习：填空练习.txt（共 9 道，来自《愚公移山》原句）
```

## 六、语法复习卡片（作业 3）

| 正面（要回忆的） | 背面（代码模板 / 一句话） |
|---|---|
| 列表推导式 | `[w for w in words if w["HSK等级"]=="4"]` —— 一行筛完一个列表 |
| 字典 get 计数 | `d[k] = d.get(k, 0) + 1` —— 没有就当 0，有就 +1 |
| with open 读文件 | `with open(p, encoding="utf-8") as f: list(csv.DictReader(f))` —— 自动关文件 |
| def 函数打包 | `def 名字(参数):` 缩进写动作，`return` 出结果；后面反复调用 |
