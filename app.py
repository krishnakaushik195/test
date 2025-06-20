from openai import OpenAI
import os
from pathlib import Path
import re

# === Step 1: Setup OpenAI Client (NVIDIA endpoint) ===
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# === Step 2: System Prompt (backend instructions) ===
system_prompt = (
    "You are a senior frontend web developer AI. Generate a complete standalone HTML5 website as a single file. "
    "Include HTML structure, CSS inside <style> in the <head>, and JavaScript inside <script> at the end. "
    "Use a clean, modern layout with a dark theme. The site must be fully responsive. "
    "It should simulate a multi-page experience with smooth-scroll or JS navigation — no external links. "
    "Include 5 to 10 sections: Home, About, Skills, Projects, Contact, Testimonials, etc. "
    "Add JavaScript interactivity: menu toggle, scroll animations, form validation, etc. "
    "Return only the full HTML code, starting from <!DOCTYPE html> and ending with </html>. No markdown, no explanations."
)

# === Step 3: User Prompt (short request) ===
user_prompt = "Create a full-stack developer's personal website named Krishna with all necessary sections."

# === Step 4: Folder to Save Output ===
output_folder = "advanced_website"
os.makedirs(output_folder, exist_ok=True)
file_path = Path(output_folder) / "index.html"

# === Step 5: Start Streaming the Response ===
stream = client.chat.completions.create(
    model="deepseek-ai/deepseek-r1-0528",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7,
    top_p=0.9,
    max_tokens=10000,
    stream=True
)

# === Step 6: Collect the Output ===
raw_output = ""
print("\n📤 Generating advanced responsive multi-section site...\n")

for chunk in stream:
    delta = chunk.choices[0].delta
    content = getattr(delta, "content", None)
    if content:
        print(content, end="")  # live feedback
        raw_output += content

# === Step 7: Extract ONLY the HTML (no markdown/extra) ===
match = re.search(r"(<!DOCTYPE html.*?</html>)", raw_output, re.DOTALL | re.IGNORECASE)
clean_html = match.group(1).strip() if match else raw_output.strip()

# === Step 8: Save as index.html ===
with open(file_path, "w", encoding="utf-8") as f:
    f.write(clean_html)

print(f"\n✅ Website saved at: {file_path}")
