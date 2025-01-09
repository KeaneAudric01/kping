# kping 🚀

kping is a simple TCP ping tool written in Python. It allows you to ping a specified host and port, and provides detailed statistics about the ping results.

## Disclaimer ⚠️

The `.exe` file attached on the [release page](https://github.com/KeaneAudric01/kping/releases) might trigger a false positive virus detection (tested with Windows Defender). Please be assured that the file is safe to use.

## Features ✨

- Ping a specified host and port
- Continuous pinging until stopped
- Customizable interval between pings
- Option to include date and time on each line
- Automatically exit on a successful ping
- Verbose mode
- Custom timeout
- Ping flood mode

## Usage 📋

```
Usage: kping [-flags] server-address [server-port]

Usage (full): kping [-t] [-n times] [-H host] [-p port] [-i interval] [-d] [-s] [-f] [-v timeout] [-q]

 -t     : ping continuously until stopped via control-c
 -n 5   : for instance, send 5 pings
 -H     : specify the host to ping
 -p     : specify the port to ping
 -i 1   : set the interval between pings (in seconds)
 -d     : include date and time on each line
 -s     : automatically exit on a successful ping
 -f     : verbose mode
 -v 1   : set custom timeout (in seconds)
 -q     : ping flood (send pings as fast as possible)
```

### Example Commands

- Ping a host on the default port (80) 5 times:
    ```sh
    kping -H host.address
    ```

- Ping a host on port 443 continuously:
    ```sh
    kping -H host.address -p 443 -t
    ```

- Ping a host on port 8080 with a 2-second interval between pings:
    ```sh
    kping -H host.address -p 8080 -i 2
    ```

- Ping a host and include date and time on each line:
    ```sh
    kping -H host.address -d
    ```

## Installation 🛠️

### Prerequisites

- Python 3.x

### Install the `requests` module

To install the `requests` module, run the following command:

```sh
pip install requests
```

## Running the Script Directly with Python 🐍

To use the script directly with Python without creating an executable, follow these steps:

1. Ensure you have Python 3.x installed on your machine.
2. Install the `requests` module if you haven't already:

    ```sh
    pip install requests
    ```

3. Navigate to the directory containing `kping.py`:

    ```sh
    cd /path/to/kping
    ```

4. Run the script using Python:

    ```sh
    python kping.py -H host.address
    ```

## Building the Executable 🏗️

To build your own executable file from the source code, follow these steps:

1. Install `pyinstaller`:

    ```sh
    pip install pyinstaller
    ```

2. Navigate to the directory containing `kping.py`:

    ```sh
    cd /path/to/kping
    ```

3. Run `pyinstaller` to create the executable:

    ```sh
    pyinstaller --onefile kping.spec
    ```

4. The executable file will be created in the `dist` directory.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](https://github.com/KeaneAudric01/kping/blob/main/LICENSE) file for details.

## Author 👤

Keane Audric

GitHub: [KeaneAudric01](https://github.com/KeaneAudric01)
