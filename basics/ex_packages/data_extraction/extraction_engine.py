import json

# this style of import makes nonjava_extraction is available without it's package prefix
from html_extraction import nonjava_extraction

# this style must reference java_extraction with its full name
# import html_extraction.java_extraction

from data_handling import *


url = "https://docs.python.org/3/tutorial/modules.html#tut-packages"

payload = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = nonjava_extraction.make_request("GET", url, headers=headers, data=payload)

if response:
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        # Find the main content area - typically in a div with class 'body' or similar
        main_content = parse_content.get_html_content(response, parser='html.parser')
        topics = []
        if main_content:
            # Find all section headers - they're typically h1, h2, h3 with ids
            headers = html_tags_handler.get_headers(main_content, header_tags=['h1', 'h2', 'h3', 'h4'])
            for header in headers:
                # Get the text content of the header
                title = header.get_text().strip()
                # title = header.get_text().strip()

                # Find the link - either the header has an id or it contains an <a> tag
                link = header.find('a')
                if link and link.get('href'):
                    # Handle relative URLs
                    href = link.get('href')
                    if href.startswith('#'):
                        full_url = f"{url.split('#')[0]}{href}"
                    else:
                        full_url = href
                elif header.get('id'):
                    # Use the header's id to create anchor link
                    full_url = f"{url.split('#')[0]}#{header.get('id')}"
                else:
                    continue  # Skip if no link can be found

                # Clean up the title (remove link symbols, extra spaces)
                title = title.replace('¶', '').strip()

                if title and full_url:
                    topics.append({
                        "Topic": title,
                        "URL": full_url
                    })

        # Print the results
        print(f"\nFound {len(topics)} topics:")
        print(json.dumps(topics, indent=2))

        # Alternative: Print in a more readable format
        print("\n" + "= " *50)
        print("TOPICS LIST:")
        print("= " * 50)
        for topic in topics:
            print(f"Topic: {topic['Topic']}")
            print(f"URL: {topic['URL']}")
            print("-" * 30)
else:
    print(f"Failed to fetch the page.")
