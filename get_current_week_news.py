import dataclasses
import datetime
from collections import OrderedDict

import cloudscraper
import orjson

_urls = (
    r'https://nfs.faireconomy.media/ff_calendar_thisweek.json',
    r'https://nfs.faireconomy.media/mm_calendar_thisweek.json',
    r'https://nfs.faireconomy.media/ee_calendar_thisweek.json',
    r'https://nfs.faireconomy.media/cc_calendar_thisweek.json'
)


@dataclasses.dataclass(kw_only=True, unsafe_hash=True, slots=True, eq=True)
class EconomyEvent:
    title: str
    country: str
    date: str | datetime.datetime | int | float
    impact: str = dataclasses.field(hash=False, compare=False)
    forecast: str
    previous: str

    def post_parse(self):
        if self.date and isinstance(self.date, str):
            self.date = int(datetime.datetime.fromisoformat(self.date).timestamp())
        if self.title:
            self.title = self.title.lower()
        if self.country:
            self.country = self.country.upper()


def download_news(urls=_urls) -> list[EconomyEvent]:
    coll = OrderedDict()  # use only OrderedDict's keys to mimic an OrderedSet
    with cloudscraper.create_scraper() as session:
        for url in urls:
            payload = session.get(url).json()
            for item in payload:
                event = EconomyEvent(**item)
                event.post_parse()
                coll[event] = True

    return sorted(coll.keys(), key=lambda x: x.date)


if __name__ == '__main__':
    print(orjson.dumps(download_news(), option=orjson.OPT_INDENT_2).decode())
