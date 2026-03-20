# Topaz Video CLI

基于 Topaz Video AI 的视频处理命令行工具，支持视频增强、超分辨率、稳定化和帧插值。

[English](./README.md) | 中文

---

## 功能特性

- 🎬 视频超分辨率增强 (Iris, Artemis, Proteus 等 AI 模型)
- 🔧 支持自定义质量参数 (码率、量化值)
- 📦 完整的参数映射 (GUI 到 CLI)
- ✅ 25+ 测试用例，100% 通过率

---

## 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/你的用户名/topaz-video-cli.git
cd topaz-video-cli

# 安装 Python 依赖
pip install -e .
```

**依赖要求：**
- Python 3.9+
- [Topaz Video AI](https://topazlabs.com/video-ai/) (需安装于 `/Applications/Topaz Video.app`)

### 2. 基本用法

```bash
# 查看帮助
topaz-video --help

# 探测视频信息
topaz-video probe input.mp4

# 2倍超分辨率增强
topaz-video process input.mp4 output.mp4 --model enhance --scale 2 --ai-model iris-2
```

---

## 部署指南

### Claude Code 部署

Claude Code 是 Anthropic 官方的 CLI 工具。

#### 方式一：从 GitHub 安装

```bash
# 1. 克隆项目到 Claude Code 插件目录
cd ~/.claude/plugins
git clone https://github.com/你的用户名/topaz-video-cli.git topaz-video

# 2. 重新加载插件
/reload-plugins

# 3. 验证安装
topaz-video --help
```

#### 方式二：使用 plugin install 命令

```bash
# 安装最新版本
/plugin install topaz-video@github:你的用户名/topaz-video-cli

# 安装指定版本
/plugin install topaz-video@github:你的用户名/topaz-video-cli@v1.0.0
```

#### 方式三：本地开发模式

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/topaz-video-cli.git
cd topaz-video-cli

# 2. 创建符号链接
mkdir -p ~/.claude/plugins
ln -s $(pwd) ~/.claude/plugins/topaz-video

# 3. 重新加载
/reload-plugins
```

#### 验证 Claude Code 安装

```bash
# 测试 CLI
topaz-video info

# 应该显示类似输出：
# Topaz Video CLI
# App Location: /Applications/Topaz Video.app
# FFmpeg: /Applications/Topaz Video.app/Contents/MacOS/ffmpeg
```

---

### OpenClaw 部署

OpenClaw 是一个开源的 AI Agent 工具，支持类似的 skill 系统。

#### 方式一：项目内安装 (推荐)

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/topaz-video-cli.git

# 2. 复制 skill 到你的项目
cp -r topaz-video-cli/.openclaw/skills/topaz-video your-project/skills/

# 3. 清理
rm -rf topaz-video-cli

# 4. 在项目中使用
cd your-project
openclaw
```

#### 方式二：全局安装

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/topaz-video-cli.git

# 2. 创建全局 skills 目录
mkdir -p ~/.openclaw/skills

# 3. 复制 skill
cp -r topaz-video-cli/.openclaw/skills/topaz-video ~/.openclaw/skills/

# 4. 清理
rm -rf topaz-video-cli
```

#### 验证 OpenClaw 安装

```bash
# 检查状态
openclaw status

# 应该显示 topaz-video skill 已加载
```

---

## 命令详解

### probe - 探测视频信息

```bash
topaz-video probe <video_path>
topaz-video probe video.mp4 --json
```

### process - 视频处理 (核心命令)

```bash
topaz-video process <input> <output> [OPTIONS]
```

