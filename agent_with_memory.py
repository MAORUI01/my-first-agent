import os
import json

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-deepseek-api-key")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

from crewai import Agent, Task, Crew

class LongMemoryAgent:
    def __init__(self, memory_file="memory.json"):
        self.role = "智能助手"
        self.goal = "记住对话历史，连贯地回答用户问题"
        self.backstory = "你是一个有长期记忆的助手，能记住用户说过的话"
        self.memory_file = memory_file
        self.memory = self.load_memory()
        print(f"📂 加载了 {len(self.memory)} 条历史记忆")
        
    def load_memory(self):
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def add_to_memory(self, user_input, agent_response):
        self.memory.append({
            "user": user_input,
            "agent": str(agent_response)
        })
        self.save_memory()
        print(f"💾 已记住：{user_input}")
    
    def get_memory_context(self):
        if not self.memory:
            return ""
        context = "【对话历史】\n"
        for i, item in enumerate(self.memory[-10:], 1):
            context += f"{i}. 用户: {item['user']}\n"
            context += f"   助手: {item['agent']}\n"
        return context
    
    def respond(self, question):
        memory_context = self.get_memory_context()
        
        agent = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True
        )
        
        task = Task(
            description=f"""
{memory_context}

【当前问题】
{question}

请根据对话历史理解上下文，回答用户问题。
""",
            expected_output="友好的回答",
            agent=agent
        )
        
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        
        self.add_to_memory(question, result)
        return result

# 创建助手
assistant = LongMemoryAgent()

print("\n" + "="*50)
print("🧠 带长期记忆的 Agent 已启动")
print("="*50)
print("输入 'quit' 退出\n")

while True:
    q = input("你：")
    if q.lower() in ['quit', 'q', 'exit']:
        print("再见！")
        break
    
    answer = assistant.respond(q)
    print(f"助手：{answer}\n")