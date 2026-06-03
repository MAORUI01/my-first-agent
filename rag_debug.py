import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-deepseek-api-key")
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "deepseek-chat"

# 读取知识库
with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

print("=== 文件内容前500字符 ===")
print(full_text[:500])
print("=== 结束 ===\n")

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

print(f"共有 {len(chunks)} 个段落")
for i, chunk in enumerate(chunks):
    print(f"\n段落 {i+1}: {chunk[:80]}...")

# 检查关键词
print("\n=== 关键词检查 ===")
for kw in ["RAG", "Agent", "机器学习"]:
    found = kw in full_text
    print(f"{kw}: {'✅ 找到' if found else '❌ 未找到'}")