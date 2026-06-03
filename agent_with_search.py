import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-deepseek-api-key")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew

# 使用内置的搜索功能（不需要额外导入）
from crewai.tools import tool

# 自定义一个搜索工具
@tool("WebSearch")
def web_search(query: str) -> str:
    """搜索网络信息"""
    import requests
    try:
        # 使用 DuckDuckGo 的免费搜索 API
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 提取结果
        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics"):
            for topic in data.get("RelatedTopics", []):
                if "Text" in topic:
                    return topic["Text"]
        return f"没有找到关于 '{query}' 的搜索结果"
    except Exception as e:
        return f"搜索出错: {str(e)}"

# 创建 Agent，使用自定义搜索工具
researcher = Agent(
    role="研究员",
    goal="搜索并获取最新、最准确的信息",
    backstory="你是一个擅长使用搜索引擎查找信息的专家",
    verbose=True,
    tools=[web_search]
)

task = Task(
    description="搜索一下最近关于DeepSeek大模型的最新消息",
    expected_output="列出3条AI领域的最新新闻，每条用一句话概括",
    agent=researcher
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
print("\n" + "="*50)
print("搜索结果：")
print(result)