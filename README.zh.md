# F1 队友排位中位差

[English](./README.md) | [日本語](./README.ja.md) | 中文

这是一个单文件交互式网页应用,用于比较一个 F1 赛季中两位队友的**单圈/排位速度**。核心指标是**排位差距中位数**:相比平均值,它更不容易被撞车、黄旗、机械故障、湿地等极端样本带偏。

🔗 **在线演示:** https://hsu9ar.github.io/f1-teammate-quali-gap/f1-teammate-quali-gap.html

如果链接显示 404,请先在 GitHub 仓库中开启 GitHub Pages:
**Settings → Pages → Deploy from a branch → `main` → `/ (root)` → Save**。

## 为什么用中位数,不是平均数?

排位差距里经常有被污染的样本:撞车、黄旗导致飞驰圈被毁、Q1 只跑了一圈、机械问题等。这些样本会产生很大的极端值,让**平均值**偏离真实水平。**中位数**对离群值更稳健,因此更适合表达两位车手在正常情况下的典型单圈差距。

## 指标怎么计算

对赛季中的每一站:

1. 取两位车手都进入过的**最高共同排位阶段**中的最快圈(Q3 > Q2 > Q1),保证比较是同条件的。
2. 用**百分比差距**而不是绝对秒数,避免不同赛道长度带来的影响:
   `gap% = (t_A − t_B) / t_B × 100`
3. 对整个赛季每站的百分比差距取**中位数**。

注意:数据源不会自动标注干地/湿地。湿地、撞车、明显不代表真实速度的站点,可以在图表或表格里手动点击排除。这个指标只衡量排位/单圈速度,不代表正赛长距离速度。

## 功能

- 选择**赛季 → 车队 → 两位车手**,所有结果即时重算。
- 展示**中位数 / 平均值 / 队内对决比分 / 有效样本数**。
- 每站柱状图使用稳健纵轴,会**裁剪极端离群值**并在柱子边缘标出真实值,避免普通差距被压扁看不清。也可以关闭聚焦视图查看完整范围。
- **点击任意柱子或表格行即可排除该站**,中位数实时更新。
- 界面支持 **English / 日本語 / 中文**,语言切换在右上角。
- **本地数据优先**:即使实时 API 无法访问,也可以通过本地 JSON 离线运行。

## 数据源

免费 [Jolpica-F1 API](https://github.com/jolpica/jolpica-f1),它是已停止的 Ergast API 的后继项目。不需要 API key。

## 如何运行

这是一个静态单文件网页,直接用浏览器打开 `f1-teammate-quali-gap.html` 即可。

页面会优先读取本地数据(`data/quali-<year>.json`),如果没有本地数据,再尝试访问实时 API。如果实时 API 因网络、CORS 或地区限制无法访问,可以先生成本地数据:

```bash
python build_data.py 2024
python build_data.py 2021 2022 2023 2024
```

脚本会生成 `data/quali-<year>.json`。刷新页面后即可离线运行。

### 可选:用 FastF1 扩展数据

`build_data.py` 里包含 `build_with_fastf1()` 示例。[FastF1](https://docs.fastf1.dev/) 是 Python 库,不是浏览器 API,但可以获取遥测、轮胎、练习赛等更丰富的数据。安装方式:

```bash
pip install fastf1
```

如果以后想把项目扩展到遥测分析,可以在 `main()` 中切换到 FastF1 取数逻辑。

## 部署到 GitHub Pages

1. 创建 GitHub 仓库并 push 这些文件。
2. 在 GitHub 仓库中进入 **Settings → Pages → Build and deployment → Source: Deploy from a branch**,分支选择 `main`,目录选择 `/ (root)`,然后保存。
3. 大约一分钟后,页面会发布到 `https://hsu9ar.github.io/f1-teammate-quali-gap/f1-teammate-quali-gap.html`。

## 项目结构

```text
f1-teammate-quali-gap.html   # 应用本体(HTML + CSS + JS,单文件)
build_data.py                # Jolpica -> data/quali-<year>.json(FastF1 可选)
data/                        # 生成的 JSON(可选,用于离线运行)
README.md                    # English documentation
README.ja.md                 # 日本語ドキュメント
README.zh.md                 # 中文文档
```

## License

MIT
