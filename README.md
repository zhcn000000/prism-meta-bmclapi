# prism-meta-bmclapi

**[PrismLauncher](https://meta.prismlauncher.org/v1/) 元数据（meta）的国内镜像，所有下载地址已改写为 [BMCLAPI](https://bmclapi2.bangbang93.com/)。**

本仓库不再自己跑生成器：上游 `PrismLauncher/meta-launcher` 已经负责生成，
用 GitHub Pages 发布，无需独立worker nginx反代等，填写链接即可

## 工作原理

1. GitHub Actions 每天定时（UTC 03:17）或手动触发，浅克隆 `PrismLauncher/meta-launcher`。
2. `scripts/patch_bmclapi.py` 按 `worker.js` 的规则替换下载地址的域名，并删掉两类
   已经失效的校验值：
   - 索引文件（`index.json`）里 `versions`/`packages` 条目的 `sha256`/`sha1`；
   - 走 BMCLAPI 的 Java 运行时条目的 `checksum`（BMCLAPI 会把转发的 runtime
     manifest 重新序列化，字节变了但内容一致，哈希必然对不上）。

   Prism 对“声称的哈希与实际文件不符”是硬失败（Checksum mismatch），所以必须剥掉。
   未改写的地址（如 Adoptium 的运行时）会保留校验值，那边的文件是原样字节。
3. 处理结果放到 `_site/v1/`，再用 `peaceiris/actions-gh-pages` 推到 `gh-pages` 分支。

## 可用地址

- GitHub Pages：`https://zhcn000000.github.io/prism-meta-bmclapi/v1/`
- GitHub Raw：`https://raw.githubusercontent.com/zhcn000000/prism-meta-bmclapi/gh-pages/v1/`
- JsDelivr：`https://fastly.jsdelivr.net/gh/zhcn000000/prism-meta-bmclapi@gh-pages/v1/`

## 在 Prism Launcher 里配置

把 meta 地址设为上面任意一个 `/v1/` 结尾的地址（**必须以 `/v1/` 结尾**，Prism 会相对它
解析 `index.json`）。

## 自检

```bash
python3 scripts/test_patch_bmclapi.py
```

## 许可证

MIT
