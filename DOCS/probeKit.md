# ProbeKit

This is a simple toolkit to be used for basic reconaisance in penetration testing.
The toolkit provides utilites for:
    - Port Scanning,
    - Remote Host OS Detection,
    - Directory and subdomain brute forcing for remote domains.

The toolkit uses 3 separate modules to provide this functionality:

- `ports` -> Associated with both TCP and UDP basic but reliable port scanning,
    - with `sockets` based service detection.

- `osprobe` -> provides basic enumeration for remote host detection,
    - uses `TTL` based OS detection by sending an ICMP packet to the host,
    - also allows host detection by using `nmap` if installed and available.

- `fuzz` -> provides a simple bruteforcing attack mechanizm for web domains
    - provides 2 modes for bruteforcing:
        - `subdomain`: bruteforce for possible subdomains and virtual hosts on a subdomain
        - `directory`: bruteforce for possible directories on a web host

The toolkit provides a simple and easy to use command line interface for interacting with it and using the modules accordingly.

---
## Working parts of the toolkit
### _The interpreter_
The interpreter is the first thing the user interacts with, it provides a clean command line interface to work around the toolkit by either opening an interactive session or providing a basic shell based commandline interface.
(The shell based commandline based interface requires some working on but still manages to provide some required functionality)

### _The modules_
The modules provide methods to work in the toolkit. At the time of writing this documentation there are only 3 reconaissance based modules provided to the user.They are as follows:
- `ports`
- `osprobe`
- `fuzz`

For further information please look up the remaining documentation.