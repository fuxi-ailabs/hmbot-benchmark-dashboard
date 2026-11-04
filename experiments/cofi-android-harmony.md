# 阶段1-所有model harness组合的A2H实验

实验规划 · 2026-10-30 · 11 组。历史迁移自报完成 6 组，其余 5 组状态见下表。

**自报完成不代表独立验收通过。** 已确认复用6组历史结果，补跑5组；当前执行状态以各行记录为准。

阶段1迁移实验已收尾：11组迁移自报完成（6组历史复用+5组本批补跑）。本批五组均完成静默复核、归档SHA校验和专属资源清理，保留结果磁盘；未自动独立验收。Qwen/DevEco首条prompt重复两遍，不能视作严格同prompt对照；MiniMax及两组DeepSeek的首尾空白差异继续保留。镜像栏记录本地克隆名称，尚无已核实的远程下载地址。

| 模型 / ID | Harness | 迁移状态 | 独立验收 | 结果镜像（本地 Tart） | 进度备注 |
|---|---|---|---|---|---|
| MiniMax / MiniMax-M3 | DevEco Code 0.2.3 | 迁移自报完成 | 待独立验收 | `s1-cofi-minimax-deveco-20261030` · 远程地址待补 | 13:17 后确认全部会话日志静默，归档693个文件并校验SHA；专属手机、relay与Tart已关闭，保留磁盘。agent自报14/14自检通过，未独立验收。自报限制包括PiP未实现、仅中英两语、未移植Wear OS及波浪环近似。首条prompt仅首尾空白差异。 日间优先 |
| MiniMax / MiniMax-M3[1m] | Claude Code 2.1.267 | 迁移自报完成 | 历史测试已执行；定位/观测受阻，未判定验收通过 | `cofi-harmony-minimax-20261026` · 远程地址待补 | 已确认复用历史结果。 历史结果已复用 |
| Qwen / qwen3.8-max | DevEco Code 0.2.3 | 迁移自报完成 | 待独立验收；存在 prompt 偏差 | `s1-cofi-qwen-deveco-20261030` · 远程地址待补 | 14:17 北京时间完成15分钟全会话静默复核，归档664文件及原生日志并校验SHA；手机/relay/VM已停止，磁盘保留。自报16种语言、11张设备截图、27文件arkts_check零错误；PiP/WearOS/动态快捷方式未迁移，Material You固定色板，冻结期回前台追补。首条消息误含两遍相同原始prompt；本轮不属于严格同prompt对照，不自动纠正或重跑。 日间优先 |
| Qwen / qwen3.8-max | Claude Code 2.1.267 | 迁移自报完成 | 历史测试已执行；定位/观测受阻，未判定验收通过 | `cofi-harmony-qwen-20261026` · 远程地址待补 | 已确认复用历史结果。 历史结果已复用 |
| GLM / glm-5.3 | DevEco Code 0.2.3 | 迁移自报完成 | 待独立验收 | `cofi-deveco-pro-20261029` · 远程地址待补 | 目录中的 pro 为旧名称，实际模型为 GLM。 历史结果已复用 |
| GLM / glm-5.3[1m] | Claude Code 2.1.267 | 迁移自报完成 | 历史测试已执行；定位/观测受阻，未判定验收通过 | `cofi-harmony-glm-20261026` · 远程地址待补 | 已确认复用历史结果。 历史结果已复用 |
| DeepSeek Pro / deepseek-v4-pro | DevEco Code 0.2.3 | 迁移自报完成 | 待独立验收 | `s1-cofi-deepseek-pro-deveco-20261030` · 远程地址待补 | 21:15北京时间完成15分钟全会话静默复核，归档489文件及原生日志并校验SHA；专属手机/relay/VM均已停止，保留磁盘。自报11/11任务、13ets检查、构建安装首屏验证；英文单语，后台/PiP/通知/实际声音未实现，备份限沙盒、emoji代替矢量图标，交互未逐点击验证。首条任务仅末尾LF变空格，正文一致；未独立验收。 北京时间 20:00–08:00 启动 |
| DeepSeek Pro / deepseek-v4-pro | Claude Code 2.1.267 | 迁移自报完成 | 待独立验收 | `cofi-harmony-deepseek-pro-retest-20261028` · 远程地址待补 | 采用 10/28 重测；10/26 旧版测试结果不混入。 历史结果已复用 |
| DeepSeek Flash / deepseek-flash | DevEco Code 0.2.3 | 迁移自报完成 | 待独立验收 | `s1-cofi-deepseek-flash-deveco-20261030` · 远程地址待补 | 21:15北京时间完成15分钟全会话静默复核，归档669文件及原生日志并校验SHA；专属手机/relay/VM均已停止，保留磁盘。自报构建安装及临时路由逐页截图，调试路由已移除；PiP/后台长时能力未接入，verify_ui因未配置多模态不可用。首条任务仅末尾LF变空格，正文一致；未独立验收。 北京时间 20:00–08:00 启动 |
| DeepSeek Flash / deepseek-flash | Claude Code 2.1.267 | 迁移自报完成 | 历史测试已执行；定位/观测受阻，未判定验收通过 | `cofi-harmony-deepseek-20261026` · 远程地址待补 | 已确认复用历史结果。 历史结果已复用 |
| GPT / gpt-6-astra | Codex CLI 0.162.1 | 迁移自报完成 | 待独立验收 | `s1-cofi-gpt-codex-20261030` · 远程地址待补 | 14:02 北京时间完成15分钟全线程静默复核；已归档1204文件、2内部相对链接及原生日志并校验SHA；专属手机/relay/代理/VM已停止，保留磁盘。ArkTS + 离线ArkWeb；agent自报12核心测试、12组浏览器流程、19项设备内断言。WearOS、系统PiP、壁纸取色未迁移；通知/文件选择器未人工验收；unsigned HAP。gpt-6-astra/high与首条prompt SHA已核实。 日间优先 |

