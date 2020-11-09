# coding: utf8
"""Bootstrap for Komi Can't Communicate."""

import json
import pathlib
import re
from typing import Generator

from tankobon.base import GenericManga, Chapters
from tankobon.utils import get_soup


class Manga(GenericManga):

    IMGHOST = "blogspot.com"
    RE_TITLE = re.compile(r"(?:.*)Chapter (\d+(?:\.\d)?) *[:\-] *(.+)\Z")
    # not used, kept here for reference
    RE_URL = re.compile(r"(?:.*)?chapter-(\d+(?:-\d)?)-([\w\-]*)/?\Z")

    DEFAULTS = {
        "title": "Komi Can't Communicate",
        "url": "https://komi-san.com",
        "chapters": {},
    }

    def page_is_valid(self, tag):
        return self.IMGHOST in tag["src"]

    def parse_chapters(self):
        # get rid of section
        section = self.soup.find("section", class_="widget ceo_latest_comics_widget")
        if section is not None:
            section.decompose()

        for tag in self.soup.find_all("a"):

            if not self.is_link(tag):
                continue
            href = tag.get("href")
            title = tag.text

            match = self.RE_TITLE.findall(title)

            if match:
                id, title = match[0]
                yield id, title, href