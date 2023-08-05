import argparse
from . import list_, new, remove, publish

parser = argparse.ArgumentParser(prog='theme')
parser.description = "Utility for managing shopify themes"
subparsers = parser.add_subparsers()

sub = subparsers.add_parser('list', aliases=['ls'])
sub.add_argument('-i', '--ids', action='store_true',
                 help="Just list theme ids")
sub.add_argument(
    '-x', '--regex', help="Return only themes where the name matches regex")
sub.add_argument(
    '-r', '--role', help="Return only themes where the name matches regex")
sub.add_argument(
    '-d', '--drop', type=int, help="Drop first n results")
sub.set_defaults(func=list_)

sub = subparsers.add_parser('new')
sub.add_argument('name')
sub.set_defaults(func=new)

sub = subparsers.add_parser('remove', aliases=['rm'])
sub.add_argument('ids', nargs="+")
sub.set_defaults(func=remove)

sub = subparsers.add_parser('publish', aliases=['pb', 'pub'])
sub.add_argument('id')
sub.set_defaults(func=publish)

args = parser.parse_args()
args.func(args)
