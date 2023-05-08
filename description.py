import json
import re
from http import client
from urllib import parse

exp = r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)"


def find_urls(text):
    return re.findall(exp, text)


def unshorten_url(url):
    try:
        parsed = parse.urlparse(url)
        h = client.HTTPConnection(parsed.netloc, timeout=10)
        resource = parsed.path

        if parsed.query != "":
            resource += "?" + parsed.query
        if parsed.netloc == "":
            return None

        h.request('HEAD', resource)
        response = h.getresponse()

        if response.status//100 == 3 and response.getheader('Location') != url:
            return unshorten_url(response.getheader('Location'))
        else:
            return url
    except:
        return None


def get_description_parsed_urls(description):
    urls = find_urls(description)
    t_urls = [unshorten_url(url) for url in urls]
    parsed_urls = [
        {
            "url": url,
            "parsed": parse.urlparse(url)
        }
        for url in t_urls if url is not None
    ]

    return parsed_urls


def save_description_parsed_urls(description, out_path):
    parsed_urls = get_description_parsed_urls(description)
    with open(out_path, "w") as file:
        json.dump(parsed_urls, file, indent=4)
