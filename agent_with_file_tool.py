import os
import os
import sys
import locale

# ============================================================
# 修复中文编码问题
# ============================================================
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["LANG"] = "zh_CN.UTF-8"
os.environ["LC_ALL"] = "zh_CN.UTF-8"

# 设置默认编码
try:
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
except:
    pass

# 重新加载 sys 模块的编码
if hasattr(sys, 'setdefaultencoding'):
    reload(sys)
    sys.setdefaultencoding('utf-8')

# ============================================================
# 配置 DeepSeek API
# ============================================================
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-deepseek-api-key")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew
from crewai.tools import tool

# ... 后面的代码不变 ...
os.environ["OPENAI_API_KEY"] = "你的DeepSeek Key"
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew
from crewai.tools import tool

# ============================================================
# 自定义文件读取工具
# ============================================================
@tool("ReadFileTool")
def read_file(file_path: str) -> str:
    """
    读取文件内容。
    参数: file_path - 文件的完整路径或相对路径
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"错误：找不到文件 {file_path}"
    except Exception as e:
        return f"读取文件出错: {str(e)}"

# ============================================================
# 自定义文件写入工具
# ============================================================
@tool("WriteFileTool")
def write_file(content: str, file_path: str = "output.txt") -> str:
    """
    将内容写入文件。
    参数: 
    - content: 要写入的内容
    - file_path: 文件保存路径（默认 output.txt）
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"成功写入文件: {file_path}"
    except Exception as e:
        return f"写入文件出错: {str(e)}"

# ============================================================
# 创建 Agent，拥有文件读写工具
# ============================================================
file_agent = Agent(
    role="文档助手",
    goal="读取、分析并处理文件内容",
    backstory="""你是一个擅长处理文档的助手。
    你可以读取文件内容、分析内容、总结信息，
    并且可以把处理结果保存到新文件中。""",
    verbose=True,
    tools=[read_file, write_file]
)

# ============================================================
# 任务：读取文件并回答
# ============================================================
task = Task(
    description="""请完成以下任务：
    1. 读取 knowledge.txt 文件的内容
    2. 总结文件里讲了哪几个概念
    3. 把总结结果保存到 summary.txt 文件中
    """,
    expected_output="""一个总结，列出文件中提到的概念，
    以及确认文件已保存的消息""",
    agent=file_agent
)

crew = Crew(agents=[file_agent], tasks=[task])
result = crew.kickoff()

print("\n" + "="*50)
print("执行结果：")
print("="*50)
print(result)