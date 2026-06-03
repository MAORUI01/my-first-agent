# 🤖 AI Agent 完整项目集

一个从零搭建的 AI Agent 项目，涵盖对话、记忆、工具、RAG、多模态、视频理解等核心能力。

## 📚 项目列表

| 项目 | 功能 | 文件 |
|------|------|------|
| 基础 Agent | 大模型对话 | `agent_demo.py` |
| 搜索工具 | Agent 联网搜索 | `agent_with_search.py` |
| 文件读写 | Agent 读取本地文件 | `agent_with_file_tool.py` |
| 多 Agent 协作 | 研究员 + 写手 + 编辑 | `multi_agent_team.py` |
| RAG 知识库 | 基于文档问答 | `rag_simple.py` |
| 长期记忆 | JSON 文件记忆 | `agent_with_memory.py` |
| 向量记忆 | 语义搜索记忆 | `vector_memory_local.py` |
| 网页界面 | Streamlit 聊天 | `chat_app.py` |
| 多模态 | 图片理解 | `multimodal_agent.py` |
| 视频理解 | 视频内容分析 | `video_agent.py` |
| 实时视频流 | 摄像头实时分析 | `webcam_agent.py` |

## 🛠️ 技术栈

- **框架**: CrewAI, LangChain
- **大模型**: DeepSeek API, 智谱 GLM-4V
- **向量数据库**: Chroma
- **前端**: Streamlit
- **部署**: GitHub

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/MAORUI01/my-first-agent.git
cd my-first-agent

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API Key（不要写死到代码里！）
export OPENAI_API_KEY="你的DeepSeek Key"
export ZHIPUAI_API_KEY="你的智谱 Key"

# 5. 运行示例
python agent_demo.py
```

## 📖 核心能力演示

### 长期记忆
Agent 能记住用户信息，关闭程序也不丢失。

### 向量记忆（语义搜索）
理解语义关联，而非关键词匹配。

### RAG 知识库
基于本地文档回答问题。

### 多模态（看图）
分析图片内容，支持 GLM-4V 视觉模型。

### 视频理解
分析视频内容，提取关键帧并理解画面。

## 🔐 安全说明

所有 API Key **必须通过环境变量设置**，切勿写死在代码中或提交到 GitHub。

```bash
# 正确做法：每次终端启动时设置
export OPENAI_API_KEY="your-key-here"
```

## 📁 项目结构

```
my_ai_project/
├── agent_demo.py              # 基础 Agent
├── agent_with_memory.py       # 长期记忆
├── vector_memory_local.py     # 向量记忆
├── rag_simple.py              # RAG 知识库
├── multi_agent_team.py        # 多 Agent 协作
├── multimodal_agent.py        # 图片理解
├── video_agent.py             # 视频理解
├── webcam_agent.py            # 实时视频流
├── chat_app.py                # 网页界面
└── knowledge_base.txt         # 知识库文件
```

## 📝 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | DeepSeek API Key |
| `OPENAI_BASE_URL` | `https://api.deepseek.com/v1` |
| `OPENAI_MODEL_NAME` | `deepseek-chat` |
| `ZHIPUAI_API_KEY` | 智谱 AI Key（用于多模态） |

## ✅ 安全提示

⚠️ **不要把真实 API Key 写进代码！**
⚠️ **提交前检查是否包含敏感信息！**

建议使用 `.env` 文件管理 Key（已加入 `.gitignore`）：
```bash
# .env
OPENAI_API_KEY=your-deepseek-key
ZHIPUAI_API_KEY=your-zhipu-key
```

## 👤 作者

MAORUI01

## 📄 许可

MIT
