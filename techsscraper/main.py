import logging
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scraper import Scraper


def main(args=None):
    configure_logging(get_project_settings())
    logging.getLogger("scrapy.middleware").setLevel(logging.WARN)
    logging.getLogger("scrapy.statscollectors").setLevel(logging.WARN)
    logging.getLogger("scrapy.extensions.logstats").setLevel(logging.WARN)
    logging.getLogger("scrapy.core.engine").setLevel(logging.WARN)

    scraper = Scraper()
    scraper.scrape_all_blogs()


if __name__ == "__main__":
    main()
