# HMBot Benchmark Dashboard

[打开阶段1-所有model harness组合的A2H实验](experiments/cofi-android-harmony.md)

独立页面：`experiments/cofi-android-harmony.html`，含 11 组实验、状态筛选及历史结果镜像登记。HTML 可直接打开，也可使用任意静态服务托管。

数据源：`data/cofi-android-harmony.json`。更新数据后运行 `python3 scripts/render.py` 同步生成 HTML 和 GitHub 文档版。页面登记执行进度与历史证据；实验调度由独立队列管理。阶段1复用6组历史结果、补跑5组，最多2台Tart并行，DeepSeek/GLM在北京时间夜间启动。

六组历史迁移自报完成不代表独立验收通过；本地 Tart 克隆名称不等于远程下载地址。尚未配置 GitHub Pages。

## 迁移测评结果

现有 HTML 与文档版均包含“迁移测评结果”区，按运行 ID 展示原始实验和补测。为对应 `experiments` 或 `retests` 记录填写 `metrics`，再运行 `python3 scripts/render.py`：

```json
"metrics": {
  "functional_score": null,
  "ui_score": null,
  "total_tokens": null,
  "duration_seconds": null
}
```

- `functional_score`、`ui_score`：0–100 分，可包含小数；其他评分量表须先换算为百分制。
- `total_tokens`：迁移运行消耗的总 Token，非负整数，按对应 Harness 的统计口径填写；不同 Harness 的缓存、推理 Token 口径差异需在记录备注中说明。
- `duration_seconds`：迁移任务开始到结束的墙钟耗时，单位为秒，非负整数；不包含后续独立验收耗时。
- 缺失字段或 `null` 显示“待发布”；真实的 `0` 正常显示。请从已核实的测评和运行记录录入，不用迁移自报状态推断分数。

展示区位于实验进度表之前，可通过 HTML 页面的 `#migration-results` 直接定位。进度表的筛选只作用于进度记录。

### 从本地证据导入与发布

在迁移工作目录下，Dashboard 仓库与 `experiments/`、`benchmark-runs/` 等证据目录同级时，执行：

```sh
python3 scripts/import_metrics.py
python3 scripts/render.py
git diff --check
git diff -- data/cofi-android-harmony.json experiments/cofi-android-harmony.md
```

导入器按安装包版本映射原始实验和补测，核验安装包 SHA-256。它只输出指标、计数、来源文件哈希及统计说明到 `data/metrics-evidence.json`，不会复制原生日志或凭据。新增实验的来源映射需在导入器中显式登记；缺失指标保持 `null`。导入器会重建已有映射的指标和说明，手工修正应先更新对应证据与映射。

核对差异后，将 JSON、来源摘要、生成的 HTML/Markdown 和相关脚本提交并推送到 GitHub `main`，仓库中的文档页即更新。HTML 是可直接打开的静态页面；对外提供网页地址需要另行配置 GitHub Pages。

本批口径：功能分采用各产物最新有效合并结果，通过数除以全部 335 个用例；受阻不从分母移除。历史原始通过另行标注。UI 保留对应安装包的评分及页数。Token 包含缓存读取和写入，按 Harness 原生统计，不能作为账单金额或不含缓存的 Token 比较；耗时口径逐行披露，历史日志跨度可能包含人工等待。

## 在线访问（GitHub Pages）

仓库已包含根目录 `index.html` 入口和 `.nojekyll`，启用 Pages 后可以直接托管现有 HTML，无需额外构建。

仓库管理员或维护者首次进入 [Settings → Pages](https://github.com/mig-everything/hmbot-benchmark-dashboard/settings/pages)，在 Build and deployment 中选择：

- Source：Deploy from a branch
- Branch：`main`
- Folder：`/ (root)`
- 点击 Save，等待 GitHub Pages 部署完成。

默认访问地址（仅在成功启用并部署后可用）：

- 首页：<https://mig-everything.github.io/hmbot-benchmark-dashboard/>
- 实验页面：<https://mig-everything.github.io/hmbot-benchmark-dashboard/experiments/cofi-android-harmony.html>
- 直接定位成绩：<https://mig-everything.github.io/hmbot-benchmark-dashboard/experiments/cofi-android-harmony.html#migration-results>

后续将生成的 HTML 和数据推送到 `main` 即会触发在线更新，无需再次设置。启用 Pages 要求仓库 admin 或 maintain 权限，只有 push 权限的账号无法开启。当前准备好静态文件不代表 Pages 已成功启用。
