import os

os.environ["OPENAI_API_KEY"] = "sk-1e55ff17d380430e9ed6d26dfd09a7ed" 
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from crewai import Agent, Task, Crew

# ============================================================
# 1. 加载文档
# ============================================================
print("📖 加载文档...")
loader = TextLoader("knowledge_base.txt", encoding="utf-8")
documents = loader.load()

# ============================================================
# 2. 切分文档（把长文档分成小块）
# ============================================================
print("✂️ 切分文档...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 每块500字符
    chunk_overlap=50,    # 块之间重叠50字符
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
)
chunks = text_splitter.split_documents(documents)
print(f"   共切分为 {len(chunks)} 个文档块")

# ============================================================
# 3. 创建向量数据库（把文档块变成可检索的向量）
# ============================================================
print("🗄️ 创建向量数据库...")
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    openai_api_base=os.environ["OPENAI_BASE_URL"]
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 保存到本地
)

# ============================================================
# 4. 检索函数（根据问题查找相关文档）
# ============================================================
def retrieve_context(question: str, k: int = 3) -> str:
    """根据问题检索最相关的 k 个文档块"""
    results = vectorstore.similarity_search(question, k=k)
    context = "\n\n---\n\n".join([doc.page_content for doc in results])
    return context

# ============================================================
# 5. 创建 RAG Agent（根据检索结果回答问题）
# ============================================================
rag_agent = Agent(
    role="知识库助手",
    goal="根据提供的知识库内容回答问题",
    backstory="""你是一个专业的问答助手。
    你会根据提供的参考资料回答问题。
    如果参考资料中没有相关信息，请如实告知用户。""",
    verbose=True
)

# ============================================================
# 6. 交互式问答
# ============================================================
print("\n" + "="*50)
print("🤖 RAG 知识库问答系统已启动")
print("="*50)
print("知识库包含：机器学习、深度学习、大语言模型、RAG、Agent")
print("输入问题（输入 'quit' 退出）\n")

while True:
    question = input("💬 你问：")
    if question.lower() in ['quit', 'exit', 'q']:
        print("再见！")
        break
    
    # 检索相关文档
    context = retrieve_context(question)
    
    # 创建任务，把检索结果作为参考资料
    task = Task(
        description=f"""
请根据以下【参考资料】回答问题。

【参考资料】
{context}

【问题】
{question}

要求：
1. 只根据参考资料回答
2. 如果参考资料中没有相关信息，请说"知识库中没有找到相关信息"
3. 回答要简洁准确
""",
        expected_output="简洁准确的回答",
        agent=rag_agent
    )
    
    crew = Crew(agents=[rag_agent], tasks=[task])
    result = crew.kickoff()
    print(f"🤖 回答：{result}\n")