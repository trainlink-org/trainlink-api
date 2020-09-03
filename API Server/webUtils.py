def obtainAddress(cabAddress, cabID):
    try:
        address = int(cabAddress)
        address = cabAddress
    except ValueError:
        try:
            address = cabID[cabAddress]
        except KeyError:
            print("Bad key")
    return address
