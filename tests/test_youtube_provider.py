from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from paperclip_kratos.models import TopicConfig
from paperclip_kratos.providers.youtube import YouTubeDiscoveryProvider, YouTubeProviderError


class YouTubeDiscoveryProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = TopicConfig(
            topic="tema",
            audience="time",
            goal="objetivo",
            platforms=["instagram", "linkding", "article"],
            keywords=["keyword principal", "keyword secundario"],
            max_results=2,
        )

    def test_returns_placeholder_when_api_key_missing(self) -> None:
        provider = YouTubeDiscoveryProvider()
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("YOUTUBE_API_KEY", None)
            sources = provider.discover(self.config)

        self.assertEqual(2, len(sources))
        self.assertIn("YOUTUBE_API_KEY não configurada", sources[0].notes[0])
        self.assertTrue(sources[0].url.startswith("https://www.youtube.com/results?search_query="))

    def test_returns_placeholder_when_search_fails_with_api_key(self) -> None:
        provider = YouTubeDiscoveryProvider()
        with patch.dict(os.environ, {"YOUTUBE_API_KEY": "invalid-key"}, clear=False):
            with patch.object(
                provider,
                "_search",
                side_effect=YouTubeProviderError("HTTP 400: API key not valid."),
            ):
                sources = provider.discover(self.config)

        self.assertEqual(2, len(sources))
        self.assertIn("HTTP 400", sources[0].notes[0])
        self.assertTrue(any("NotebookLM" == use_case for use_case in sources[0].use_cases))


if __name__ == "__main__":
    unittest.main()
