import os
from django.shortcuts import render
from django.http import HttpResponse
from stocks.screens.low_pe import low_pe
from stocks.screens.low_pb import low_pb
from .sip_data_dictionary import sip_data_dictionary

copy_to_clipboard_button = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Copy to Clipboard</title>
    <style>
        .copy-button {{
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }}
        .copy-button:hover {{
            background-color: #45a049;
        }}
        .copy-button.copied {{
            background-color: #007bff;
        }}
    </style>
</head>
<body>

<button class="copy-button" id="copyButton" onclick="copyToClipboard()">Copy Tickers to Clipboard</button>
{dataframe_html}

<script>
    function copyToClipboard() {{
        const textToCopy = `{ticker_list}`;
        navigator.clipboard.writeText(textToCopy).then(() => {{
            const copyButton = document.getElementById("copyButton");
            copyButton.textContent = "Copied!";
            copyButton.classList.add("copied");
            
            // Reset the button text after a few seconds
            setTimeout(() => {{
                copyButton.textContent = "Copy Tickers to Clipboard";
                copyButton.classList.remove("copied");
            }}, 2000);
        }}).catch(err => {{
            console.error("Failed to copy text: ", err);
        }});
    }}
</script>

</body>
</html>
"""


drop_down_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropdown Redirect Example</title>
    <script>
        function redirectToPage() {{
            // Get the select element
            var selectElement = document.getElementById("dropdown");
            // Get the selected value
            var selectedValue = selectElement.value;
            // Redirect to the new page
            if (selectedValue) {{
                window.open(selectedValue, '_blank');
            }}
        }}
    </script>
</head>
<body>

<label for="dropdown">Select an option:</label>
<select id="dropdown" onchange="redirectToPage()">
    <option value="">Select...</option>
    {screen_options}
</select>

</body>
</html>
"""


def screen_dropdown(request):
    # <option value="https://example.com/page1">Page 1</option>
    # <option value="https://example.com/page2">Page 2</option>
    # <option value="https://example.com/page3">Page 3</option>

    def list_files_in_directory(directory_path):
        list_of_screens = os.listdir(directory_path)
        list_of_screens.remove("__pycache__")
        list_of_screens.remove("utils.py")
        cleaned_names = [name.removesuffix(".py") for name in list_of_screens]
        return cleaned_names

    # directory_path = "screens"
    file_list = list_files_in_directory("./stocks/screens")

    options = "\n".join(
        f'<option value="screens/{name}">{name}</option>' for name in file_list
    )

    # return HttpResponse(",".join(file_list))
    return HttpResponse(drop_down_html.format(screen_options=options))


def low_pe_view(request):
    df = low_pe().rename(columns=sip_data_dictionary).head()
    df.index.name = None

    # Convert DataFrame to HTML
    dataframe_html = df.to_html()

    # Convert DataFrame to a string list for JavaScript
    ticker_list = ",".join(df.index)  # Assuming index contains tickers

    # Format HTML with DataFrame and ticker list
    html_content = copy_to_clipboard_button.format(
        dataframe_html=dataframe_html, ticker_list=ticker_list
    )

    return HttpResponse(html_content)


def low_pb_view(request):
    df = low_pb().rename(columns=sip_data_dictionary).head()
    df.index.name = None

    # Convert DataFrame to HTML
    dataframe_html = df.to_html()

    # Convert DataFrame to a string list for JavaScript
    ticker_list = ",".join(df.index)  # Assuming index contains tickers

    # Format HTML with DataFrame and ticker list
    html_content = copy_to_clipboard_button.format(
        dataframe_html=dataframe_html, ticker_list=ticker_list
    )

    return HttpResponse(html_content)
