# prism-meta-bmclapi

A static mirror of [PrismLauncher meta](https://meta.prismlauncher.org/v1/) with all
download URLs rewritten to [BMCLAPI](https://bmclapi2.bangbang93.com/).

`PrismLauncher/meta-launcher` is shelled out of the *generator* repo, so this project
simply post-processes the already generated output (same behaviour as `worker.js`)
and republishes it via GitHub Pages.

## How it works

1. GitHub Actions (daily, or manual) clones `PrismLauncher/meta-launcher`.
2. `scripts/patch_bmclapi.py` applies the `worker.js` host replacements and strips the
   `sha256`/`sha1` values from index entries (Prism rejects a rewritten file whose
   advertised hash no longer matches).
3. The result is placed under `_site/v1/` and pushed to the `gh-pages` branch.

## Endpoints

- GitHub Pages: `https://<OWNER>.github.io/<REPO>/v1/`
- raw (useful behind a GitHub proxy):

  ```
  https://raw.githubusercontent.com/<OWNER>/<REPO>/gh-pages/v1/
  https://gh-proxy.com/https://raw.githubusercontent.com/<OWNER>/<REPO>/gh-pages/v1/
  ```

## Configure Prism Launcher

Set the meta base URL to the `/v1/` endpoint above (it **must** end with `/v1/`,
Prism resolves `index.json` relative to it).

## Notes

- Output is a point-in-time snapshot; new Minecraft/loader versions appear up to a
  day late. Trigger the workflow manually (`workflow_dispatch`) to refresh.
- Hosts not covered by the replacement list (`repo1.maven.org`, `files.prismlauncher.org`,
  `archive.org`, ...) are left untouched, exactly like `worker.js`.
- Do **not** copy `PrismLauncher/meta-launcher`'s `.github/CNAME`: it points at
  `meta.prismlauncher.org`.
