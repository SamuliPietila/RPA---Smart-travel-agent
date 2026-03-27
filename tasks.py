from datetime import datetime
from robocorp.tasks import task
from robocorp import browser
from playwright.sync_api import Page

from functions import SAP


@task

def main():

    SAP.matkakohde()
    SAP.testaa_vain_kalenteria()
    SAP.aseta_henkilömäärä()