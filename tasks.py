from datetime import datetime
from robocorp.tasks import task
from robocorp import browser
from playwright.sync_api import Page
from seleniumbase import Driver

from functions import SAP
from functions import EMV


@task

def main():

    EMV.lahtopaikka()
    EMV.testaa_skyscanner_kalenteria()
    EMV.aseta_henkilömäärä()
    EMV.skyscanner_sivuII()
    SAP.matkakohde()
    SAP.testaa_vain_kalenteria()
    SAP.aseta_henkilömäärä()
    SAP.filters()
    SAP.hae_trivago_hotellit()

    