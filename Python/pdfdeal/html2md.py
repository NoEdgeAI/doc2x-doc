from pdfdeal.file_tools import html_table_to_md

with open("old.md", "r") as f:
    html = f.read()
    md = html_table_to_md(html)
    with open("Output/new.md", "w") as f:
        f.write(md)
