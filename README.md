# MyIP Exporter

A simple prometheus exporter for reporting data about your current Internet 
connection, with data from ip-api.com.

## Installation

Run the following as root, or using *sudo* as appropriate:

1. Checkout the code:
   ```shell
   cd /usr/local/
   git clone https://github.com/dpage/myip_exporter.git
   ```

2. Create a virtual environment:
   ```shell
   cd myip_exporter
   python3 -m venv venv
   ```
   
3. Install dependencies:
   ```shell
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Setup and run the service:
   ```shell
   cp myip_exporter.service /etc/systemd/system/
   systemctl daemon-reload
   systemctl enable myip_exporter
   systemctl start myip_exporter
   ```
   
## Configuration

The following environment variables can be set to configure myip_cxporter. Add
and *Environment=* line to the service unit file in the *Service* section, e.g.

```shell
Environment=MYIP_PORT=1234 MYIP_CACHE_TIMEOUT=10
```

**MYIP_PORT**: Set the port number to listen on.

**MYIP_CACHE_TIMEOUT**: Set the timeout for cached data from ip-api.com. This 
defaults to 5 seconds. Set to 0 to disable caching.
