"""
"""
head_labels = {
    "title": "العنوان",
    "touched": "آخر تعديل",
    "Q": "معرف ويكي بيانات",
    "ns": "النطاق",
    "len": "الحجم",
}

head_formats = {
    "title": "[[{}]]",
    "touched": "{{{{#time:j M Y (H:i)|{}}}}}",
    "Q": "{{{{Q|{}}}}}",
    "ns": "{}",
    "len": "{}",
}


def wiki_table(tab):
    # ---
    table_head = ["title"]
    # ---
    rows = []
    # ---
    for row, data in tab.items():
        # print(data)
        # {'touched': '20230327144419', 'Q': 'Q6853789', 'ns': 0, 'len': 3393, 'title': 'محمد حسين هيثم'}
        # ---
        if table_head == ["title"]:
            table_head += [x for x in data.keys() if x != "title"]
        # ---
        # row = f"! [[{data.get('title')}]]"
        row = []
        # ---
        for x in table_head:
            formated_x = head_formats.get(x, "{}").format(data.get(x, ""))
            row.append(formated_x)
        # ---
        row = "! " + "\n| ".join(row)
        # ---
        rows.append(row)
    # ---
    text = '{| class="wikitable sortable"\n|-'
    # ---
    # text += "\n! title"
    # ---
    for x in table_head:
        ar_x = head_labels.get(x, x)
        text += f"\n! {ar_x}"
    # ---
    text += "\n|-\n"
    # ---
    text += "\n|-\n".join(rows)
    text += "\n|}"
    # ---
    # print(text)
    # ---
    return text
