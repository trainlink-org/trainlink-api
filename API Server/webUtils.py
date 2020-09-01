def obtainAddress(cabAddress, cabID):
    try:
        address = int(cabAddress)
        address = cabAddress
    except ValueError:
        address = cabID[cabAddress]
    return address
