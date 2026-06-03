import os

os.environ["OPENAI_API_KEY"] = "sk-1e55ff17d380430e9ed6d26dfd09a7ed"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# ============================================================
# 使用本地 Embeddings 模型（支持中文）
# ============================================================
print("📦 加载中文 Embeddings 模型（首次会下载，约 400MB）...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
print("✅ 模型加载完成\n")

# ============================================================
# 向量记忆类
# ============================================================
class VectorMemory:
    def __init__(self, persist_dir="./vector_memory_local"):
        self.persist_dir = persist_dir
        self.embeddings = embeddings
        self.vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings
        )
        self.memories = []
    
    def add(self, user_input, agent_response):
        memory_text = f"用户说：{user_input}\n助手回答：{agent_response}"
        
        self.vectorstore.add_texts(
            texts=[memory_text],
            metadatas=[{"user": user_input, "agent": agent_response}]
        )
        
        self.memories.append({
            "user": user_input,
            "agent": agent_response
        })
        print(f"💾 已记住：{user_input}")
    
    def search(self, query, k=10):
        results = self.vectorstore.similarity_search(query, k=k)
        if not results:
            return ""
        
        context = "【相关历史记忆】\n"
        for i, doc in enumerate(results, 1):
            context += f"{i}. {doc.page_content}\n"
        return context

# ============================================================
# 向量记忆 Agent
# ============================================================
class VectorMemoryAgent:
    def __init__(self):
        self.memory = VectorMemory()
    
    def respond(self, question):
        relevant_memory = self.memory.search(question)
        
        prompt = f"""
{relevant_memory}

【当前问题】
{question}

请根据历史记忆理解上下文，回答用户问题。
如果记忆中有相关信息，可以参考。
"""
        
        agent = Agent(
            role="智能助手",
            goal="友好地回答问题",
            backstory="你是一个有向量记忆的助手，能理解语义",
            verbose=True
        )
        
        task = Task(
            description=prompt,
            expected_output="友好的回答",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        
        self.memory.add(question, str(result))
        return result

# ============================================================
# 启动
# ============================================================
if __name__ == "__main__":
    agent = VectorMemoryAgent()
    
    print("\n" + "="*50)
    print("🧠 向量记忆 Agent 已启动（本地中文模型）")
    print("="*50)
    print("我能理解语义！比如你说'水果'，我能找到'苹果'")
    print("输入 'quit' 退出\n")
    
    while True:
        q = input("你：")
        if q.lower() in ['quit', 'q']:
            print("再见！")
            break
        
        answer = agent.respond(q)
        print(f"助手：{answer}\n")