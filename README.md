# HMBot Benchmark Dashboard

[打开阶段1-所有model harness组合的A2H实验](experiments/cofi-android-harmony.md)

独立页面：`experiments/cofi-android-harmony.html`，含 11 组实验、状态筛选及历史结果镜像登记。HTML 可直接打开，也可使用任意静态服务托管。

数据源：`data/cofi-android-harmony.json`。更新数据后运行 `python3 scripts/render.py` 同步生成 HTML 和 GitHub 文档版。页面登记执行进度与历史证据；实验调度由独立队列管理。阶段1复用6组历史结果、补跑5组，最多2台Tart并行，DeepSeek/GLM在北京时间夜间启动。

六组历史迁移自报完成不代表独立验收通过；本地 Tart 克隆名称不等于远程下载地址。已启用 GitHub Pages：<https://fuxi-ailabs.github.io/hmbot-benchmark-dashboard/>。

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

核对差异后，将 JSON、来源摘要、生成的 HTML/Markdown 和相关脚本提交并推送到 GitHub `main`，仓库中的文档页即更新。推送结果 JSON 后，GitHub Actions 会自动重新生成 HTML/Markdown 并触发现有 GitHub Pages 部署，不需要手工提交生成页。

本批口径：功能分采用各产物最新有效合并结果，通过数除以全部 335 个用例；受阻不从分母移除。历史原始通过另行标注。UI 保留对应安装包的评分及页数。Token 包含缓存读取和写入，按 Harness 原生统计，不能作为账单金额或不含缓存的 Token 比较；耗时口径逐行披露，历史日志跨度可能包含人工等待。

## 在线访问与自动更新

在线地址：<https://fuxi-ailabs.github.io/hmbot-benchmark-dashboard/experiments/cofi-android-harmony.html#migration-results>

GitHub Pages 已配置为 `main` 的 `/ (root)`。工作流 [Update migration dashboard](https://github.com/fuxi-ailabs/hmbot-benchmark-dashboard/actions/workflows/update-dashboard.yml) 会在 `main` 收到 `data/**`、生成脚本、首页或工作流的修改后：

1. 读取仓库内最新结果 JSON，生成 HTML 和 GitHub Markdown 文档。
2. 检查指标格式和运行 ID，提交生成页及 `data/site-version.json`。
3. 显式请求 Pages 构建。机器人提交本身不会触发分支式 Pages 发布，因此此步骤不可省略。

日常只需把已核实的指标写入 `data/cofi-android-harmony.json`，同时补充 `data/metrics-evidence.json` 的来源摘要，提交并推送到 `main`。新增产物登记独立运行 ID，旧版本保留；不能仅把原始结果推到其他仓库或本地 `benchmark-runs/`，期待网页自动发现。

```sh
# 已在 Dashboard 仓库中更新对应记录及来源摘要后：
git diff --check
git add data/cofi-android-harmony.json data/metrics-evidence.json
git commit -m "Update migration evaluation results"
git push origin HEAD:main
```

有已审核的本地来源映射时可以先运行 `scripts/import_metrics.py`。该脚本依赖本地证据，覆盖已映射的指标；新增或更新测评须先修改映射，避免用旧摘要覆盖新结果。云端工作流不会运行它，也不需要本地磁盘、设备、模型密钥或原生日志。

推送后查看 Actions 和 Pages 部署是否成功，再访问在线 `data/site-version.json`，核对 `ledger_sha256` 与本次结果 JSON 的 SHA-256 一致。页面受缓存和部署时间影响，浏览器刷新后生效；不是已打开页面的实时推送。工作流失败时保留原结果和日志；并发推送冲突时先检查最新 `main`，可手动运行工作流重试，不强推。

工作流仅写回生成文件，使用仓库自动提供的 `GITHUB_TOKEN`（contents/pages write），无需新增个人 Token。若组织策略禁止机器人写入或 Pages 构建，Actions 会显示错误，不应宣称发布成功。

## 按 App 浏览、筛选与排序

根目录 `index.html` 为 App 目录，点击卡片进入对应结果页。页面从现有记录的 `app` 字段自动分组；未提供 `app` 的历史记录归入 Cofi。目前另有 Simple Calendar、Omni Notes 的待测评记录。新增 App 时使用稳定且唯一的英文名称，例如 `app: "Simple-Calendar"`，执行生成器后会生成对应页面和入口。

结果页支持模型准确 ID、Harness、批次的组合筛选、文本搜索、重置，以及功能完备度、UI 分、Token 数和迁移耗时的升降序；点击指标表头也可排序。默认功能完备度降序；缺失指标始终最后，0 值正常排序。筛选与排序保留在网址参数中，可复制分享，其他 App 的记录不会混入当前表格。

批次优先取记录中明确填写的 `batch` 或 `batch_id`，建议新实验填写人可读、同批一致的名称。旧记录兼容使用阶段、运行 ID 日期、Prompt 等信息分组，不根据成绩或模型名称推断批次。

成绩按区间着色并加粗，历史口径、待测评及迁移失败有文字标签；逐行“评分说明与运行记录”中保留原始状态、备注和镜像信息。排序表示查看顺序，不能消除实验口径差异。完整历史内容仍保留在 Markdown 文档中。

生成器现在还使用 `scripts/render_dashboard.py` 生成多 App 页面，共用 `assets/dashboard.css` 与 `assets/dashboard.js`。修改这些文件后也会触发自动更新；工作流写回目录首页及所有 App 页。

## 静态访问密码

网站通过 `login.html` 输入访问密码，密码在 `assets/static-login.js` 中设置。登录状态保存在当前标签页的 sessionStorage，底部可退出；成功后返回原 App 或筛选视图。不包含用户名或访问日志。静态文件和源码仍公开可见，此功能不是服务端访问保护。
