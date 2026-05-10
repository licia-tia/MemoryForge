# MemoryForge 总体架构 v0.1

## 1. 项目定位

MemoryForge 是一个可配置模型 Provider 的 AI 媒体理解与粗剪系统。

第一阶段不追求复杂自动选片算法。先完成一个更直接的闭环：

```text
扫描全部素材
  -> 为照片和视频片段生成简介
  -> 合并成分层项目素材包
  -> 交给高能力 LLM 组织粗剪时间线
  -> 校验并修复时间线
  -> 导出预览和可编辑时间线
  -> 生成自评报告
```

换句话说，一期重点是把一大坨杂乱素材变成 LLM 能理解、能组织、能落地导出的结构化上下文。

典型输入：

```text
3-4 小时 行人记录仪长视频
+ 30-80 张照片 / Live Photo / Motion Photo
+ 若干短视频
```

一期目标输出：

```text
素材总览报告
每个素材 / 片段的简介
分层 ProjectBrief
60s / 3min 粗剪时间线
预览视频
DaVinci Resolve 免费版可继续精修的时间线
时间线自评报告
```

---

## 2. 核心判断

### 2.1 一期先做全量素材简介

一期的关键问题是让系统先知道“这批素材里大概有什么”。

对照片：

```text
识别画面内容
评估摄影质量和作品价值
判断是否适合作为封面 / 开场 / 结尾 / 插图 / 独立照片段落
记录拍摄时间、相机、位置等元数据
生成一句人能读、LLM 能用的简介
```

对视频：

```text
按时间切成粗 segment
抽取关键帧
识别画面内容
识别轻量音频特征
估计画质、稳定性、音频可用性和粗略用途
```

### 2.2 高能力 LLM 做一期编排核心

一期不急着堆复杂规则。先把素材简介、时间顺序、评分和约束整理成一个项目上下文，让高能力 LLM 做故事线组织。

LLM 输入不是原始 4 小时视频，而是结构化摘要：

```text
项目概况
素材列表
场景分组
视频 segment 简介
照片简介
画面和音频质量分
目标片长
用户偏好
```

LLM 输出必须是可执行的 TimelinePlan：

```text
每个条目的 source_asset_id
每个视频条目的 source in/out
每个照片条目的展示时长和 motion 策略
每个条目在成片中的 record in/duration
选择理由
被舍弃素材的简要原因
```

### 2.3 照片作为独立素材参与编排

一期照片的作用：

```text
作为独立素材被理解
作为故事节点的提示信息
作为封面 / 插图 / 开场 / 结尾候选
好照片可以作为摄影作品独立进入时间线
可以在一段动态视频后展示 n 秒，形成“动态过程 -> 定格作品”的节奏
作为 photo timeline item 进入粗剪
和视频 segment 一起交给 LLM 编排
```

### 2.4 模型 Provider 可配置

MemoryForge 不预设必须本地或云端。每个 AI 环节都应该能单独配置模型 provider。

可配置的环节：

```text
video_frame_labeler     视频关键帧识别
photo_labeler           照片识别和摄影质量评估
audio_analyzer          音频分析
scene_group_summarizer  场景分组摘要
planning_llm            时间线规划
repair_llm              无效 TimelinePlan 修复
evaluation_llm          时间线自评
```

用户自己选择每个环节使用本地模型、云端模型或手工规则，并平衡：

```text
隐私
成本
速度
效果
稳定性
```

系统职责是把 provider 边界、输入输出 schema、缓存 key 和审计记录定义清楚。

### 2.5 所有中间产物必须可恢复

3-4 小时素材分析可能跑很久，任何一步都不能只存在内存里。

原则：

```text
所有中间产物落盘
每一步输入输出可复查
任务失败后可从最近成功节点继续
同一素材同一参数不重复分析
更换模型 / prompt / segment 参数时能明确哪些结果需要重算
```

### 2.6 稳定数据契约比模型选择更重要

MemoryForge 不绑定某个照片平台或模型。

需要稳定的是这几类内部对象：

```text
Asset
Segment
MediaSummary
SceneGroupSummary
ProjectBrief
TimelinePlan
PlanValidationResult
TimelineEvaluation
AnalysisCache
```

