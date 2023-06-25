import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langchain import GoogleSearchAPIWrapper


def get_random_user_agent():
    return UserAgent().random


class WebPagePassageExtractor:
    def __init__(
        self,
        claims: list[str],
        max_input_chars: int = 50000,
        max_tokens_to_sample: int = 1000,
    ):
        self.claims = claims
        self.max_input_chars = max_input_chars
        self.max_tokens_to_sample = max_tokens_to_sample

    def run(self, url: str):
        if url.endswith(".pdf"):
            return "Sorry, I can't extract passages from PDFs yet."
        response = requests.get(url, headers={"User-Agent": get_random_user_agent()})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        page = soup.get_text()[: self.max_input_chars]
        claims_section = "\n".join(self.claims)
        prompt = f"""
I am attempting to find sources that either support or contradict the following claims: {claims_section}
Here is a web page that I found:
<page>
{page}
</page>

Please extract up to 5 direct quotes from the page that either support or contradict the claim. If there are no such quotes, please respond "None".
"""
        model = ChatAnthropic(max_tokens_to_sample=self.max_tokens_to_sample)
        return model.call_as_llm(prompt)


class GoogleSearchAPIWrapperWithLinks(GoogleSearchAPIWrapper):
    """Wrapper for Google Search API that returns
    snippets and their links, nicely formatted."""

    def run(self, query: str) -> str:
        """Run query through GoogleSearch and
        parse result with snippets and their links."""
        formatted_results = []
        results = self._google_search_results(query, num=self.k)
        if len(results) == 0:
            return "No good Google Search Result was found"

        for result in results:
            formatted_result = f"{result.get('title', 'No title')}\n"
            if "snippet" in result:
                formatted_result += f"{result['snippet']}\n"
            if "link" in result:
                formatted_result += f"Link: {result['link']}\n"
            formatted_results.append(formatted_result)

        return "\n".join(formatted_results)
