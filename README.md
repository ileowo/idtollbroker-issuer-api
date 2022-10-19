<h1 align="center">
    Bolagsverket (Proof of Business) - MyCompany Wallet Portal Backend
</h1>

<p align="center">
    <a href="/../../commits/" title="Last Commit"><img src="https://img.shields.io/github/last-commit/L3-iGrant/pob-backend?style=flat"></a>
    <a href="/../../issues" title="Open Issues"><img src="https://img.shields.io/github/issues/L3-iGrant/pob-backend?style=flat"></a>
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#release-status">Release Status</a> •
  <a href="#licensing">Licensing</a>
</p>

## About

This repository hosts the source code for Bolagsverket Proof-Of-Business project  (Portal backend)
## Release Status

Release 1.0 - The release is in alpha demo stage. 
## Installation

Requirements:
- python 3.8.1.2 and pip3
## Steps to run

1. Clone this repo

```sh
$ git clone https://github.com/L3-iGrant/pob-backend
$ cd pob-backend/code
```

2. Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

3. Install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

4. Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
The server should be running at `http://127.0.0.1:8000/`.

5. Create super user
```sh
(env)$ cd project
(env)$ python manage.py createsuperuser



## Licensing
Copyright (c) 2022-25 Bolagsverket, Sweden

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the LICENSE for the specific language governing permissions and limitations under the License.