---

## 3. 一期总体架构

```text
MemoryForge Phase 1

1. Ingest
   扫描本地目录，建立素材清单。

2. Preprocess
   读取元数据，统一时间，识别媒体类型和 still/motion pair。

3. Segment
   将视频切成粗 segment，抽关键帧，提取轻量音频特征。

4. Summarize
   对照片和视频 segment 生成简介、标签、质量分和用途建议。

5. Group / Compress
   将连续相似 segment 合并为 scene group，压缩 LLM 上下文。

6. Brief
   汇总照片简介和 scene group，生成 ProjectBrief。

7. Plan
   把 ProjectBrief 交给高能力 LLM，生成 TimelinePlan。

8. Validate / Repair
   校验 TimelinePlan 的引用、时间范围、总时长和 preset 约束，必要时触发 repair。

9. Export
   根据通过校验的 TimelinePlan 导出预览视频和可编辑时间线。

10. Evaluate
   对粗剪结果生成自评报告，帮助判断是否需要重新规划。
```

数据流：

```text
Media Files
   |
   v
Asset Catalog
   |
   v
Segments + Keyframes + Audio Features
   |
   v
Media Summaries
   |
   v
Scene Group Summaries
   |
   v
ProjectBrief
   |
   v
High Capability LLM
   |
   v
TimelinePlan
   |
   v
PlanValidator + Repair Loop
   |
   v
Preview / OTIO / FCPXML / Reports
   |
   v
TimelineEvaluation
```

---

## 4. 模块边界

### 4.1 Ingest

职责：

```text
扫描本地媒体目录
识别照片、视频、Live Photo / Motion Photo
生成 asset_id
记录源路径和基础元数据
保证不修改原始素材
```

一期只完整支持本地目录。其他来源先不做，最多保留 adapter 边界。

### 4.2 Preprocess

职责：

```text
读取 EXIF / QuickTime / ffprobe 元数据
统一拍摄时间
生成视频基础信息
识别 still/motion pair
准备缩略图和代理路径
```

时间字段先保持简单但要分清两类：

```text
captured_at_utc    素材拍摄时间，用于排序
source_pts_sec     视频内部时间，用于剪辑 in/out
```

Live Photo / Motion Photo 边界：

```text
一期只负责把 still 和 motion 归为同一个 pair_id
```

pair 识别优先级：

```text
Apple Live Photo:
  1. metadata content identifier 匹配
  2. 文件名接近
  3. creation time 接近

Google Motion Photo:
  1. 单文件内嵌 video payload
  2. 导出目录中的 photo/video pair
  3. sidecar metadata 匹配
```

### 4.3 Segment

职责：

```text
按固定时长切视频 segment
抽取关键帧
提取轻量音频特征
记录 segment 和 keyframe 路径
```

默认策略：

```text
每 10-20 秒切一个粗 segment
每段抽 3-5 张关键帧
提取音量、静音比例、简单风噪/人声/环境声标签
```

一期不需要做复杂语音转写；如果检测到明显人声，可以后续接 ASR。

### 4.4 Summarize

一期核心模块。

职责：

```text
为每张照片生成简介
为每个视频 segment 生成简介
输出视觉标签、音频标签、摄影质量分、音频质量分、用途建议
生成 LLM 可消费的结构化摘要
```

照片默认处理方式：

```text
读取元数据
生成缩略图
调用视觉模型生成一句简介
评估 sharpness / exposure / composition / color / subject / moment
判断是否是一张好照片或摄影作品
判断是否适合封面 / 开场 / 结尾 / 插图 / 独立照片段落
```

视频 segment 默认处理方式：

```text
读取关键帧和音频特征
用视觉模型或多模态 LLM 生成段落简介
保留画面可用性和音频可用性
```

### 4.5 Group / Compress

职责：

```text
将连续相似 segment 合并为 scene group
为每个 scene group 生成摘要
标记 best_segments 和 repetitive_segments
压缩 ProjectBrief 上下文长度
```

