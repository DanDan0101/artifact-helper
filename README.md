# Genshin Impact artifact helper

1. Use a screen-recording software such as [OBS Studio](https://obsproject.com/) to record a video of you clicking through all the artifacts in your inventory. My video has the following properties:
    * File format: `.mkv`
    * Resolution: $1620\times1080$
    * Frame rate: 30 fps
    * Video codec: H.264
2. Preprocess the video into a series of cropped photos showing the artifact information for each artifact.
3. Use [Python-tesseract](https://github.com/madmaze/pytesseract) to perform optical character recognition (OCR) on the cropped photos.
4. Parse each OCR output into Artifact objects.
5. Export all Artifacts to JSON, according to the [Genshin Open Object Description (GOOD) V3](https://frzyc.github.io/genshin-optimizer/#/doc) standard.

## Installation

This repository uses [pixi](https://pixi.prefix.dev/latest/) for package management ([installation instructions](https://pixi.prefix.dev/latest/installation/)).

After installing pixi, simply run `pixi shell` within this repository's root directory.