#### 模型选项

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--model` | 处理模式 | `upscale`, `enhance`, `stabilize`, `interpolate` |
| `--ai-model` | AI 模型名称 | 见下方 |
| `--scale` | 放大倍数 | 1, 2, 4, 8 |

#### AI 模型列表

| GUI 显示 | CLI 名称 | 适用场景 |
|---------|---------|---------|
| Iris | `iris-2` | 通用增强，快速处理 |
| Artemis | `artemis` | 动漫/卡通 |
| Proteus | `proteus` | 高质量通用 |
| Rhea | `rhea` | 速度优先 |
| Nyx | `nyx` | 高分辨率源 |
| Theia | `theia` | 最高质量 |
| GFX | `gfx` | 图形/屏幕录制 |

#### 质量参数

| 参数 | GUI 对应 | 范围 |
|------|---------|------|
| `--noise` | Add noise | -1 到 1 |
| `--details` | Recover detail | -1 到 1 |
| `--blur` | Sharpen | -1 到 1 |
| `--preblur` | Anti-alias/deblur | -1 到 1 |
| `--halo` | Dehalo | -1 到 1 |
| `--compression` | Revert compression | -1 到 1 |
| `--grain` | Grain | 0 到 1 |

#### 输出质量控制

| 参数 | 说明 | 示例 |
|------|------|------|
| `--bitrate` | 视频码率 | `2000k`, `5M`, `10M` |
| `--qv` | 量化值 (1-1024) | 越大质量越低 |
| `--crf` | CRF 质量 (0-51) | 越小质量越好 |
| `--codec` | 编码器 | `h264_videotoolbox` |
| `--audio-bitrate` | 音频码率 | `128k` |

### convert - 视频格式转换

```bash
topaz-video convert input.mp4 output.mov --codec h264_videotoolbox
topaz-video convert input.mp4 output.mov --codec prores_videotoolbox
```

---

## 使用示例

### 示例 1: 2 倍放大，保持原码率

```bash
# 先探测原视频码率
topaz-video probe input.mp4

# 处理 (使用原码率)
topaz-video process input.mp4 output_2x.mp4 \
  --model enhance \
  --ai-model iris-2 \
  --scale 2 \
  --bitrate 2000k
```

### 示例 2: 低质量视频增强

```bash
topaz-video process input.mp4 output.mp4 \
  --model enhance \
  --ai-model proteus \
  --scale 2 \
  --noise 0.3 \
  --details 0.5
```

### 示例 3: 视频稳定化

```bash
topaz-video process shaky.mp4 stable.mp4 \
  --model stabilize \
  --smoothness 8
```

### 示例 4: 慢动作

```bash
topaz-video process input.mp4 slowmo.mp4 \
  --model interpolate \
  --slowmo 2 \
  --fps 60
```

### 示例 5: JSON 输出 (程序调用)

```bash
topaz-video --json probe video.mp4
topaz-video --json process input.mp4 output.mp4 --model enhance --ai-model iris-2 --scale 2
```

---

## 常见问题

### Q: 遇到 "Model not found" 错误？

**解决方法**：首次使用前，先在 Topaz Video GUI 中选择该模型并下载。

### Q: 输出文件太大？

**解决方法**：使用 `--bitrate` 参数控制码率。
```bash
--bitrate 2000k   # 约 2Mbps
--bitrate 5000k   # 约 5Mbps
```

### Q: 如何查看日志？

```
~/Library/Application Support/Topaz Labs LLC/Topaz Video/logs/
```

---

## 项目结构

```
topaz-video-cli/
├── .openclaw/                    # OpenClaw skill 配置
│   └── skills/
│       └── topaz-video/
│           └── SKILL.md
├── cli_anything/                 # Python 包
│   └── topaz_video/
│       ├── topaz_video_cli.py   # CLI 入口
│       ├── utils/
│       │   └── topaz_video_backend.py
│       └── tests/
├── SKILL.md                      # Claude Code skill 定义
├── README.md                     # 英文文档
├── README-zh.md                  # 中文文档
└── setup.py                      # Python 包配置
```

---

## 开发相关

### 运行测试

```bash
pytest cli_anything/topaz_video/tests/ -v
```

### 本地安装

```bash
pip install -e .
topaz-video --help
```

---

## 许可证

MIT License

---

## 参考链接

- [Topaz Video AI](https://topazlabs.com/video-ai/)
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code/overview)
- [OpenClaw GitHub](https://github.com/open-ai/OpenClaw)

## Star History

<a href="https://www.star-history.com/?repos=thy950523%2Ftopaz-video-cli&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=thy950523/topaz-video-cli&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=thy950523/topaz-video-cli&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/image?repos=thy950523/topaz-video-cli&type=date&legend=top-left" />
 </picture>
</a>