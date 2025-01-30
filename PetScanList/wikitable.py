import time

# Define labels and formats for table headers
head_labels = {
    "title": "العنوان",
    "touched": "آخر تعديل",
    "q": "معرف ويكي بيانات",
    "Q": "معرف ويكي بيانات",
    "namespace": "النطاق",
    "ns": "النطاق",
    "len": "الحجم",
    "image": "صورة",
    "disambiguation": "صفحة توضيح؟",
}

head_formats = {
    "image": "[[File:{}|50px]]",
    "title": "[[{}]]",
    "q": "{{{{Q|{}}}}}",
    "Q": "{{{{Q|{}}}}}",
    "ns": "{}",
    "len": "{}",
}


def format_timestamp(timestamp):
    """Format a timestamp from 'YYYYMMDDHHMMSS' to 'YYYY-MM-DD HH:MM:SS'."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(timestamp, "%Y%m%d%H%M%S"))


def generate_table_header(table_head):
    """Generate the table header row based on the provided headers."""
    header_row = "\n".join(f"! {head_labels.get(x, x)}" for x in table_head)
    return header_row


def generate_table_row(row_data, table_head, row_number):
    """Generate a single row of the table."""
    row = []
    # ---
    data2 = {x: str(v) for x, v in row_data.items()}
    # ---
    if "metadata" in row_data:
        for x, v in row_data["metadata"].items():
            data2[x] = str(v)
    # ---
    for x in table_head:
        if x == "#":
            formatted_x = str(row_number)
        elif x == "touched":
            formatted_x = format_timestamp(data2.get(x, ""))
        else:
            formatted_x = head_formats.get(x, "{}").format(data2.get(x, "")) if data2.get(x, "") else ""
        row.append(formatted_x)
    return "! " + "\n| ".join(row)


def wiki_table(tab):
    """Generate a wikitable from the provided data."""
    table_head2 = ["#"]
    table_head = []
    rows = []

    for row_number, data in enumerate(tab.values(), start=1):
        if not table_head:
            table_head = table_head2 + list(data.keys())
            if "metadata" in data:
                table_head.extend(list(data["metadata"].keys()))
                table_head.remove("metadata")

        row = generate_table_row(data, table_head, row_number)
        rows.append(row)

    # Generate the full table
    table = '{| class="wikitable sortable"\n|-\n' + f"{generate_table_header(table_head)}\n|-\n" + "\n|-\n".join(rows) + "\n|}"

    return table


if __name__ == "__main__":
    tab = {
        "Q44835215": {
            "id": 46019515,
            "len": 9167,
            "n": "page",
            "namespace": 0,
            "nstext": "",
            "title": "Q44835215",
            "touched": "20240314021723",
        },
    }

    print(wiki_table(tab))
