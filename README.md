# Heliotrope

[![CI](https://github.com/Saebasol/Heliotrope/actions/workflows/ci.yml/badge.svg)](https://github.com/Saebasol/Heliotrope/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Saebasol/Heliotrope/branch/main/graph/badge.svg?token=CKRUjYaPSW)](https://codecov.io/gh/Saebasol/Heliotrope)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/Saebasol/Heliotrope?include_prereleases)](https://github.com/Saebasol/Heliotrope/releases)
[![Discord](https://img.shields.io/discord/725643500171034691)](https://discord.saebasol.org)

> Hitomi.la mirror api

## Feature

* 🚀 Very fast response and processing with [Sanic framework](https://sanic.dev/).
* ⚡ Blazingly fast search with [MongoDB](https://www.mongodb.com/).
* 🔄 Galleryinfo, Info auto mirroring with [Sunflower](https://github.com/Saebasol/Sunflower).
* 🖼️ Pixiv.net, Hitomi.la image proxying.
* 🏡 Production ready with [Bouquet](#related-projects).
* 🧑‍💻 Easy to use SDKs for Python, JS/TS, Rust.
* 📚 Friendly [documentation](https://github.com/Saebasol/Heliotrope/wiki/) on how to configure.


## Languages ​​supported by Saebasol

If you've deploy your API publicly and would like someone to use it, please let me know on [Discord](https://discord.saebasol.org)!

* Korean: https://heliotrope.saebasol.org (MongoDB Atlas Search Supported)
* English, Japanese, Korean: https://inst.psec.dev

[Other languages](https://github.com/Saebasol/Heliotrope/wiki/Configuration#supported-index-files) ​​can also be used by users who distribute Heliotrope themselves!

## SDK

### Python
* [Delphinium](https://github.com/Saebasol/Delphinium)
```sh
pip install delphinium
```

### JS/TS
* [Delphinium-js](https://github.com/Saebasol/Delphinium-js)
```sh
npm install @saebasol/delphinium
# or
yarn add @saebasol/delphinium
# or
pnpm add @saebasol/delphinium
```

### Rust
* [delphinium-rs](https://github.com/Saebasol/delphinium-rs)
```toml
[dependencies]
delphinium = "1.0.0"
``` 


## Related Projects

* [Yggdrasil](https://github.com/Saebasol/Yggdrasil)
  * Common components shared between Saebasol's related projects.
* [Sunflower](https://github.com/Saebasol/Sunflower)
  * A mirroring tool for Hitomi.la galleryinfo and info files. Used to keep Heliotrope's database up to date.
* [Hibiscus](https://github.com/Saebasol/Hibiscus)
  * A modern, self-hostable manga reader with a beautiful interface built on top of Heliotrope.
* [Bouquet](https://github.com/Saebasol/Bouquet)
  * Bouquet is a easy deployment solution for Heliotrope, Sunflower and Hibiscus.
* [Hyacinth](https://github.com/Saebasol/Hyacinth)
  * A tool to create a personal offline manga library. depends on Heliotrope for metadata.
  
