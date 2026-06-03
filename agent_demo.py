import os

# ============================================================
# 1. 配置 DeepSeek API（通过环境变量）
# ============================================================
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-deepseek-api-key")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"  # ← 关键！通过环境变量指定模型

# ============================================================
# 2. 导入依赖
# ============================================================
from crewai import Agent, Task, Crew

# ============================================================
# 3. 创建 Agent（不需要再写 llm_config）
# ============================================================
agent = Agent(
    role="Python专家",
    goal="用简单易懂的方式解释Python概念",
    backstory="你是一个有10年经验的Python开发者，擅长把复杂的技术概念讲得生动有趣。",
    verbose=True
)

# ============================================================
# 4. 创建任务
# ============================================================
task = Task(
    description="人饿了为什么要睡觉" ,
    expected_output="一句简洁、准确、易懂的解释",
    agent=agent
)

# ============================================================
# 5. 创建 Crew 并执行
# ============================================================
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

print("\n" + "="*50)
print("开始执行任务...")
print("="*50)

result = crew.kickoff()

print("\n" + "="*50)
print("最终结果：")
print("="*50)
print(result)