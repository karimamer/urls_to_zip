 URLs-to-ZIP Archive web service
================
URLs-to-ZIP Archive web service.
Stack of choice

    Programming Language Python 3.7  
    aiohttp

Decision making
Programming Language:

I choose python over other Languages Due to

    familiarity
    fast iteration
    Mature web echo system

I choose aiohttp

    aysnc first
    can scale easily to a million user https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
    lightweight
    easy to use and iterate on

Structure
```
(level one)
urls_to_zip_test ---|  (level two A)
|                   |-> urls_to_zip_test -|(level three)
|                   |                     |-> __init__.py
|                   |                     |-> main.py
|                   |
|                   |
|                   |
|                   |
|                   |
|                   |
|                   |
|                   |(level two B)
|                   |-> tests  ->|
|                                |-> init.py
|-> README.md                    |-> test_urls_to_zip_test.py
|-> poetry.lock
|-> pyproject.toml
|-> sample_archive.json
````

Folder structure
urls_to_zip_test

is the head folder
Level one

urls_to_zip_test

    README.md
    .pyproject.toml -> poetry config 
    poetry.lock -> lock file for python

Level two A

urls_to_zip_test
level 3

    init.py
    main.py contains the code to run the server

level two B

tests

    init.py
    test_tenatbase.py

Installation

    Install poetry https://poetry.eustace.io/
    run poetry install
    run poetry shell
    run python main.py

Code Documentation

main
```
 contains web views
                    | -> health_check -> to check if the service is running 
                    | -> archive_img -> get on value for a givien key
```
URLS
Create key value pair

POST http://127.0.0.1:800/archive_img Body ex -> {"filenmae":"code", "url":"test}

How to run ?
==================

cd url_to_zip_test
python main.py

Things I could have done better
  use a language with better threading and streaming support
