import os

os.environ["OPENAI_API_KEY"] = "sk-1e55ff17d380430e9ed6d26dfd09a7ed"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew

# ============================================================
# Agent 1：研究员（负责搜索资料）
# ============================================================
researcher = Agent(
    role="资深研究员",
    goal="查找并整理关于【人工智能】的最新信息",
    backstory="""你是一名顶尖科技公司的研究员，
    擅长快速查找资料并提炼关键信息。
    你的输出要条理清晰，便于后续写作使用。""",
    verbose=True,
    allow_code_execution=False
)

# ============================================================
# Agent 2：写手（负责写文章）
# ============================================================
writer = Agent(
    role="科技撰稿人",
    goal="根据研究资料写出通俗易懂的文章",
    backstory="""你是一名资深科技记者，
    擅长把复杂的技术概念写得像故事一样有趣。
    你写的文章让普通人都能看懂。""",
    verbose=True,
    allow_code_execution=False
)

# ============================================================
# Agent 3：编辑（负责润色和校对）
# ============================================================
editor = Agent(
    role="资深编辑",
    goal="审核并润色文章，确保质量",
    backstory="""你是一家知名科技媒体的主编，
    有10年编辑经验，擅长发现文章中的问题，
    让文章更流畅、更专业。""",
    verbose=True,
    allow_code_execution=False
)

# ============================================================
# 任务 1：研究（研究员负责）
# ============================================================
research_task = Task(
    description="""请整理关于【人工智能的应用领域】的资料。
    
    要求：
    1. 列出3个主要的应用领域
    2. 每个领域用一句话说明
    3. 用条理清晰的格式输出
    """,
    expected_output="3个AI应用领域及其说明",
    agent=researcher
)

# ============================================================
# 任务 2：写作（写手负责，依赖研究结果）
# ============================================================
writing_task = Task(
    description="""根据以下研究资料，写一篇简短的文章。
    
    要求：
    1. 标题自拟
    2. 正文150字左右
    3. 语言通俗有趣
    """,
    expected_output="一篇150字左右的文章",
    agent=writer,
    context=[research_task]  # 依赖研究任务的结果
)

# ============================================================
# 任务 3：编辑（编辑负责，依赖文章初稿）
# ============================================================
editing_task = Task(
    description="""请对文章进行润色和校对。
    
    要求：
    1. 检查语法和表达
    2. 优化用词，让文章更生动
    3. 保持原意，不要大改
    """,
    expected_output="润色后的最终文章",
    agent=editor,
    context=[writing_task]  # 依赖写作任务的结果
)

# ============================================================
# 创建 Crew，按顺序执行
# ============================================================
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    verbose=True
)

print("\n" + "="*50)
print("🤖 多 Agent 团队开始工作...")
print("="*50)

result = crew.kickoff()

print("\n" + "="*50)
print("📝 最终文章：")
print("="*50)
print(result)