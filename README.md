# prism-meta-bmclapi

**prism bmclapi meta镜像源，镜像自bmclapi**

A static mirror of [PrismLauncher meta](https://meta.prismlauncher.org/v1/) with all
download URLs rewritten to [BMCLAPI](https://bmclapi2.bangbang93.com/).

`PrismLauncher/meta-launcher` is shelled out of the _generator_ repo, so this project
simply post-processes the already generated output (same behaviour as `worker.js`)
and republishes it via GitHub Pages.

## How it works

1. GitHub Actions (daily, or manual) clones `PrismLauncher/meta-launcher`.
2. `scripts/patch_bmclapi.py` applies the `worker.js` host replacements and strips the
   `sha256`/`sha1` values from index entries plus the `checksum` of Java runtime
   entries served through BMCLAPI (Prism rejects a rewritten file whose advertised
   hash no longer matches; BMCLAPI re-serialises the runtime manifests it mirrors).
3. The result is placed under `_site/v1/` and pushed to the `gh-pages` branch.

## Endpoints

- GitHub Pages: `https://zhcn000000.github.io/prism-meta-bmclapi/v1/`
- Github Raw: `https://raw.githubusercontent.com/zhcn000000/prism-meta-bmclapi/gh-pages/v1/`
- JsDeliver: `https://fastly.jsdelivr.net/gh/zhcn000000/prism-meta-bmclapi@gh-pages/v1/`

## Configure Prism Launcher

Set the meta base URL to the `/v1/` endpoint above (it **must** end with `/v1/`,
Prism resolves `index.json` relative to it).

## License

MIT
