# Clink Chinese Enhanced v0.4

语言代码：`zh_cn`（避开官方 `zh` 包冲突）

这是给 [Clink](https://clinkkeys.app/) 用的社区中文拼音包。  
词频、读音和候选排序来自 [万象拼音](https://github.com/amzxyz/rime-wanxiang)（CC BY 4.0），再按 Clink 的能力裁剪。

> 万象好用，是因为 Rime 会动态切分音节、整句解码，再叠加语法模型。  
> Clink 的 `.cime` **不会**做这些事：它只做「整串拼音 → 最多 16 个候选」。  
> 所以这个包能做的，是把万象里真正高频的字词，按权重排进这张静态表，而不是假装自己是 Rime。

## 和 v0.3 / 官方 `zh` 的差别

| | v0.3 实验包 | 官方 `zh` | 本包 v0.4 |
|---|---|---|---|
| 数据来源 | GB2312 + 模板长句笛卡尔积 | Clink 自带表 | 万象字表 + 高频基础词 |
| IME 条数 | 14,216，其中 1.2 万是「晚上我们能坐火车」这种整句 | 约 2.8 万 | 约 6.7 万（字、词、地名、人名、少量简拼） |
| 候选排序 | 基本按字表顺序，`wo` 第二候选是「倭」 | 一般，但覆盖偏旧 | 按万象词频，`wo`/`ni`/`shi`/`de` 常用字在前 |
| 日常词 | 缺「什么」「怎么」 | 有，但现代网络词偏少 | 有微信、支付宝、外卖、验证码等 |
| 长句 | 靠穷举模板 | 几乎没有 | 只保留真的会整串输入的短句 |
| 联想 | 115 个词拼出来的 2 万模板句 | 有下一词模型 | 3,090 条更自然的下一词对 |
| Emoji | 24 个 | 约 1900 | 沿用官方中文 Emoji 表并合并本包补充 |

v0.3 不好用的根因不是「词太少」，而是：

1. **12,228 条 reading 长度 ≥ 16**，全是模板句。日常输入是 `jin` → `jintian` → 再打下一个词，不会把「等会儿我们想要看电影」一次打完。
2. **词典 7388 条里 6763 条是生僵单字**，2 字词只有 350 个。
3. Clink 不会切分拼音。词库再堆长句，只要你少打一个字母就匹配不上。

## 这个包实际覆盖什么

- 万象单字表：按音节取词频最高的 16 个字
- 万象基础词库：权重 ≥ 1500 的 2–4 字词
- 多音、错音、地名、人名、艺人（按权重截断）
- 高频词简拼：`nh` 你好、`zg`/`zhg` 中国、`bj` 北京、`wx` 微信
- `v` = `ü`：`nv` 女、`lv` 绿
- 常用口语短句：你好吗、对不起、我想吃饭、中文输入法

## 必测

| 拼音 | 预期首选 |
|---|---|
| `nihao` | 你好 |
| `nihaoma` | 你好吗 |
| `shenme` | 什么 |
| `zenme` | 怎么 |
| `zenmeyang` | 怎么样 |
| `wo` | 我 |
| `shi` | 是 |
| `de` | 的 |
| `yi` | 一 |
| `nv` | 女 |
| `lv` | 绿 |
| `zhongguo` | 中国 |
| `zg` / `zhg` | 中国 |
| `bj` | 北京 |
| `wx` | 微信 |
| `woxiangchifan` | 我想吃饭 |
| `pinyin` | 拼音 |
| `zhongwenshurufa` | 中文输入法 |

打词请按词来：`jintian` 出「今天」，再打 `tianqi` 出「天气」。不要指望整串解码——Clink 现在没有这个解码器。

## 安装

1. Clink → **General → Repositories**，添加：

   ```text
   dayifulalala-del/clink-chinese-enhanced
   ```

2. GitHub Actions 运行 `Publish Clink Chinese Enhanced`，版本填 `v0.4.0`。
3. Languages → Community，安装 `zh_cn`。
4. 不要覆盖官方 `zh`。

发布后 Clink 读的是 GitHub Release 里的 `manifest.json` 和 `zh_cn--zh_cn.*`。

## 许可

- 本仓库整理脚本、短句和发布配置：CC0-1.0
- 字词读音与词频：来自 [amzxyz/rime-wanxiang](https://github.com/amzxyz/rime-wanxiang)，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 构建脚本格式兼容 [anti-ltd/clink-language-packs](https://github.com/anti-ltd/clink-language-packs)
