from typing import List
from tavily import TavilyClient
from config import Config


class TavilyContent:
    def __init__(self, topic, url, title, banner, banner_alt, favicon, raw_content):
        self.topic = topic
        self.url = url
        self.title = title
        self.banner = banner
        self.banner_alt = banner_alt
        self.favicon = favicon
        self.raw_content = raw_content


class Tavily:
    def __init__(self):
        self.client = TavilyClient(api_key=Config.tavily_api_key)
        self.max_results = int(Config.content_per_topic)

    def find(self, topic, max_results=None) -> List[TavilyContent]:
        if max_results is None:
            max_results = self.max_results

        print(f"Finding content for topic: {topic}")
        try:
            response = self.client.search(query=topic, search_depth="advanced", include_images=True, include_raw_content='text',
                                          include_image_descriptions=True, include_favicon=True, max_results=max_results)
            images = response['images'] if 'images' in response else []

            content_results: List[TavilyContent] = []
            for index, result in enumerate(response["results"]):
                image = images[index] if index < len(images) else None
                content_item = TavilyContent(
                    topic=topic,
                    url=result.get("url"),
                    title=result.get("title"),
                    banner=image.get('url') if image else None,
                    banner_alt=image.get('description') if image else None,
                    favicon=result.get("favicon"),
                    raw_content=result.get("raw_content")
                )
                content_results.append(content_item)
            return content_results
        except Exception as e:
            print(f"Error finding content for {topic}: {e}")
            return []
