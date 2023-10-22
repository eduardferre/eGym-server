import os

# Remove the existing formatted_report.txt file if it exists
if os.path.exists("formatted_report.txt"):
    os.remove("formatted_report.txt")

if os.path.exists("table_report.txt"):
    os.remove("table_report.txt")

if os.path.exists("report.html"):
    os.remove("report.html")

# Read the report from a file (or you can modify this to read from any source)
with open("report_logs.txt", "r") as file:
    lines = file.readlines()

prev_lines = list()
report_lines = list()
post_lines = list()
flag = True

for count, line in enumerate(lines):
    if count < 8:
        prev_lines.append(line)
    elif not "[100%]" in lines[count - 1] and flag == True:
        report_lines.append(line)
    else:
        post_lines.append(line)
        flag = False

# Calculate the maximum row length
max_length = max(len(line) for line in report_lines)


# Function to format each line
def format_line(line):
    # Find the index of '%'
    percent_index = line.find("[")

    # Calculate the number of spaces needed between checkbox and '[ XX%]'
    spaces_needed = max_length - len(line)

    # Format the line with extra spaces
    formatted_line = line[:percent_index] + " " * spaces_needed + line[percent_index:]
    return formatted_line


# Format all lines
formatted_lines = [format_line(line) for line in lines]

# Write the formatted content to a new file
with open("formatted_report.txt", "w") as output_file:
    for count, line in enumerate(formatted_lines):
        if count < 8:
            output_file.write(prev_lines[count])
        elif not "[100%]" in formatted_lines[count - 1]:
            output_file.write(line)
        else:
            break

    for line in post_lines:
        output_file.write(line)

with open("table_report.txt", "w") as output_table_file:
    for count, line in enumerate(formatted_lines):
        if count < 8:
            None
        elif not "[100%]" in formatted_lines[count - 1]:
            output_table_file.write(line)
        else:
            break

with open("formatted_report.txt", "w") as output_file:
    for count, line in enumerate(formatted_lines):
        if count < 8:
            output_file.write(prev_lines[count])
        elif not "[100%]" in formatted_lines[count - 1]:
            output_file.write(line)
        else:
            break

    for line in post_lines:
        output_file.write(line)

with open("formatted_report.txt", "r") as file:
    text = file.read()

    html_text = "<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>\n<link rel='stylesheet' href='style.css' type='text/css'>\n</head>\n<body class='pyfile'>\n"

    for line in text.split("\n"):
        html_text += f"<p>{line}</p>\n"

    html_text += "</body>\n</html>"

with open("report.html", "w") as file:
    file.write(html_text)
