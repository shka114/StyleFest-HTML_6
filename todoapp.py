import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []
    
    def save_todos(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def add_todo(self, title, priority="medium"):
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "completed": False,
            "priority": priority,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.todos.append(todo)
        self.save_todos()
        return f"✅ Todo added: {title}"
    
    def view_todos(self):
        if not self.todos:
            return "📭 No todos yet!"
        
        output = "\n" + "="*60 + "\n"
        output += "📋 YOUR TODOS\n"
        output += "="*60 + "\n"
        
        for todo in self.todos:
            status = "✓" if todo["completed"] else "○"
            priority_emoji = "🔴" if todo["priority"] == "high" else "🟡" if todo["priority"] == "medium" else "🟢"
            output += f"{status} [{todo['id']}] {todo['title']} {priority_emoji}\n"
        
        output += "="*60 + "\n"
        return output
    
    def mark_complete(self, todo_id):
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                self.save_todos()
                return f"✓ Marked as complete: {todo['title']}"
        return f"❌ Todo #{todo_id} not found"
    
    def delete_todo(self, todo_id):
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                title = todo["title"]
                self.todos.pop(i)
                self.save_todos()
                return f"🗑️  Deleted: {title}"
        return f"❌ Todo #{todo_id} not found"
    
    def search_todos(self, keyword):
        results = [t for t in self.todos if keyword.lower() in t["title"].lower()]
        if not results:
            return f"🔍 No todos found with '{keyword}'"
        
        output = f"\n🔍 Search results for '{keyword}':\n"
        for todo in results:
            status = "✓" if todo["completed"] else "○"
            output += f"{status} [{todo['id']}] {todo['title']}\n"
        return output
    
    def get_stats(self):
        total = len(self.todos)
        completed = sum(1 for t in self.todos if t["completed"])
        pending = total - completed
        
        return f"""
📊 STATS
--------
Total: {total}
Completed: {completed}
Pending: {pending}
"""
    
    def menu(self):
        while True:
            print("\n" + "="*60)
            print("🎯 TODO APP - MENU".center(60))
            print("="*60)
            print("1. View all todos")
            print("2. Add new todo")
            print("3. Mark as complete")
            print("4. Delete todo")
            print("5. Search todos")
            print("6. View stats")
            print("7. Exit")
            print("="*60)
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                print(self.view_todos())
            
            elif choice == "2":
                title = input("Enter todo title: ").strip()
                priority = input("Priority (high/medium/low): ").strip().lower()
                if priority not in ["high", "medium", "low"]:
                    priority = "medium"
                print(self.add_todo(title, priority))
            
            elif choice == "3":
                print(self.view_todos())
                try:
                    todo_id = int(input("Enter todo ID to mark complete: "))
                    print(self.mark_complete(todo_id))
                except ValueError:
                    print("❌ Invalid ID")
            
            elif choice == "4":
                print(self.view_todos())
                try:
                    todo_id = int(input("Enter todo ID to delete: "))
                    print(self.delete_todo(todo_id))
                except ValueError:
                    print("❌ Invalid ID")
            
            elif choice == "5":
                keyword = input("Search keyword: ").strip()
                print(self.search_todos(keyword))
            
            elif choice == "6":
                print(self.get_stats())
            
            elif choice == "7":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice!")

if __name__ == "__main__":
    app = TodoApp()
    app.menu()