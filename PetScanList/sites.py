valid_wikis = []

valid_projects = {
    "wikipedia": ["ar"],
    "wikisource": ["ar"],
}

for project, langs in valid_projects.items():
    for lang in langs:
        valid_wikis.append(f"{lang}.{project}.org")
