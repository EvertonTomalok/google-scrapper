import sys

import click

from src.domain.workers.ean_crawl import run_worker_ean_crawler
from src.domain.workers.product_crawl import run_worker_product_crawl
from src.helpers.tasks import TaskAsWorkers


@click.group("Google Scraper CLI")
def cli() -> None:
    ...


@cli.command()
@click.option("-w", "--num_workers", type=int, default=1, help="number of workers.")
def crawl_products_daemon(num_workers):
    workers = TaskAsWorkers(run_worker_product_crawl, num_workers=num_workers)
    try:
        workers.execute()
    except KeyboardInterrupt:
        if workers.num_workers > 1:
            for thread in workers.threads:
                thread.terminate()
        sys.exit(0)


@cli.command()
@click.option("-e", "--ean", type=str, required=True, help="Ean to Crawl.")
@click.option("-d", "--search_date", type=str, required=False, help="Date to filter.")
def crawl_ean(ean, search_date=None):
    run_worker_ean_crawler(ean, search_date)


if __name__ == "__main__":
    cli()
