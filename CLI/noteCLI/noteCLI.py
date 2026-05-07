import argparse
import json
import os

def main():
    if not os.path.exists("json/note.json"):
        data = []
    else:
        with open("json/note.json", "r") as f:
            data = json.load(f)
    
    parser = argparse.ArgumentParser(description="Create a note")
    subparser = parser.add_subparsers(dest="choice", help="Commands", required=True)

    add_p = subparser.add_parser("add", help="Add a new note")
    add_p.add_argument("title", help="Note title")
    add_p.add_argument("description", help="Note description")

    upd_p = subparser.add_parser("update", help="Update a note")
    upd_p.add_argument("title", help="Note title")
    upd_p.add_argument("description", help="Note description")

    del_p = subparser.add_parser("delete", help="Delete a note")
    del_p.add_argument("title", help="Note title")

    list_p = subparser.add_parser("list", help="List of notes")

    args = parser.parse_args()

    if args.choice == "add":
        add(args, data)
    elif args.choice == "update":
        update(args, data)
    elif args.choice == "delete": 
        data = delete(args, data)
    elif args.choice =="list":
        note_list(args, data)
    with open("json/note.json", "w") as f:
        json.dump(data, f, indent=2)

def add(args, data):
    found = False
    for item in data:
        if item["title"] == args.title:
            found = True
    if not found:
        data.append({"title": args.title, "description": args.description})
        print("Note added")  
    else:
        print("Title is used")
def update(args, data):
    for item in data:
        if item["title"] == args.title:
            item["description"] = args.description
            print("Note updated")
            break
    else:
        print("Note not found")
def delete(args, data):
    new_data = []
    found = False
    for item in data:
        if item["title"] != args.title:
            new_data.append(item)
        else:
            found = True
    if found:
        print("Note deleted")
        data = new_data
    else:
        print("Note not found")
    return data
def note_list(args, data):
    if data:
        for item in data:
            print(f"{item['title']} : {item['description']}")
    else:
        print("No Notes found")
    

if __name__ == "__main__":
    main()