import girder_client


def createGirderClient(api_url, api_key=None, username=None, password=None):
    print(api_url, api_key, username, password)
    gc = girder_client.GirderClient(apiUrl=api_url)

    if username and password:
        gc.authenticate(username=username, password=password)
    elif api_key:
        gc.authenticate(apiKey=api_key)

    return gc
