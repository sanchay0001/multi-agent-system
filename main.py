 # main.py

import os
from agents.classifier_agent import ClassifierAgent
from memory.shared_memory import SharedMemory

def list_input_files():
    input_dir = "inputs"
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    print("\nAvailable input files:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    return files

def main():
    print("🔁 Initializing Multi-Agent AI System...")
    memory = SharedMemory()
    classifier = ClassifierAgent(memory)

    files = list_input_files()
    choice = input("\nEnter file number to process: ")

    try:
        selected_file = files[int(choice) - 1]
        file_path = os.path.join("inputs", selected_file)
        print(f"\n🚀 Processing: {selected_file}")
        classifier.route(file_path)
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n📜 Memory Log:")
    for row in memory.fetch_all():
        print(row)

    memory.close()

if __name__ == "__main__":
    main()

