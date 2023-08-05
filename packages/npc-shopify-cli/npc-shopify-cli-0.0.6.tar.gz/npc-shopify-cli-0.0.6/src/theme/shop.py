import os
from contextlib import contextmanager

import shopify
from dotenv import load_dotenv

from pyactiveresource.connection import ResourceNotFound

# .env file is git ignored so values will be taken from the
# github action's environment when we use this for real
load_dotenv()

API_KEY = os.environ['SHOPIFY_API_KEY']
API_PASSWORD = os.environ['SHOPIFY_API_PASSWORD']
STORE_URL = os.environ['SHOPIFY_STORE_URL']
API_VERSION = os.getenv('SHOPIFY_API_VERSION', default='2021-01')


class ShopifyError(RuntimeError):
    ...


@contextmanager
def temp_session():
    with shopify.Session.temp(STORE_URL, API_VERSION, API_PASSWORD):
        yield


@contextmanager
def find_theme_by_id(theme_id):
    with temp_session():
        try:
            yield shopify.Theme.find(theme_id)
        except ResourceNotFound as e:
            raise ShopifyError(f'Theme {theme_id} does not exist') from e


def list_themes():
    with temp_session():
        return shopify.Theme.find()


def create_theme(name):
    with temp_session():
        theme = shopify.Theme()
        theme.name = name
        theme.save()
        return theme


def remove_theme(theme_id):
    with find_theme_by_id(theme_id) as theme:
        if theme.role != 'unpublished':
            raise ShopifyError(f"Can't delete published theme {theme_id}")
        theme.destroy()
    return theme


def publish_theme(theme_id):
    with find_theme_by_id(theme_id) as theme:
        theme.role = "main"
        if theme.save():
            return theme
        else:
            msg = '{}'.format(", ".join(theme.errors.full_messages()))
            raise ShopifyError(msg)
