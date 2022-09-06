from typing import List

from javscraper import JAVLibrary as BaseJAVLibrary


class JAVLibrary(BaseJAVLibrary):
    def search(self, query: str, *, code: str = None) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :param code: Code for closest match if not in query
        :return: List of found URLs
        """
        # Build URL
        path = self._build_search_path(query)
        if self.debug:
            print(f"Path: {path}")

        # Make request
        return self._make_normal_search(path)