4 小时视频按 20 秒切会产生约 720 个 segment，不能全部原样塞给 LLM。Planning LLM 应优先阅读 scene group，再按需引用具体 segment。

### 4.6 Brief

职责：

```text
把照片简介和 scene group 组织成项目级上下文
控制上下文长度
按时间、素材类型和质量分组
生成给 Planning LLM 的输入包
```

ProjectBrief 应该是一个确定性的中间产物，方便复查和重复规划。

### 4.7 Plan

职责：

```text
调用高能力 LLM
根据 ProjectBrief 组织粗剪时间线
控制目标时长
保留时间顺序和故事节奏
给出每个片段的选择理由
```

一期可以让 LLM 承担更多判断，但 LLM 输出不能直接执行，必须先进入 PlanValidator。

### 4.8 Validate / Repair

职责：

```text
校验 TimelinePlan JSON schema
校验 source_asset_id 是否存在
校验 source_in/out 是否在素材 duration 范围内
校验 record timeline 是否重叠
校验总时长误差是否在阈值内
校验 preset 约束
失败时生成 repair prompt 并重试
```

PlanValidator 是防止 LLM 输出“看起来合理但不可执行”的关键模块。

### 4.9 Export

职责：

```text
读取通过校验的 TimelinePlan
生成 preview.mp4
导出 OTIO
导出 DaVinci Resolve 免费版可导入的 FCPXML
必要时导出 EDL
输出 selection_report.md
```

一期导出顺序应收敛：

```text
先保证 preview.mp4
再保证 OTIO
最后做 FCPXML for DaVinci Resolve Free
```

FCPXML 兼容性不应该阻塞第一条 preview 闭环。

### 4.10 Evaluate

职责：

```text
检查目标时长是否达标
检查是否过度重复
检查是否覆盖关键时间段
检查照片是否被使用
检查低质量片段占比
检查是否存在长时间黑屏 / 静止 / 抖动 / 废音频
```

Evaluate 不替代人工审片，但可以帮助快速判断 LLM plan 是否需要重跑。

---

## 5. 核心数据对象

这里只定义逻辑对象，不展开完整数据库 schema。

### 5.1 Asset

表示一个原始媒体资产。

```json
{
  "asset_id": "asset_xxx",
  "media_type": "photo | video | live_photo_still | live_photo_motion",
  "source_path": "...",
  "pair_id": "...",
  "captured_at_utc": "2026-05-10T02:30:00Z",
  "duration_sec": 0.0,
  "camera": "GoPro / iPhone / Pixel",
  "favorite": false,
  "content_hash": "..."
}
```

### 5.2 Segment

表示视频中的一段粗粒度分析区间。

```json
{
  "segment_id": "seg_xxx",
  "asset_id": "asset_video_xxx",
  "source_in_sec": 120.0,
  "source_out_sec": 140.0,
  "captured_start_utc": "2026-05-10T02:32:00Z",
  "keyframes": ["frame_001.jpg", "frame_002.jpg"],
  "audio_features": {
    "silent_ratio": 0.05,
    "peak_db": -6.0,
    "speech_detected": false
  }
}
```

### 5.3 MediaSummary

表示照片或视频 segment 的简介。

```json
{
  "summary_id": "summary_xxx",
  "target_type": "photo | segment",
  "target_id": "seg_xxx",
  "time_range": "上午 10:20 左右",
  "description": "山路上行走，画面有树林和远处山脊，轻微抖动。",
  "tags": ["trail", "forest", "walking"],
  "quality_score": 0.68,
  "photo_quality": {
    "is_photo_work": false,
    "photo_score": 0.0,
    "sharpness": 0.0,
    "exposure": 0.0,
    "composition": 0.0,
    "color": 0.0,
    "subject_interest": 0.0,
    "moment_value": 0.0
  },
  "suggested_use": ["process", "b_roll"],
  "avoid_reason": ["slightly_shaky"],
  "audio_summary": "有风噪，几乎无可用人声。",
  "speech_detected": false,
  "audio_quality_score": 0.35,
  "sound_tags": ["wind", "footsteps"],
  "usable_audio": false
}
```

照片没有音频时，音频字段可以为空或标记为 not_applicable。

