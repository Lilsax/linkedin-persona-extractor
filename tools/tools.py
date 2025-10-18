from langchain_tavily import TavilySearch


def get_profile_linkedin(name: str):
    """Search for a LinkedIn profile URL for the given name."""

    search = TavilySearch()
    # Bias the query toward LinkedIn profiles
    res = search.run(f"site:linkedin.com/in {name}")
    return res


if __name__ == "__main__":
    pass
