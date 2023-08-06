# OctoEverywhereAPI
Login into OctoEverywhere and use it in your app, instead of NGROK

# Usage
```py
from octoeverywhere import *

session = getSessionCookie("email@example.com", "password")
```

If we inserted correct login info, we should get something like this:
```
{'OctoEverywhereSessionKey': 'dnmdmkjasnmkjkj644kJhjjhhHSIJSAjJKHKJAJSJIUEWUEHXSHWETWQZROO94UZZW'}
```

Otherwise, an exception will be thrown:
```
Incorrect login info with status code of 403
```
