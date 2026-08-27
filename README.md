# Clink Chinese Enhanced v0.3（社区实验版）

Clink Chinese Enhanced language code: `zh_cn`

这是一个社区实验性中文增强包，用于验证 Clink 中文拼音输入的候选、长拼音短句和基础联想能力。仓库只发布 `zh_cn` 这一套语言包；旧的 `zh` 文件已移除，以避免与 Clink 官方中文包冲突。

这是针对 Clink 中文拼音现有“整串 reading → 候选”机制制作的实验增强包。目标不是假装实现真正的拼音解码器，而是在 **不修改 Clink App 本体** 的前提下，先补齐常用单字、常用词、长拼音短句和基础下一词预测。

## 这版具体做了什么

- `zh_cn.cime`：14,216 个拼音 reading，包含 GB2312 常用汉字、常用词和常见组合短句。
- `zh_cn.clex`：7,388 个词典条目，用于词典/补全基础能力。
- `zh_cn.cngm`：704 个下一词关系，从分词后的中文模板语料构建。
- `zh_cn.emoji.json`：基础中文 Emoji 关键词。
- **没有神经网络模型**：本版本先验证 IME 和联想链路，避免把问题混在一起。

## 必测用例

| 拼音 | 预期候选 |
|---|---|
| `nihao` | 你好 |
| `nihaoma` | 你好吗 |
| `pinyin` | 拼音 |
| `woxiangchifan` | 我想吃饭 |
| `jintianwoxiangchifan` | 今天我想吃饭 |
| `zhongwenshurufa` | 中文输入法 |
| `zidongjiucuo` | 自动纠错 |
| `zhongwenyuyanbao` | 中文语言包 |

如果 `nihaoma` / `pinyin` 在本包下仍然完全无法形成候选，那么问题基本可以判定在 **Clink App 的中文 IME composition/decoder**，不是语言包数据不足。

## 安装到 Clink 的方式

Clink 社区语言包通过 GitHub Release 仓库安装。

1. 在 GitHub 新建一个公开仓库，例如 `clink-chinese-enhanced`。
2. 把这个 ZIP 解压后的**全部内容**上传到仓库根目录。
3. GitHub → Actions → `Publish Clink Chinese Enhanced` → Run workflow，版本填 `v0.3.0`。
4. Workflow 成功后会创建 Release，并上传 `manifest.json` 与四个 `zh_cn--zh_cn.*` 语言包资产。
5. Clink → General → Repositories → 添加 `你的GitHub用户名/clink-chinese-enhanced`。
6. 回到 Languages / Community，安装该仓库提供的中文包。

> 这个包使用语言代码 `zh_cn`，以避开 Clink 官方 `zh` 中文包。测试前建议记下当前官方中文包设置，必要时可随时切回官方仓库。

## 已知硬限制

Clink 当前 `.cime` 本质仍是 reading→候选表。这个包用高频词和结构化短句扩大覆盖率，但它 **不能从语言包层面实现真正的动态拼音切分、Viterbi/beam search 整句解码、模糊音纠错**。这些需要 Clink App 本体支持。

因此本社区实验版的目的很明确：

1. 先让 `pinyin / nihaoma / woxiangchifan` 这类常用长拼音能工作；
2. 验证 `.cngm` 下一词模型是否被中文键盘实际调用；
3. 用测试结果判断下一步该继续扩词库，还是必须让开发者改 decoder。

## 文件说明

- `Lexicons/zh_cn.cime`：可读文本 IME 表。
- `Lexicons/zh_cn.clex`：Clink CLEX v1 二进制词典。
- `Lexicons/zh_cn.cngm`：Clink CNGM v1 下一词模型。
- `Lexicons/zh_cn.emoji.json`：中文 Emoji aliases。
- `source/zh_cn-ime.tsv`：可编辑 IME 源表。
- `source/zh_cn.txt`：词典源词表。
- `source/zh_cn.sentences.txt`：下一词模型的分词语料。
- `.github/workflows/release.yml`：自动发布 Release。

## 数据与许可

本实验包没有直接复制搜狗、百度等商业输入法词库，也没有打包 Rime 的第三方词库。常用词/短语与模板为本项目整理；拼音在构建阶段由系统 ICU transliterator 生成。详细见 `LICENSE.txt`。
