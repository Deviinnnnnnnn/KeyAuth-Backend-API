from fastapi import FastAPI
import os, requests, dhooks

os.system('cls')

app = FastAPI()

SELLER_KEY = "here"

WHITELISTED_IPS = ["1.1.1.1", "2.2.2.2"]

THREAT_LOG = "https://discord.com/api/webhooks/917948746515745291/BN_kxN6dcCeNDWEnuCSXT9lY9DIA_hCdyPPgUH8DPayhXKnsJOVIf4aRQga"

UNWHITELISTED_MESSAGE = "logged bud."

def isWhitelisted():
    y = requests.get("http://ip-api.com/json/").json()["query"]
    if y in WHITELISTED_IPS:
        return True
    else:
        return False

def getIP():
    return requests.get("http://ip-api.com/json/").json()["query"]

def logThreat(WEBHOOK, MESSAGE):
    if WEBHOOK != "":
        try:
            x = dhooks.Webhook(WEBHOOK)
            x.send(MESSAGE)
        except:
            pass

@app.get('/addlicense/')
def addlicense(*, expiry: str = None, level: str = None, amount: str = None, mask: str = "XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX"):
    # EXAMPLE - http://127.0.0.1:8000/addlicense/?expiry=7&level=1&amount=1&mask=TEST-XXX-XXX
    if expiry == None or level == None or amount == None:
        data_set = {'success': False, 'message': 'missing input'}
    else:
        y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=add&expiry={expiry}&mask={mask}&level={level}&amount={amount}&format=json"
        if isWhitelisted():
            if int(amount) == 1:
                z = requests.get(y).json()
                if z['success'] == True:
                    data_set = {'success': True, 'data': 'Key Successfully Generated', 'key': z['key']}
                else:
                    data_set = {'success': False, 'data': z['message']}
            else:
                z = requests.get(y).json()
                if z['success'] == True:
                    data_set = {'success': True, 'data': 'Key Successfully Generated', 'key': z['keys']}
                else:
                    data_set = {'success': False, 'data': z['message']}
        else:
            data_set = {'data': UNWHITELISTED_MESSAGE}
            logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/addsub/')
def addsub(*, name: str = None, level: str = None):
    # EXAMPLE http://127.0.0.1:8000/addsub/?name=Paid&level=1
    if name == None or level == None:
        data_set = {'success': False, 'message': 'missing input'}
    else:
        y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=addsub&name={name}&level={level}"
        if isWhitelisted():
            z = requests.get(y).json()
            if z['success'] == True:
                data_set = {'success': True, 'data': 'Subscription Added'}
            else:
                data_set = {'success': False, 'data': z['message']}
        else:
            data_set = {'data': UNWHITELISTED_MESSAGE}
            logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/verify/')
def verifykey(*, key: str = None):
    # EXAMPLE http://127.0.0.1:8000/verify/?key=8ZCARQ-9ZIE5O-EJ2278-9UTNB2-BNTWDN-KHZQ16
    if key == None:
        data_set = {'success': False, 'message': 'missing input'}
    else:
        y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=verify&key={key}"
        if isWhitelisted():
            z = requests.get(y).json()
            if z['success'] == True:
                data_set = {'success': True, 'data': 'Key Is Valid'}
            else:
                data_set = {'success': False, 'data': z['message']}
        else:
            data_set = {'data': UNWHITELISTED_MESSAGE}
            logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/activate/')
def activate(*, username: str = None, password: str = None, key: str = None):
    # EXAMPLE http://127.0.0.1:8000/activate/?username=devin&password=123&key=HSDB0R-3VPH3T-7B7VDH-9U1X29-EI4FFM-9T7WT2
    if username == None or password == None or key == None:
        data_set = {'success': False, 'message': 'missing input'}
    else:
        y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=activate&user={username}&key={key}&pass={password}"
        if isWhitelisted():
            z = requests.get(y).json()
            if z['success'] == True:
                data_set = {'success': True, 'data': 'Successfully Registered'}
            else:
                print(z)
                data_set = {'success': False, 'data': z['message']}
        else:
            data_set = {'data': UNWHITELISTED_MESSAGE}
            logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/deletekey/')