对照片，`quality_score` 表示综合可用性，`photo_quality.photo_score` 表示作为摄影作品单独进入时间线的价值。

### 5.4 SceneGroupSummary

表示连续多个 segment 合并后的场景摘要。

```json
{
  "scene_group_id": "scene_012",
  "asset_id": "asset_video_001",
  "source_in_sec": 1200.0,
  "source_out_sec": 1580.0,
  "summary": "沿山脊徒步，天气晴朗，视野逐渐开阔。",
  "visual_tags": ["ridge", "wide_view", "walking"],
  "sound_tags": ["wind", "footsteps"],
  "best_segments": ["seg_061", "seg_064", "seg_072"],
  "repetitive_segments": ["seg_062", "seg_063"],
  "quality_score": 0.78
}
```

### 5.5 ProjectBrief

表示交给高能力 LLM 的项目级上下文。

```json
{
  "project_id": "hike_2026",
  "target_presets": ["60s", "3min"],
  "project_summary": "一次徒步旅行，包含长视频、照片和少量 Live Photo。",
  "assets_count": {
    "photos": 64,
    "videos": 3,
    "segments": 720,
    "scene_groups": 85
  },
  "photo_summaries": [],
  "scene_groups": [],
  "constraints": {
    "prefer_chronological": true,
    "avoid_repetition": true,
    "keep_original_files_readonly": true
  }
}
```

### 5.6 TimelinePlan

表示 LLM 输出的粗剪时间线。

视频条目：

```json
{
  "preset": "60s",
  "timeline": [
    {
      "item_id": "item_001",
      "source_type": "video",
      "record_in_sec": 0.0,
      "duration_sec": 4.0,
      "source_asset_id": "asset_video_xxx",
      "source_in_sec": 120.0,
      "source_out_sec": 124.0,
      "role": "opening",
      "reason": "开场画面开阔，适合快速建立旅行场景。"
    }
  ],
  "rejected_notes": [],
  "editing_notes": "整体按时间顺序推进，减少重复山路。"
}
```

照片条目：

```json
{
  "item_id": "item_014",
  "source_type": "photo",
  "record_in_sec": 46.0,
  "duration_sec": 3.0,
  "source_asset_id": "asset_photo_xxx",
  "role": "photo_work",
  "motion": "slow_zoom_in",
  "placement": {
    "after_item_id": "item_013",
    "intent": "dynamic_to_still"
  },
  "reason": "照片构图好，适合接在到达山顶的视频后作为定格作品展示。"
}
```

一期支持的照片使用方式：

```text
静帧插入
默认展示 2-4 秒
可选 slow_zoom_in / slow_pan
接在相关动态视频之后展示 n 秒
封面候选
结尾候选
```

### 5.7 AnalysisCache

表示可复用的中间产物缓存键。

```json
{
  "cache_key": "cache_xxx",
  "target_type": "asset | segment | summary | scene_group",
  "target_id": "seg_xxx",
  "content_hash": "...",
  "media_mtime": 1778397600,
  "segment_params": {
    "segment_length_sec": 20,
    "keyframes_per_segment": 5
  },
  "provider": "openai",
  "model_name": "vision-model",
  "model_version": "2026-05-10",
  "prompt_version": "summary_v1",
  "summary_version": "media_summary_v1",
  "artifact_path": "analysis/summaries/seg_xxx.json"
}
```

### 5.8 PlanValidationResult

表示 TimelinePlan 校验结果。

```json
{
  "valid": false,
  "errors": [
    {
      "code": "source_range_out_of_bounds",
      "item_id": "item_003",
      "message": "source_out_sec exceeds asset duration"
    }
  ],
  "repairable": true,
  "repair_prompt_path": "analysis/repair_prompts/plan_60s_attempt_1.md"
}
```

### 5.9 TimelineEvaluation

表示粗剪自评结果。

```json
{
  "preset": "60s",
  "target_duration_sec": 60,
  "actual_duration_sec": 61.5,
  "duration_ok": true,
  "photo_usage_count": 4,
  "low_quality_ratio": 0.08,
  "repetition_warning": false,
  "coverage_notes": ["覆盖出发、山脊和到达点，回程素材较少。"],
  "audio_warnings": ["item_006 有明显风噪，建议静音或替换。"]
}
```

