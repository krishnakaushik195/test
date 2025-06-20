from openai import OpenAI
import os
from pathlib import Path

# Setup NVIDIA-compatible OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# === Backend System Prompt (LONG) ===
system_prompt = (
    "You are a senior frontend developer AI. Your job is to generate a complete standalone HTML5 website. "
    "The entire website must be written in one single file using only valid HTML5. "
    "All CSS must be placed inside <style> tags in the <head>. "
    "All JavaScript must be placed at the bottom inside <script> tags. "
    "Use a clean layout, modern fonts, responsive design, and dark theme by default. "
    "You must not return multiple files or markdown formatting — just raw code of a complete <html> document. "
    "The HTML must start with <!DOCTYPE html> and end with </html>. "
    "Do not include explanations. Return only code."
)

# === User Prompt (Short + Flexible) ===
user_prompt = "Portfolio website for a UI/UX designer"

# === Output folder ===
folder_name = "single_file_output"
os.makedirs(folder_name, exist_ok=True)
file_path = Path(folder_name) / "index.html"

# === Streaming request ===
stream = client.chat.completions.create(
    model="deepseek-ai/deepseek-r1-0528",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.6,
    top_p=0.7,
    max_tokens=4096,
    stream=True
)

# === Collect full HTML output ===
html_code = ""

print("\n📤 Receiving generated website...\n")

for chunk in stream:
    delta = chunk.choices[0].delta
    content = getattr(delta, "content", None)
    if content:
        print(content, end="")  # Live stream to console
        html_code += content

# === Save to index.html ===
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_code.strip())

print(f"\n✅ Website saved as: {file_path}")
print("\n🌐 Open the file in your browser to view the generated website.")
