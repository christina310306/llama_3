import os
from file_reader import read_file

# 🔹 CHANGE THIS if your OneDrive path is different
ONEDRIVE_PATH = r"C:\Users\chris\OneDrive"

def main():
    print("🔌 MCP Server started")

    if not os.path.exists(ONEDRIVE_PATH):
        print("❌ OneDrive path not found")
        return

    all_text = ""

    for root, _, files in os.walk(ONEDRIVE_PATH):
        for file in files:
            if file.lower().endswith((".pdf", ".docx")):
                file_path = os.path.join(root, file)

                print(f"📄 Reading: {file_path}")
                text = read_file(file_path)

                if text.strip():
                    print(f"✅ Collected {len(text)} characters")
                    all_text += "\n\n" + text
                else:
                    print("⚠️ No text extracted")

    print("\n📊 Finished scanning OneDrive")
    print(f"🧠 Total characters collected: {len(all_text)}")

    # Save collected text (optional but VERY useful)
    with open("reports/knowledge_base.txt", "w", encoding="utf-8") as f:
        f.write(all_text)

    print("💾 Knowledge base saved to reports/knowledge_base.txt")

if __name__ == "__main__":
    main()
