import click

from c7ncli.group.setting_lm_client import client
from c7ncli.group.setting_lm_config import config


@click.group(name='lm')
def lm():
    """Manages License Manager Setting(s)"""


lm.add_command(config)
lm.add_command(client)
