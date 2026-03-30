from datetime import datetime
from robocorp.tasks import task
from robocorp import browser
from playwright.sync_api import Page

from functions import SAP
from functions import EMV
from functions import sky

@task

def main():

    EMV.lahtopaikka()
    #SAP.matkakohde()
    #SAP.testaa_vain_kalenteria()
    #SAP.aseta_henkilömäärä()
    #SAP.filters()
    #sky.testaa_skyscanner_kalenteria()