### 5.10 ModelProviderConfig

表示每个 AI 环节使用的 provider。

```json
{
  "video_frame_labeler": {
    "provider": "openai | gemini | local_ollama | lmstudio | custom",
    "model": "model-name",
    "send_images": true
  },
  "photo_labeler": {
    "provider": "openai | gemini | local_ollama | lmstudio | custom",
    "model": "model-name",
    "send_images": true
  },
  "audio_analyzer": {
    "provider": "local_ffmpeg | whisper | custom",
    "model": "model-name"
  },
  "scene_group_summarizer": {
    "provider": "openai | local_ollama | custom",
    "model": "model-name"
  },
  "planning_llm": {
    "provider": "openai | claude | gemini | local_ollama | custom",
    "model": "model-name",
    "input_mode": "metadata_only | thumbnail_light"
  },
  "repair_llm": {
    "provider": "same_as_planning | openai | local_ollama | custom",
    "model": "model-name"
  }
}
```

具体 provider 名称和模型名不写死在架构里，由项目配置决定。

---

## 6. 一期 LLM 编排方式

一期把 Planning LLM 放在核心位置，但必须用分层摘要控制上下文。

输入层级：

```text
SegmentSummary
  -> SceneGroupSummary
  -> ProjectBrief
  -> TimelinePlan
```

Planning LLM 优先阅读 `SceneGroupSummary` 和高分照片摘要，只在需要精确落点时引用 `best_segments`。

输入应该尽量结构化，而不是直接塞一篇自然语言长文：

```text
项目目标
目标片长
素材统计
按时间排序的照片简介
按时间排序的 scene group
每个 scene group 的 best_segments
画面质量、音频质量和用途建议
硬约束
```

LLM 需要完成：

```text
选择视频片段和照片
将高分照片作为独立 photo item 插入时间线
可以在动态视频片段后放一张摄影作品持续 n 秒
决定片段顺序
控制总时长
减少重复
兼顾时间顺序和故事节奏
解释为什么选这些片段
```

为了防止输出不可执行，TimelinePlan 必须引用已有 asset_id 和 source_in/source_out。

可以先支持两种规划模式：

```text
metadata_only    只发送文字简介和分数
thumbnail_light  允许发送缩略图或关键帧
```

默认优先 `metadata_only`。

### 6.1 Plan 校验和修复

LLM 输出后必须经过强校验：

```text
JSON Schema / Pydantic schema 校验
source_asset_id 必须存在
source_in/out 必须在素材 duration 范围内
photo item 不应带 source_in/out
record timeline 不能重叠
总时长误差不能超过阈值
必须满足 preset 约束
```

校验失败时进入 repair loop：

```text
TimelinePlan
  -> PlanValidator
  -> ValidationResult(errors)
  -> repair prompt
  -> LLM 修复
  -> 再次校验
```

repair 重试次数应有限制。超过限制后保留失败产物和错误报告，方便人工排查。

---

## 7. CLI 设计

一期 CLI-first。

建议命令：

```bash
memoryforge init ./project
memoryforge ingest ./media --project ./project
memoryforge segment --project ./project
memoryforge summarize --project ./project
memoryforge brief --project ./project --preset 60s --preset 3min
memoryforge plan --project ./project --planner gpt-5.5
memoryforge validate --project ./project --preset 60s
memoryforge export --project ./project --preset 60s
memoryforge evaluate --project ./project --preset 60s
```

每个命令都应该：

```text
读取上一步落盘产物
写入本步骤产物
支持跳过已有且缓存有效的结果
输出清晰的失败原因
```

---

## 8. 一期输出

```text
output/
  reports/
    project_brief.md
    project_brief.json
    selection_report.md
    timeline_eval.md
    timeline_eval.json

  preview/
    60s_highlight.mp4
    3min_travel.mp4

  timelines/
    60s_highlight.otio
    3min_travel.otio
    60s_highlight.fcpxml
    3min_travel.fcpxml
    60s_highlight.edl
    3min_travel.edl

  analysis/
    memoryforge.db
    summaries.json
    scene_groups.json
    timeline_plan.json
    validation_result.json
```

