import click
import requests
import bs4

#
# simple scraper for SJSU. (i love beautiful soup!)
# it turns out that all the classes are in the page with the load classes button
# here is an example URL https://www.sjsu.edu/classes/schedules/fall-2023.php
#
@click.command()
@click.argument("url")
def class_scrape(url):
    rsp = requests.get(url)
    bs = bs4.BeautifulSoup(rsp.content, "html.parser")
    class_schedule = bs.find(id="classSchedule")
    thead = class_schedule.find("thead")
    headers = [th.get_text() for th in thead.find_all("th", recursive=True)]
    print(",".join(headers))
    tbody = class_schedule.find("tbody")
    for tr in tbody.find_all("tr"):
        data = []
        for td in tr.find_all("td"):
            a = td.find("a")
            href = a.get("href") if a else None
            if href and href.startswith("mailto:"):
                data.append("{} <{}>".format(td.get_text(), href.removeprefix("mailto:")))
            else:
                data.append(td.get_text())

        print(",".join(data))

if __name__ == '__main__':
    class_scrape()
