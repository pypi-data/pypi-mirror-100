import re
from datetime import datetime

from . import shop


def split_timestamp(s):
    dt = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z')
    return (dt.strftime("%d %b"), dt.strftime('%H:%M'))


def theme_id(theme):
    return int(theme.id)


def name_matches(theme, regex):
    return True if re.search(regex, theme.name) else False


def list_(args):
    result = reversed(sorted(shop.list_themes(), key=theme_id))

    if args.regex:
        result = [theme for theme in result if name_matches(theme, args.regex)]

    if args.role:
        result = [theme for theme in result if theme.role == args.role]

    if args.drop:
        result = [theme for i, theme in enumerate(result) if i >= args.drop]

    for theme in result:
        if args.ids:
            print(theme.id)
        else:
            dt, ts = split_timestamp(theme.created_at)
            print('{:<15}{:<12}{:<7}{:<6}{}'.format(theme.id, theme.role,
                                                    dt, ts, theme.name))

    return result


def new(args):
    theme = shop.create_theme(args.name)
    print(theme.id)


def remove(args):
    for id_ in args.ids:
        try:
            theme = shop.remove_theme(id_)
            print(f'Deleted {theme.id} ({theme.name})')
        except shop.ShopifyError as e:
            exit(f'ERROR: {e}')


def publish(args):
    try:
        theme = shop.publish_theme(args.id)
        print(f'Published {theme.id} ({theme.name})')
    except shop.ShopifyError as e:
        exit(f'ERROR: {e}')
