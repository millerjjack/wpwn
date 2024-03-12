<H2>WPwn</H2>
Eats WPSCAN output and automates inital reporting.

<H3>Usage</H3>

1. Copy your wpscan output to same directory.
2. <code>python3 main.py -f scan.txt -u http://target-address.com.au</code>

The common.txt file is used to check if enumerated WP users are default or common - raises corresponding finding.

To do:
- use requests to check urls and cover remaining WP findings.
- make pretty banner art
- compatibility upgrades for --json wpscan files
- general code clean-up
