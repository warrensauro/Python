from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

base_url = "https://quotes.toscrape.com/"
current_url = base_url

datas = []

while current_url:
    page = requests.get(current_url)
    page.raise_for_status()

    soup = BeautifulSoup(page.text, "html.parser")
    divs = soup.find_all("div", class_="quote")

    pairs = [
        {
            "Quote": div.find("span", class_="text").get_text(),
            "Author": div.find("small", class_="author").get_text(),
            "Tags": [tag.get_text(strip=True) for tag in div.find_all("a", class_="tag")]
        }
        for div in divs
    ]

    datas.extend(pairs)

    next_li = soup.find("li", class_="next")
    if next_li:
        next_page = next_li.find("a").get("href")
        current_url = base_url + next_page
    else:
        current_url = None
        break


df = pd.DataFrame(datas)
conn = sqlite3.connect("quotes.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS quotes")
cursor.execute("DROP TABLE IF EXISTS authors")
cursor.execute("DROP TABLE IF EXISTS tags")
cursor.execute("DROP TABLE IF EXISTS quote_tags")
#Authors Table
unique_author = df["Author"].unique()
cursor.execute("""CREATE TABLE IF NOT EXISTS
               authors(author_id INTEGER PRIMARY KEY AUTOINCREMENT, author_name TEXT UNIQUE)""")

with conn:
    cursor.executemany("Insert or IGNORE into authors (author_name) Values (?)", ((author, ) for author in unique_author))
conn.commit()
#Quotes Table
cursor.execute("""CREATE TABLE IF NOT EXISTS quotes(
               quote_id INTEGER PRIMARY KEY AUTOINCREMENT, 
               quote_text TEXT UNIQUE, 
               author_id INTEGER,
               FOREIGN KEY(author_id) REFERENCES authors(author_id))""")
for _, row in df.iterrows():
    cursor.execute("Select author_id FROM authors where author_name = ?",
                   (row["Author"],))
    author_id = cursor.fetchone()[0]

    with conn:
        cursor.execute("INSERT OR IGNORE INTO quotes (quote_text, author_id) VALUES (?,?)",
                       (row["Quote"], author_id))
conn.commit()
#Tags Table
tag_explode = df.explode("Tags")
unique_tag = tag_explode["Tags"].unique()
cursor.execute("""CREATE TABLE IF NOT EXISTS tags(
               tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
               tag_name TEXT UNIQUE)""")
with conn:
    cursor.executemany("INSERT OR IGNORE into tags (tag_name) Values (?)", ((tag, ) for tag in unique_tag if tag))
conn.commit()
#Quote_Tag Table
cursor.execute("""CREATE TABLE IF NOT EXISTS quote_tags(
               quote_id INTEGER,
               tag_id INTEGER,
               FOREIGN KEY(quote_id) REFERENCES quotes(quote_id),
               FOREIGN KEY(tag_id) REFERENCES tags(tag_id),
               PRIMARY KEY(quote_id, tag_id))""")
for _, row in tag_explode.iterrows():
    if pd.isna(row["Tags"]):
        continue

    cursor.execute("Select quote_id FROM quotes where quote_text = ?",
                   (row["Quote"],))
    quote_id = cursor.fetchone()[0]
    cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (row["Tags"],))
    res = cursor.fetchone()
    if res:
        tag_id = res[0]
        with conn:
            cursor.execute("INSERT OR IGNORE INTO quote_tags (quote_id, tag_id) VALUES (?, ?)",
                           (quote_id, tag_id))
conn.commit()

#Test: Find all tags for a given author
author_name = "Albert Einstein"
query = cursor.execute("""
    SELECT DISTINCT t.tag_name
    FROM tags t
    JOIN quote_tags qt ON t.tag_id = qt.tag_id
    JOIN quotes q ON qt.quote_id = q.quote_id
    JOIN authors a ON q.author_id = a.author_id
    WHERE a.author_name = ?;
""", (author_name,))

results = query.fetchall()
tags = [row[0] for row in results]
print(tags)

#Test: Find all quotes for a given tag
tag_name = "life"
query = cursor.execute("""
    SELECT q.quote_text, a.author_name
    FROM quotes q
    JOIN authors a ON q.author_id = a.author_id
    JOIN quote_tags qt ON q.quote_id = qt.quote_id
    JOIN tags t ON qt.tag_id = t.tag_id
    WHERE t.tag_name = ?;
""", (tag_name,))
results = query.fetchall()
for quote, author in results:
    print(f"{author}: {quote}")


