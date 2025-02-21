# List to store valid wiki URLs
valid_wikis = []

# Dictionary of valid projects and their respective languages
valid_projects = {
    "wikipedia": ["ar"],
    "wikisource": ["ar"],
}

# Construct valid wiki URLs and append to the list
for project, languages in valid_projects.items():
    for language in languages:
        valid_wikis.append(f"{language}.{project}.org")

# Optionally print the list of valid wikis
if __name__ == "__main__":
    print(valid_wikis)
