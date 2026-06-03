import os

# 设置编码
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-deepseek-api-key")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew

# ============================================================
# 1. 先用 Python 读取文件（不经过 Agent）
# ============================================================
file_path = "knowledge.txt"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    print(f"✅ 成功读取文件，共 {len(file_content)} 个字符")
except FileNotFoundError:
    print(f"❌ 文件 {file_path} 不存在！")
    exit(1)
except Exception as e:
    print(f"❌ 读取文件出错: {e}")
    exit(1)

# ============================================================
# 2. 创建 Agent（只负责处理内容，不负责读文件）
# ============================================================
agent = Agent(
    role="文档分析专家",
    goal="分析文档内容并总结",
    backstory="你擅长从文档中提取关键概念",
    verbose=True
)

# ============================================================
# 3. 任务：分析文件内容
# ============================================================
task = Task(
    description=f"""
请分析以下文档内容，然后完成：
1. 总结文档中讲了哪几个概念
2. 每个概念用一句话解释

文档内容：
{file_content}
""",
    expected_output="列出文档中的概念及其解释",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()

print("\n" + "="*50)
print("分析结果：")
print("="*50)
print(result)

# ============================================================
# 4. 保存结果到文件
# ============================================================
with open("summary.txt", 'w', encoding='utf-8') as f:
    f.write(str(result))
print("\n✅ 结果已保存到 summary.txt")