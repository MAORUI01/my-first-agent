import os

os.environ["OPENAI_API_KEY"] = "sk-1e55ff17d380430e9ed6d26dfd09a7ed"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew

# 读取知识库
with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# 按段落切分
chunks = []
current = []
for line in full_text.split("\n"):
    line = line.strip()
    if line == "" or line.startswith("#"):
        if current:
            chunks.append("\n".join(current))
            current = []
    else:
        current.append(line)
if current:
    chunks.append("\n".join(current))

print(f"📖 知识库共 {len(chunks)} 个段落")

def search(question):
    question_lower = question.lower()
    results = []
    
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0
        # 检查问题中的每个词
        for word in question_lower.split():
            if len(word) > 1 and word in chunk_lower:
                score += 1
        # 特殊关键词加分
        for kw in ["rag", "agent", "机器学习", "深度学习", "大语言模型", "llm"]:
            if kw in question_lower and kw in chunk_lower:
                score += 10
        
        if score > 0:
            results.append((score, chunk))
    
    results.sort(reverse=True)
    if not results:
        return chunks[0] if chunks else "知识库中没有找到相关信息"
    
    return "\n\n---\n\n".join([c for s, c in results[:2]])

agent = Agent(
    role="知识库助手",
    goal="根据参考资料回答问题",
    backstory="只根据参考资料回答",
    verbose=True
)

print("\n问答系统已启动\n")

while True:
    q = input("问：")
    if q.lower() in ['quit', 'q']:
        print("再见")
        break
    
    context = search(q)
    task = Task(
        description=f"参考资料：{context}\n\n问题：{q}\n只根据参考资料回答",
        expected_output="简短回答",
        agent=agent
    )
    result = Crew(agents=[agent], tasks=[task]).kickoff()
    print(f"答：{result}\n")