# commonconf

[![Build Status](https://github.com/uw-it-aca/commonconf/workflows/tests/badge.svg?branch=master)](https://github.com/uw-it-aca/commonconf/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/commonconf/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/commonconf?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/commonconf.svg)](https://pypi.python.org/pypi/commonconf)
![Python versions](https://img.shields.io/pypi/pyversions/commonconf.svg)

Configuring an application's settings can be tricky.  We tend to use Django for our apps, so we use Django settings.  But - then if we write a helpful library, and we use Django settings, the library is only useful for Django developers.  On the other hand, if we use another settings library (and there are many!), we need to have two types of configuration in our apps.

That's no good!

This library is designed to be a drop-in replacement for Django settings usage, while potentially reading settings from other libraries.  It's an easy way to remove 1 Django dependency.

Currently there are backends for Django settings and ConfigParser.  To use Django settings, the easiest way is to add this to your project's settings.py:


    from commonconf.backends import use_django_backend
    use_django_backend()

To use ConfigParser, do this in your initialization. (?)

    from commonconf.backends import use_configparser_backend
    use_configparser_backend("path/to/your_settings.cfg", "Section Name")

This in your code you can do:

    from commonconf import settings

    foo = settings.DEBUG
    bar = getattr(settings, "MISSING_KEY", "DEFAULT VALUE")

Pull requests welcome.