## 更新镜像补测（独立记录）

原11组结果保留；本批用户授权立即启动，豁免夜间窗口。

| 模型 | 状态 | 基础镜像 | 记录 |
|---|---|---|---|
| DeepSeek Flash / deepseek-flash | 迁移自报完成；未独立验收 | `mobile-harness-deveco-v2-20261103` | 更新镜像独立补测，完整npm DevEco0.2.3 + devecocli1.3.4。已通过15分钟全会话静默复核，归档723普通文件与4个内部相对链接，源码/产物/原生日志SHA核验通过，专属手机/relay/VM停止，结果磁盘保留。自报23ETS、9页面、4组件、HAP和运行截图；限制英文单语、无PiP/WearOS/后台通知、未注册外部深链。未独立验收。首条消息仅1条、正文一致，末尾LF变空格。 |
| GLM / glm-5.3 | 迁移自报完成；未独立验收 | `mobile-harness-deveco-v2-20261103` | 更新镜像独立补测，完整npm DevEco0.2.3 + devecocli1.3.4。已通过15分钟全3会话静默复核，归档757普通文件与4个内部相对链接，源码/产物/原生日志SHA核验通过，专属手机/relay/VM停止，结果磁盘保留。自报25源文件、8页面、en/zh双语、RDB、调试签名HAP与50项逻辑单测通过。交互未触控验证；PiP/后台计时/WearOS/动态取色/波浪进度环未迁移。未独立验收。首条消息仅1条、正文一致，末尾LF变空格。 |
| MiniMax / MiniMax-M3 | 失败（模型服务额度耗尽）；未独立验收 | `mobile-harness-deveco-v2-20261103` | 独立补测，保留全部旧结果。模型与设备预检通过；正式首轮请求因Token Plan额度耗尽HTTP429（2056）失败，原生assistant已记录结束，无迁移工具调用和迁移产物。已归档355个原始源码文件及原生日志并校验SHA，专属手机/relay/VM已停止，磁盘保留。不判为harness兼容性失败，不自动重跑。原生首条用户消息仅1条，正文一致、末尾LF变空格。 |
| Qwen / qwen3.8-max | 迁移运行中；未独立验收 | `mobile-harness-deveco-v2-20261103` | 独立补测，保留全部旧结果。8CPU/8GiB，图形Tart与可见Terminal前台全自动。模型与设备预检通过。原生首条用户消息仅1条，正文一致、末尾LF变空格。已开始自主读取源码。 |
| DeepSeek Pro / deepseek-v4-pro | 自报完成，待静默复核；未独立验收 | `mobile-harness-deveco-v2-20261103` | 独立补测，保留全部旧结果。8CPU/8GiB，图形Tart与可见Terminal前台--auto。模型文本/绝对路径文件读取/shell、工具链及手机Demo预检通过。用户授权本组立即启动，其余配置保持。原生日志仅一条初始用户消息，正文一致但末尾LF转换为空格，非字节精确SHA对照；已开始工具调用。未独立验收。 2026-11-04 02:20Z整体自报完成，待至少15分钟全会话静默复核后归档清理。自报构建/安装/启动成功，UI仅首页截图像素分析；PiP、后台通知、WearOS、深链、动态主题未实现，外链为toast、本地JSON备份，图标使用Emoji/Unicode。上述为agent自报，未独立验收。 |

## 实验口径与待锁定项

- 固定源码：`e3212d7090b0dd3d81ec5a31cb0b0641f68c865a`。每组独立 Tart，8 CPU / 8 GiB，图形化和可见 Terminal。
- Codex 使用 gpt-6-astra + ChatGPT 登录；实际默认 reasoning effort 为 medium，按用户要求显式设置 high。DeepSeek / GLM 限北京时间 20:00–08:00 启动，最多两台 Tart 并行。
- 六组历史完成记录已确认复用。历史 Claude Code 为 2.1.267，基础镜像与 prompt 存在差异，不能宣称完全等条件对照。
- DeepSeek Pro 采用 10/28 重测；10/27 对旧版的测试不混入。其他历史测试存在定位/观测阻塞，不展示为有效综合分。
- 镜像栏为已核实存在的本地 Tart 克隆名称；远程下载地址尚未提供。发布结果镜像前需去除凭据。本页未上传磁盘或原始日志。
- OpenCode + GLM、Codex + GLM、DSH + GLM 和双账号实验不计入本矩阵。

[结构化数据](../data/cofi-android-harmony.json) · [HTML 页面](cofi-android-harmony.html)