一期可以不导出大量 selected_clips 文件。先保证 preview 和 timeline 正确。

DaVinci Resolve 免费版兼容策略：

```text
第一目标：preview.mp4 可播放
内部格式：OTIO
主交换格式：FCPXML
保底格式：EDL
时间线内容：剪切点、素材路径、source in/out、轨道顺序
一期避免：复杂转场、插件效果、调色、字幕样式、Fusion 合成
```

---

## 9. 路线图

### Phase 1 MVP

#### v0.1 本地素材扫描

目标：

```text
扫描本地视频和照片
建立 Asset 记录
读取基础时间和相机元数据
识别 Live Photo / Motion Photo pair
```

验收：

```text
给定一个本地目录，可以生成 memoryforge.db
assets 中有视频、照片和 pair 关系
不会修改原始素材
```

#### v0.2 Segment 和素材简介生成

目标：

```text
切分视频 segment
抽取关键帧和轻量音频特征
为照片生成简介
为视频粗 segment 生成简介
生成 summaries.json
```

验收：

```text
每张照片有 description / tags / suggested_use
每个视频 segment 有 description / quality_score / audio_quality_score / suggested_use
可以生成人能读的素材总览报告
失败后可断点续跑
```

#### v0.3 Group / Brief / Plan / Validate

目标：

```text
生成 SceneGroupSummary
把全部素材简介组织成 ProjectBrief
调用高能力 LLM 生成 TimelinePlan
校验并修复 TimelinePlan
```

验收：

```text
ProjectBrief 不直接塞满全部 segment 原文
TimelinePlan 引用真实 asset_id 和 source in/out
输出 60s / 3min 两套计划
每个片段有选择理由
无效 plan 会进入 repair loop
```

#### v0.4 Preview Export 和 Evaluate

目标：

```text
根据 TimelinePlan 生成 preview.mp4
输出 selection_report.md
输出 timeline_eval.md
```

验收：

```text
60s 和 3min preview 可播放
片段顺序和 TimelinePlan 一致
自评报告能指出时长、重复、覆盖和音频风险
不修改原始素材
```

#### v0.5 可编辑时间线导出

目标：

```text
生成 OTIO
导出 DaVinci Resolve 免费版可导入的 FCPXML
必要时导出 EDL 作为保底
```

验收：

```text
DaVinci Resolve 免费版可以导入时间线
素材引用、in/out 和片段顺序正确
FCPXML 问题不阻塞 preview 闭环
```

---

## 10. 暂不做

一期不做：

```text
复杂 GUI
账号系统
云端同步
自动配乐卡点
自动字幕样式
多平台双向同步
一键最终大片
```

一期只追求一个闭环：

```text
全量素材
  -> 素材简介
  -> SceneGroupSummary
  -> ProjectBrief
  -> LLM TimelinePlan
  -> Validate / Repair
  -> preview / timeline
  -> Evaluate
```

---

## 11. 一期成功标准

给定一次徒步素材：

```text
3-4 小时视频
+ 30-80 张照片 / Live Photo / Motion Photo
```

MemoryForge 一期应做到：

```text
1. 扫描全部素材并建立素材目录
2. 给照片和视频片段生成可读简介
3. 记录基础音频可用性，避免 LLM 盲选废音频片段
4. 生成分层项目素材总览
5. 把素材总览交给高能力 LLM 组织 60s / 3min 时间线
6. 校验并修复不可执行的 TimelinePlan
7. 根据时间线导出可播放 preview
8. 输出 OTIO，并在 v0.5 提供 DaVinci Resolve 免费版可导入的 FCPXML
9. 生成时间线自评报告
10. 全程不修改原始素材，并支持断点续跑
```

最终一句话：

```text
MemoryForge 一期先把全部素材变成带画面和音频信息的分层简介包，
再让高能力 LLM 基于这个简介包组织粗剪时间线，
并通过校验、导出和自评形成可恢复的粗剪闭环。
```
