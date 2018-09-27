import requests

#todo need to add API passowrd

class Hyperspace:
    address = 'http://localhost'
    port = 5580
    headers = {
        'User-Agent': 'Hyperspace-Agent',
    }

    def __init__(self, address='http://localhost', port=5580):
        self.set_address(address)
        self.set_port(port)

    def set_address(self, address='http://localhost'):
        """Sets address of Hyperspace object to send requests to.
        If no address is set, resets to localhost.
        """
        self.address = address

    def set_port(self, port=5580):
        """Sets port of Hyperspace object to send requests to.
        If no port is set, resets to 5580.
        """
        self.port = port

    def http_get(self, path, data=None):
        """Helper HTTP GET request function that returns a decoded json dict.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers, files=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise HyperspaceError(resp.status_code, resp.json().get('message'))
        return resp.json()


    def http_get_bytes(self, path, data=None):
        """Helper HTTP GET request function that returns a byte array.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.get(url, headers=self.headers, files=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise HyperspaceError(resp.status_code, resp.json().get('message'))
        return resp


    def http_post(self, path, data=None):
        """Helper HTTP POST request function.
        Sends HTTP POST request to given path with given payload.
        """
        url = self.address + ':' + str(self.port) + path
        resp = requests.post(url, headers=self.headers, data=data)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise HyperspaceError(resp.status_code, resp.json().get('message'))
        try:
            return resp.json()
        except ValueError:
            return resp

    """Daemon API"""

    def get_constants(self):
        """Returns set of constants in use."""
        return self.http_get('/daemon/constants')

    def stop(self):
        """Cleanly shuts down the daemon."""
        return self.http_get('daemon/stop')

    def get_version(self):
        """Returns the version of hsd running."""
        version = self.http_get('/daemon/version')
        return version.get('version')

    """Consensus API"""

    def get_consensus(self):
        """Returns information about the consensus set."""
        return self.http_get('/consensus')

 #todo  
 # def validate_transactionset(self, transactionset):
        """Validates a set of transactions using the current utxo set.
        """
        #TODO: I'm not really sure what this does. Attempting to use this
        #method just returns the response "Method Not Allowed"
        #return self.http_post('/consensus/validate/transactionset', transactionset)

    """Gateway API"""

    def get_gateway(self):
        """Returns information aout the gateway."""
        return self.http_get('/gateway')

    def gateway_connect(self, netaddress):
        """Connects the gateway to a peer."""
        self.http_post('/gateway/connect/' + netaddress)

    def gateway_disconnect(self, netaddress):
        """Disconnects the gateway from a peer."""
        self.http_post('/gateway/disconnect/' + netaddress)

    """Host API"""

    def get_host(self):
        """Returns information about the host."""
        return self.http_get('/host')

    def set_host(self, host_settings):
        """Configures hosting parameters.
        """
        return self.http_post('/host', host_settings)

    def host_announce(self, netaddress=None):
        """Announces the host to the network as a source of storage."""
        payload = None
        if netaddress is not None:
            payload = {'netaddress': netaddress}
        return self.http_post('/host/announce', payload)

    def host_storage(self):
        """Returns a list of folders tracked by the storage manager."""
        return self.http_get('/host/storage').get('folders')

    def host_storage_add(self, path, size):
        """Adds a storage folder to the manager."""
        payload = {'path': path, 'size': size}
        return self.http_post('/host/storage/folders/add', payload)

    def host_storage_remove(self, path, force=False):
        """Removes a folder from the storage manager."""
        payload = {'path': path, 'force': force}
        return self.http_post('/host/storage/folders/remove', payload)

    def host_storage_resize(self, path, size):
        """Resizes a folder in the manager."""
        payload = {'path': path, 'size': size}
        return self.http_post('/host/storage/folder/resize', payload)

    def host_storage_sector_delete(self, merkleroot):
        """Deletes a sector from the manager."""
        return self.http_post('/host/storage/sector/' + merkleroot)

    def host_estimatescore(self, host_settings=None):
        """Returns the estimated HostDB score of the host using its current
        settings, combined with the provided settings.
        """
        return self.http_get('/host/estimatescore', host_settings)

    """HostDB API"""

    def get_hostdb(self):
        """Returns list of all known hosts."""
        return self.http_get('/hostdb/all').get('hosts')

    def get_hostdb_active(self, numhosts=None):
        """Returns list of active hosts.
        Optional parameter numhosts for maximum number of hosts returned.
        """
        payload = None
        if numhosts is not None:
            payload = {'numhosts': (None, str(numhosts))}
        return self.http_get('/hostdb/active', payload).get('hosts')

    def get_hostdb_host(self, pubkey):
        """Fetches detailed information about a particular host, including
        metrics regarding the score of the host within the database
        """
        return self.http_get('/hostdb/hosts/' + pubkey)

    """Miner API"""

    def get_miner(self):
        """Returns status of the miner."""
        return self.http_get('/miner')

    def start_miner(self):
        """Starts a single threaded CPU miner."""
        return self.http_get('/miner/start')

    def stop_miner(self):
        """Stops the CPU miner."""
        return self.http_get('/miner/stop')

    def get_block_header(self):
        """Returns a block header for mining.
        Returned as bytes.
        """
        return self.http_get_bytes('/miner/header').content

    def post_block_header(self, header):
        """Submits a header that has passed the POW.
        Must be sent as bytes.
        """
        return self.http_post('/miner/header', header)

    """Renter API"""

    def get_renter(self):
        """Returns current renter settings."""
        return self.http_get('/renter')

    def get_renter_prices(self):
        """Returns current renter settings."""
        return self.http_get('/renter/prices')

    def get_renter_contracts(self):
        """Returns a list of active contracts."""
        return self.http_get('/renter/contracts').get('contracts')

    def get_downloads(self):
        """Returns a list of files in the download queue."""
        return self.http_get('/renter/downloads').get('downloads')

    def get_files(self):
        """Returns a list of all files."""
        files = self.http_get('/renter/files')
        return files.get('files')

    def delete_file(self, hyperspacepath):
        """Deletes a renter file."""
        self.http_post('/renter/delete/' + hyperspacepath)

    def download_file(self, path, hyperspacepath):
        """Downloads a file from hyperspace.
        """
        payload = {'destination': (None, path)}
        self.http_get('/renter/download/' + hyperspacepath, payload)

    def rename_file(self, hyperspacepath, newhyperspacepath):
        """Renames a file."""
        payload = {'newhyperspacepath': newhyperspacepath}
        self.http_post('/renter/rename/' + hyperspacepath, payload)

    def upload_file(self, path, hyperspacepath):
        """Uploads a file to hyperspace.
        """
        payload = {'source': path}
        self.http_post('/renter/upload/' + hyperspacepath, payload)

    """Wallet API"""

    def get_wallet(self):
        """Returns information aout the wallet."""
        return self.http_get('/wallet')

    def get_address(self):
        """Returns a single address from the wallet."""
        return self.http_get('/wallet/address').get('address')

    def get_addresses(self):
        """Returns a list of addresses from the wallet."""
        return self.http_get('/wallet/addresses').get('addresses')

   #todo add changepassword

    def backup_wallet(self, destination):
        """Creates a backup of the wallet settings."""
        payload = {'destination': destination}
        return self.http_get('/wallet/backup', payload)

    def wallet_init(self, encryptionpassword=None):
        """Initializes a new wallet.
        Returns the wallet seed.
        """
        payload = None
        if encryptionpassword is not None:
            payload = {'encryptionpassword': encryptionpassword}
        return self.http_post('/wallet/init', payload).get('primaryseed')

    def wallet_load_seed(self, encryptionpassword, seed, dictionary='english'):
        """Gives the wallet a seed to track when looking for incoming transactions
        """
        payload = {'encryptionpassword': encryptionpassword,
                   'dictionary': dictionary,
                   'seed': seed}
        return self.http_post('/wallet/seed', payload)

    #todo add lock

    def wallet_seeds(self, dictionary='english'):
        """Returns the list of seeds in use by the wallet
        """
        payload = {'dictionary': dictionary}
        return self.http_get('/wallet/seeds', payload)

    def send_hyperspacecoins(self, amount, address):
        """Sends hyperspacecoins to an address or set of addresses
        Returns list of transaction IDs
        """
        payload = {'amount': amount, 'destination': address}
        return self.http_post('/wallet/spacecash', payload).get('transactionids')

    def load_siagkey(self, encryptionpassword, keyfiles):
        """Loads a key into the wallet that was generated by siag
        """
        payload = {'encryptionpassword': encryptionpassword,
                   'keyfiles': keyfiles}
        return self.http_post('/wallet/siagkey', payload)

    def lock_wallet(self):
        """Locks the wallet."""
        return self.http_post('/wallet/lock')

    def get_transaction(self, transaction_id):
        """Gets the transaction associated with a specific transaction id
        """
        return self.http_get('/wallet/transaction/' + transaction_id).get('transaction')

    def get_transactions(self, startheight, endheight):
        """Returns a list of transactions related to the wallet in chronological order
        """
        return self.http_get('/wallet/transactions?startheight=%d&endheight=%d' % (startheight, endheight))

    def get_transactions_related(self, address):
        """Returns a list of transactions related to the given address."""
        return self.http_get('/wallet/transactions/' + address).get('transactions')

    def unlock_wallet(self, encryptionpassword):
        """Unlocks the wallet."""
        payload = {'encryptionpassword': encryptionpassword}
        return self.http_post('/wallet/unlock', payload)

    def verify_address(self, address):
        """Returns if the given address is valid
        """
        return self.http_get('/wallet/verify/address/' + address).get('Valid')

    def change_password(self, encryptionpassword, newpassword):
        """Changes the wallet's encryption key
        """
        payload = {'encryptionpassword': encryptionpassword,
                   'newpassword': newpassword}
        return self.http_post('/wallet/changepassword', payload)


class HyperspaceError(Exception):
    """Exception raised when errors returned from hyperspace daemon
    """
    def __init__(self, status_code, message):
        super(HyperspaceError, self).__init__(message)
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return 'HTTP code: ' + repr(self.status_code) + ' With message: ' + repr(self.message)
