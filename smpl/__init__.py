"""
A collection of simplified utilities
"""
import pkg_resources as pkg  # part of setuptools
import json
#import requests
#from urllib.request import urlopen

package = "smpl"

version = pkg.require(package)[0].version
__version__ = version

#def is_internet_available():
#    try:
#        urlopen('http://216.58.192.142', timeout=1)
#        return True
#    except:
#        return False


#
# repository_url='https://pypi.python.org/pypi/%s/json'
#
# url = repository_url % package
#
# if is_internet_available():
#
#     response = requests.get(url).text
#
#     latest_version =  json.loads(response)['info']['version']
#

#
#     parsed_latest = pkg.parse_version(latest_version)
#
#     parsed_version = pkg.parse_version(version)
#

#
#     if parsed_latest > parsed_version:
#
#         print("New version " + str(latest_version) + " > " + str(version) + " available via: \n $ pip install " + package + " --upgrade [--user]'")
#
#     elif parsed_latest < parsed_version:
#
#         print("You are using an unreleased version.")
