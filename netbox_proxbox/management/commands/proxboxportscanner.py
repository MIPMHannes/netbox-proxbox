import time

from django.core.management.base import BaseCommand
from django.utils import timezone
import asyncio

from netbox_proxbox.proxbox_api_v2.port_scanner import VMPortScanner


class Command(BaseCommand):
    help = "Run the proxbox scrapper"

    def add_arguments(self, parser):
        parser.add_argument('tenants', nargs='+', help="Tenants for the machines to get the ports")
        pass

    def handle(self, *args, **options):
        tenants = options.get('tenants')
        asyncio.run(VMPortScanner.async_run(tenants))
        # Scrapper.run()
        # Wrap things up
        self.stdout.write(
            "[{:%H:%M:%S}] Finished".format(timezone.now())
        )
