# 天空素材来源与使用说明

四张天空均为本轮通过 OpenAI `image_gen.imagegen` 实际生成的独立宽幅图片；不是图库下载，也不是旧背景改名。原始 PNG 原样保留在 `originals/`。未使用最初的四宫格预览。

| 文件 | 内容 | 原生像素 |
| --- | --- | --- |
| originals/day.png | 城市日间蓝天、层叠白云、暖阳 | 1774 × 887 |
| originals/night.png | 城市深蓝夜空、克制星点、薄云 | 1774 × 887 |
| originals/dawn.png | 生态廊道晨光、淡金云边 | 1774 × 887 |
| originals/dusk.png | 村落至湿地橙红、粉紫黄昏云层 | 1774 × 887 |

生成时明确请求 4096 × 2048、天空为主、无建筑/文字/近景树木。工具实际返回 1774 × 887，**没有达到 4K 原生分辨率要求**。未用插值放大冒充原生 4K。

统一提示词基调：Hong Kong migratory bird game; panoramic sky-only texture; realistic painterly photographic atmosphere; natural fine cloud detail; restrained contrast; horizon glow at bottom; no ground/buildings/trees/mountains/birds/text; landscape 2:1; portrait center-crop safe。四个版本分别指定 day / urban night without Milky Way / fresh golden-edged dawn / orange-pink-violet wetland dusk。

`tools/build-assets.py` 使用 Pillow/Lanczos 缩放并以 WebP 编码。桌面版本保留原生 1774 × 887（quality 84）；手机与离线版本为 960 × 480（quality 78）。具体字节数见 `manifest.json`。运行时不下载原始 PNG，保持比例 cover 裁切，不拉伸。只预载当前和下一种天空；桌面在小图就绪后升级。

使用许可：这些是本项目请求生成的输出，提供给项目使用、修改与部署；输出的权利归属与使用受适用 OpenAI 服务条款及当地法律约束（https://openai.com/policies/terms-of-use/）。未声明为 CC0、公共领域或具有独占版权，也未冒用第三方图库许可证。原游戏源码的许可状态不因本说明而改变。
