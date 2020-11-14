import pkg_resources as pkg  # part of setuptools
import json
import requests

package = "smpl"

version = pkg.require(package)[0].version
print(version)

repository_url='https://pypi.python.org/pypi/%s/json'
url = repository_url % package
response = requests.get(url).text
latest =  json.loads(response)['info']['version']

parsed_latest = pkg.parse_version(latest)
parsed_version = pkg.parse_version(version)

if parsed_latest > parsed_version:
    print("New version " + str(latest_version) + " > " + str(version) + " available via: \n $ pip install " + package + "'")