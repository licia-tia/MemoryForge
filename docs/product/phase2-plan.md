# MemoryForge 二期规划

## 1. 二期目标

一期先跑通：

```text
全量素材 -> 素材简介 -> ProjectBrief -> LLM TimelinePlan -> preview / timeline
```

二期再增强自动选片能力：

```text
照片锚点
embedding 检索
候选片段选择
更强去重
更小的 LLM 输入
```

二期不是重做一期，而是在 LLM 编排前增加更精准的候选片段层。

---

## 2. 主要能力

### 2.1 照片 Anchor

目标：

```text
用照片 / Live Photo 的时间和画面内容，反查长视频里的对应动态片段。
```

基本流程：

```text
照片拍摄时间 T
  -> 查找附近视频 segment
  -> 比较照片和视频 frame 的视觉相似度
  -> 找到最相近时间点
  -> 生成候选动态片段
```

输出：

```text
anchor_candidate_clips
```

### 2.2 Embedding Index

目标：

```text
为照片、视频 frame、视频 segment 建立视觉索引。
```

用途：

```text
相似画面检索
重复镜头聚类
照片匹配视频 frame
文本检索素材
封面候选筛选
```

### 2.3 Candidate Selector

目标：

```text
在 LLM 编排前，先用规则和 embedding 生成更小、更准的候选片段池。
```

候选来源：

```text
照片 anchor 附近片段
高质量大景
人物 / 地标 / 到达点
明显场景变化
少量时间均匀采样片段
用户手动保留片段
```

输出：

```text
candidate_clips.json
```

---

## 3. 二期 Pipeline

```text
Phase 1 Outputs
  -> Embedding Index
  -> Photo Anchor Match
  -> Candidate Selector
  -> ProjectBrief v2
  -> LLM TimelinePlan
  -> Validate / Export / Evaluate
```

一期的 `MediaSummary`、`SceneGroupSummary`、`TimelinePlan` 继续复用。

---

## 4. 路线

### v1.0 照片 Anchor

```text
根据照片时间和视觉相似度找到附近视频片段。
```

### v1.1 Embedding Index

```text
建立 frame / photo / segment embedding，支持检索和聚类。
```

### v1.2 Candidate Selector

```text
在 LLM 前生成候选片段池，降低输入规模，提升去重效果。
```

---

## 5. 成功标准

二期完成后应做到：

```text
1. 照片附近的动态视频片段能被自动找出
2. 重复镜头明显减少
3. LLM 输入规模下降
4. 生成的粗剪更少依赖 LLM 从海量摘要里硬挑
5. 仍然保持一期 preview / timeline / evaluate 闭环
```
