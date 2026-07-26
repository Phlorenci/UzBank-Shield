# Extracts URL components
from urllib.parse import urlparse

def extract_url_components(url):
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    return {
        "original_url": url,
        "protocol": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
    }