def deletekey(*, key: str = None):
    # EXAMPLE http://127.0.0.1:8000/deletekey/?key=HSDB0R-3VPH3T-7B7VDH-9U1X29-EI4FFM-9T7WT2
    if key == None:
        data_set = {'success': False, 'message': 'missing input'}
    else:
        y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=del&key={key}"
        if isWhitelisted():
            z = requests.get(y).json()
            if z['success'] == True:
                data_set = {'success': True, 'data': 'Successfully Deleted Key'}
            else:
                data_set = {'success': False, 'data': z['message']}
        else:
            data_set = {'data': UNWHITELISTED_MESSAGE}
            logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/deleteuser/')
def deleteuser(*, username: str = None):
    # EXAMPLE http://127.0.0.1:8000/deleteuser/?username=devin
    if username == None:
        data_set = {'success': False, 'message': 'missing input'}
    else:
        y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=deluser&user={username}"
        if isWhitelisted():
            z = requests.get(y).json()
            if z['success'] == True:
                data_set = {'success': True, 'data': 'Successfully Deleted User'}
            else:
                data_set = {'success': False, 'data': z['message']}
        else:
            data_set = {'data': UNWHITELISTED_MESSAGE}
            logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/deleteunusedkeys/')
def deleteunusedkeys():
    # EXAMPLE http://127.0.0.1:8000/deleteunusedkeys/
    y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=delunused"
    if isWhitelisted():
        z = requests.get(y).json()
        if z['success'] == True:
            data_set = {'success': True, 'data': 'Successfully Deleted Unused Keys'}
        else:
            data_set = {'success': False, 'data': z['message']}
    else:
        data_set = {'data': UNWHITELISTED_MESSAGE}
        logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set


@app.get('/deleteexpusers/')
def deleteexpusers():
    # EXAMPLE http://127.0.0.1:8000/deleteexpusers/
    y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=delexpusers"
    if isWhitelisted():
        z = requests.get(y).json()
        if z['success'] == True:
            data_set = {'success': True, 'data': 'Successfully Deleted Expired Users'}
        else:
            data_set = {'success': False, 'data': z['message']}
    else:
        data_set = {'data': UNWHITELISTED_MESSAGE}
        logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/deleteallkeys/')
def deleteallkeys():
    # EXAMPLE http://127.0.0.1:8000/deleteallkeys/
    y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=delalllicenses"
    if isWhitelisted():
        z = requests.get(y).json()
        if z['success'] == True:
            data_set = {'success': True, 'data': 'Successfully Deleted All Keys'}
        else:
            data_set = {'success': False, 'data': z['message']}
    else:
        data_set = {'data': UNWHITELISTED_MESSAGE}
        logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set

@app.get('/extenduser/')
def extenduser(*, username: str = None, name: str = None, days: str = None):
    # EXAMPLE http://127.0.0.1:8000/extenduser/?username=devin&name=default&days=7
    if username == None or days == None:
        data_set = {'success': False, 'message': 'missing input'}
    else:
        y = f"https://keyauth.com/api/seller/?sellerkey={SELLER_KEY}&type=extend&user={username}&name={name}&expiry={days}"
        if isWhitelisted():
            z = requests.get(y).json()
            if z['success'] == True:
                data_set = {'success': True, 'data': 'Successfully Extended User'}
            else:
                data_set = {'success': False, 'data': z['message']}
        else:
            data_set = {'data': UNWHITELISTED_MESSAGE}
            logThreat(THREAT_LOG, f'**Detected Unwhitelisted API Request!**\n**IP -> `{getIP()}`**\n**URL -> `&type{y.split("&type")[1]}`**')
    return data_set