#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This module uses the Shodan library to interact with shodan.io to lookup and search for hostnames
and IP addresses.
"""

import click
import shodan
import requests

from . import helpers


class ShodanTools(object):
    """Class with various tools for itneracting with Shodan to search for IP addresses and domains."""
    shodan_dns_resolve_uri = "https://api.shodan.io/dns/resolve?hostnames={}&key={}"

    def __init__(self):
        """Everything that should be initiated with a new object goes here."""
        try:
            self.shodan_api_key = helpers.config_section_map("Shodan")["api_key"]
            self.shodan_api = shodan.Shodan(self.shodan_api_key)
        except Exception:
            self.shodan_api = None
            click.secho("[!] Did not find a Shodan API key.", fg="yellow")

    def run_shodan_search(self, target):
        """Collect information Shodan has for target domain name. This uses the Shodan search
        instead of host lookup and returns the target results dictionary from Shodan.

        A Shodan API key is required.
        """
        if self.shodan_api is None:
            pass
        else:
            try:
                target_results = self.shodan_api.search(target)
                return target_results
            except shodan.APIError as error:
                click.secho("\n[!] No Shodan data for {}!".format(target), fg="red")
                click.secho("L.. Details: {}".format(error), fg="red")

    def run_shodan_resolver(self, target):
        """Resolve a hosname to an IP address using the Shodan API's DNS endpoint.
        
        A Shodan API key is required.
        """
        if not helpers.is_ip(target):
            resolved = requests.get(self.shodan_dns_resolve_uri.format(target, self.shodan_api_key))
            target_ip = resolved.json()[target]
            return target_ip
        else:
            click.secho("[!] Only a hostname can be resolved to an IP address.", fg="red")

    def run_shodan_lookup(self, target):
        """Collect information Shodan has for target IP address. This uses the Shodan host lookup
        instead of search and returns the target results dictionary from Shodan.

        A Shodan API key is required.
        """
        if self.shodan_api is None:
            pass
        else:
            # click.secho("[+] Performing Shodan IP lookup for {}.".format(target), fg="green")
            try:
                target_results = self.shodan_api.host(target)
                return target_results
            except shodan.APIError as error:
                click.secho("\n[!] No Shodan data for {}!".format(target), fg="red")
                click.secho("L.. Details: {}".format(error), fg="red")
