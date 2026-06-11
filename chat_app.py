import streamlit as st
import os

# ============================================================
# API Key 读取顺序：
# 1. 本地开发 → .env 文件
# 2. Streamlit Cloud → st.secrets（在后台设置）
# ============================================================

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 优先用 st.secrets（Streamlit Cloud），回退到 os.getenv（本地）
os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
os.environ["OPENAI_BASE_URL"] = st.secrets.get("OPENAI_BASE_URL", os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1"))
os.environ["OPENAI_MODEL_NAME"] = st.secrets.get("OPENAI_MODEL_NAME", os.getenv("OPENAI_MODEL_NAME", "deepseek-chat"))

from crewai import Agent, Task, Crew

st.set_page_config(page_title="我的AI助手", page_icon="🤖")
st.title("🤖 我的 AI Agent")
st.markdown("有记忆的智能助手")

# 初始化记忆
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 输入框
if prompt := st.chat_input("输入你的问题..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 构建记忆上下文
    context = ""
    for msg in st.session_state.messages[-5:]:
        if msg["role"] == "user":
            context += f"用户: {msg['content']}\n"
        else:
            context += f"助手: {msg['content']}\n"
    
    # 创建 Agent
    agent = Agent(
        role="智能助手",
        goal="友好地回答问题",
        backstory="你是一个有记忆的智能助手",
        verbose=False
    )
    
    task = Task(
        description=f"{context}\n请回答用户的问题：{prompt}",
        expected_output="友好的回答",
        agent=agent
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    response = crew.kickoff()
    
    # 显示助手回复
    with st.chat_message("assistant"):
        st.write(str(response))
    st.session_state.messages.append({"role": "assistant", "content": str(response)})