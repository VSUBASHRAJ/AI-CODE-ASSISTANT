import requests
import os

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct:free"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
}

def ask_openrouter(prompt):
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You're an AI agent that performs coding tasks on the local computer."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    return result['choices'][0]['message']['content']

def main():
    print("🧠 Masyo AI Agent for Local Task Execution\n")
    user_task = input("📝 What do you want me to do? (e.g., Create a Hello World script): ")

    print("\n🤖 Getting plan from AI...")
    plan = ask_openrouter(f"Given the task: '{user_task}', generate a step-by-step plan and the code needed to accomplish it.")
    print("\n📋 AI-Generated Plan:\n")
    print(plan)

    approve = input("\n✅ Approve this plan? (y/n): ").lower()
    if approve != 'y':
        print("❌ Task cancelled.")
        return

    print("\n🧾 Extracting code block...")
    import re
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", plan, re.DOTALL)

    if not code_blocks:
        print("⚠️ No code found in the response.")
        return

    code = code_blocks[0]
    filename = "masyo_task.py"
    with open(filename, "w") as f:
        f.write(code)
    print(f"\n📂 Code written to {filename}")

    print("\n⚙️ Running the script...\n")
    os.system(f"python {filename}")

    success = input("\n❓Was the output correct? (y/n): ").lower()
    if success != 'y':
        feedback = input("💬 What went wrong?: ")
        refined_plan = ask_openrouter(f"The previous code had this issue: {feedback}. Refine and fix it.")
        print("\n🔁 Updated Plan:\n", refined_plan)

        new_code = re.findall(r"```(?:python)?\n(.*?)```", refined_plan, re.DOTALL)
        if new_code:
            with open(filename, "w") as f:
                f.write(new_code[0])
            print("\n⚙️ Running the updated script...")
            os.system(f"python {filename}")
        else:
            print("⚠️ Still couldn't extract code from refinement.")
    else:
        print("✅ Task successfully completed!")

if __name__ == "__main__":
    main()
