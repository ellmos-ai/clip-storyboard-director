# Third-Party Licenses & Software Inventory

**Project:** `clip-storyboard-director`  
**License:** [MIT License](LICENSE)  
**Audit Date:** 2026-09-09  

---

## Runtime Architecture & Dependencies

`clip-storyboard-director` is engineered as a local-first, privacy-respecting video production director.

### Runtime Dependencies

| Package | Version Spec | License | Purpose |
| :--- | :--- | :--- | :--- |
| [PyYAML](https://github.com/yaml/pyyaml) | `>=6.0` | MIT | Declarative project configuration and 4D persistence buffer parsing |
| [edge-tts](https://github.com/rany2/edge-tts) | `>=6.1.0` | GPL-3.0 | Local speech synthesis for dialogue and voiceover generation |
| [websocket-client](https://github.com/websocket-client/websocket-client) | `>=1.6.0` | Apache-2.0 | Chrome DevTools Protocol (CDP) communication with Edge browser |
| [requests](https://github.com/psf/requests) | `>=2.28.0` | Apache-2.0 | HTTP communication for CDP target discovery on `127.0.0.1:9222` |

---

## Development & Test Dependencies

The following tools and libraries are utilized during development, linting, packaging, and automated test execution:

| Package / Tool | Version Spec | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [pytest](https://pytest.org/) | `>=7.0` | MIT | `[dev]` | Automated unit, contract, and regression test runner |
| [ruff](https://github.com/astral-sh/ruff) | `>=0.1.0` | MIT OR Apache-2.0 | `[dev]` | High-performance Python linter and code formatting validation |
| [setuptools](https://github.com/pypa/setuptools) | `>=61.0` | MIT | `[build-system]` | Standard Python packaging and build backend |

---

## External Tools & Binaries (System Level)

| Binary | Recommended Version | License | Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [FFmpeg / FFprobe](https://ffmpeg.org/) | `>=4.4` | LGPL-2.1+ / GPL-2.0+ | System PATH | Media probing, clue-frame extraction, video stitching, audio ducking |
| [Microsoft Edge](https://www.microsoft.com/edge) | Any modern build | Proprietary | Optional | Dual-pane cockpit display and CDP automation |

---

## License Texts & Attribution

### MIT License (`clip-storyboard-director`, `PyYAML`, `pytest`, `setuptools`)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Apache License 2.0 (`websocket-client`, `requests`, `ruff`)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
