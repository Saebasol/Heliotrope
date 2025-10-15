# Heliotrope

[![CI](https://github.com/Saebasol/Heliotrope/actions/workflows/ci.yml/badge.svg)](https://github.com/Saebasol/Heliotrope/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Saebasol/Heliotrope/branch/main/graph/badge.svg?token=CKRUjYaPSW)](https://codecov.io/gh/Saebasol/Heliotrope)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/Saebasol/Heliotrope?include_prereleases)](https://github.com/Saebasol/Heliotrope/releases)

> Hitomi.la mirror api

## Feature

* 🚀 Very fast response and processing with [Sanic framework](https://sanic.dev/)
* ⚡ Blazingly fast search with [MongoDB](https://www.mongodb.com/)
* 🔄 Galleryinfo, Info auto mirroring.
* 🖼️ Pixiv.net, Hitomi.la image proxying.
* 🏡 Production ready with [Bouquet](#related-projects)
* 🧑‍💻 Easy to use SDKs for Python, JS/TS, Rust.
* 📚 Friendly [documentation](https://github.com/Saebasol/Heliotrope/wiki) on how to configure.


## Languages ​​supported by Saebasol

* English: https://en.heliotrope.saebasol.org
* Japanese: https://ja.heliotrope.saebasol.org
* Korean: https://heliotrope.saebasol.org (MongoDB Atlas Search Supported)

Other languages ​​can also be used by users who distribute Heliotrope themselves!

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

* [Hibiscus](https://github.com/Saebasol/Hibiscus)
  * A modern, self-hostable manga reader with a beautiful interface built on top of Heliotrope.
* [Bouquet](https://github.com/Saebasol/Bouquet)
  * Bouquet is a easy deployment solution for Heliotrope and Hibiscus.
* [Hyacinth](https://github.com/Saebasol/Hyacinth)
  * A tool to create a personal offline manga library. depends on Heliotrope for metadata.
  
