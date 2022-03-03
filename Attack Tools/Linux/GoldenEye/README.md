# GoldenEye 

GoldenEye is an python app for SECURITY TESTING PURPOSES ONLY!

GoldenEye is a HTTP DoS Test Tool. 

Attack Vector exploited: HTTP Keep Alive + NoCache

## Usage

     USAGE: ./goldeneye.py <url> [OPTIONS]
    
     OPTIONS:
        Flag           Description                     Default
        -u, --useragents   File with user-agents to use                     (default: randomly generated)
        -w, --workers      Number of concurrent workers                     (default: 50)
        -s, --sockets      Number of concurrent sockets                     (default: 30)
        -m, --method       HTTP Method to use 'get' or 'post'  or 'random'  (default: get)
        -d, --debug        Enable Debug Mode [more verbose output]          (default: False)
        -h, --help         Shows this help


## Utilities
* util/getuas.py - Fetchs user-agent lists from http://www.useragentstring.com/pages/useragentstring.php subpages (ex: ./getuas.py http://www.useragentstring.com/pages/Browserlist/) *REQUIRES BEAUTIFULSOUP4*
* res/lists/useragents - Text lists (one per line) of User-Agent strings (from http://www.useragentstring.com)

## License
This software is distributed under the GNU General Public License version 3 (GPLv3)

## LEGAL NOTICE
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL USE ONLY! IF YOU ENGAGE IN ANY ILLEGAL ACTIVITY THE AUTHOR DOES NOT TAKE ANY RESPONSIBILITY FOR IT. BY USING THIS SOFTWARE YOU AGREE WITH THESE TERMS.
