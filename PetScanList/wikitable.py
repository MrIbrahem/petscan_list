import time

# Define labels and formats for table headers
head_labels = {
    "title": "العنوان",
    "touched": "آخر تعديل",
    "Q": "معرف ويكي بيانات",
    "ns": "النطاق",
    "len": "الحجم",
}

head_formats = {
    "title": "[[{}]]",
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
    for x in table_head:
        if x == "#":
            formatted_x = str(row_number)
        elif x == "touched":
            formatted_x = format_timestamp(row_data.get(x, ""))
        else:
            formatted_x = head_formats.get(x, "{}").format(row_data.get(x, ""))
        row.append(formatted_x)
    return "! " + "\n| ".join(row)


def wiki_table(tab):
    """Generate a wikitable from the provided data."""
    table_head2 = ["#", "title"]
    table_head = []
    rows = []

    for row_number, data in enumerate(tab.values(), start=1):
        if not table_head:
            table_head = table_head2 + [x for x in data.keys() if x not in table_head2]

        row = generate_table_row(data, table_head, row_number)
        rows.append(row)

    # Generate the full table
    table = '{| class="wikitable sortable"\n|-\n' + f"{generate_table_header(table_head)}\n|-\n" + "\n|-\n".join(rows) + "\n|}"

    return table
