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
| 实时视频流 | 摄像头实时分析 | `webcam_agent_fixed.py` |

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

# 4. 配置 API Key
export OPENAI_API_KEY="你的DeepSeek Key"
export ZHIPUAI_API_KEY="你的智谱 Key"

# 5. 运行示例
python agent_demo.py