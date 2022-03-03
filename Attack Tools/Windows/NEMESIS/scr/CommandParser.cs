#region LICENSE
/*
 * CommandParser - A GetOpt inspired command line parser that makes use of
 *                 C# and LINQ.  
 *
 * Copyright (c) 2009, Christopher Hahn <chahn.chris@gmail.com>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *  * Neither the name of the <organization> nor the
 *    names of its contributors may be used to endorse or promote products
 *    derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY <copyright holder> ''AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */
#endregion
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;

namespace Appature.Common {
    class CommandArgument : IEquatable<CommandArgument> {
        public string Name { get; set; }
        public string LongName { get; set; }
        public string Description { get; set; }
        public uint Flags { get; set; }
        public string ParameterName { get; set; }
        public Action<CommandParser, string> Action { get; set; }

        public bool Equals(CommandArgument other) {
            bool equals = false;

            if (this.Name.Equals(other.Name) &&
                this.LongName.Equals(other.LongName) &&
                this.Description.Equals(other.Description) &&
                this.Flags == other.Flags &&
                this.ParameterName.Equals(other.ParameterName)) {
                equals = true;
            }

            return equals;
        }
    }

    public class CommandArgumentFlags {
        public const uint None = 0x00000000;
        public const uint TakesParameter = 0x00000001;
        public const uint Required = 0x00000002;
        public const uint HideInUsage = 0x00000004;

        public static bool FlagEnabled(uint f0, uint f1) {
            return (f0 & f1) != 0;
        }

        public static bool FlagDisabled(uint f0, uint f1) {
            return (f0 & f1) == 0;
        }
    }

    public class CommandParser {
        
        private IList<CommandArgument> arguments = 
            new List<CommandArgument>();

        private IList<string> unknownCommands =
            new List<string>();

        private IList<string> missingRequired =
            new List<string>();

        //
        // the argument prefix list is used to designate the set of values
        // that are used to denote the start of an argument.  Long versions
        // are always assumed to be two instances of the string.  Thus,
        // if the short version is specified via "-", the long version
        // would be specified via "--".
        //
        public char[] ArgumentPrefixList { get; set; }
        
        //
        // shown on the help screen
        //
        public string ApplicationDescription { get; set; }
        
        //
        // this gets populated during a Parse() operation accumulating the list
        // of commands that were supplied that are not understood by the parser.
        //
        public IList<string> UnknownCommands { get { return this.unknownCommands; } }

        public IList<string> MissingRequiredCommands { get { return this.missingRequired; } }

        public CommandParser() {
            this.ArgumentPrefixList = new char[] { '-', '/' };
        }

        public CommandParser(string appDescription) {
            this.ApplicationDescription = appDescription;
            this.ArgumentPrefixList = new char[] { '-', '/' };
        }

        //
        // specifying a longName for a command argument is not optional
        // on purpose.  it takes very little effort to specify one when building
        // a tool, and it enhances the understandability of the tool greatly
        // if good long names are chosen when someone reads the tool's help screen.
        //
        public void Argument(string name,
                             string longName,
                             string description,
                             Action<CommandParser, string> action) {
            Argument(name,
                     longName,
                     description,
                     String.Empty,
                     CommandArgumentFlags.None,
                     action);
        }

        public void Argument(string name,
                             string longName,
                             string description,
                             uint flags,
                             Action<CommandParser, string> action) {
            Argument(name,
                     longName,
                     description,
                     String.Empty,
                     flags,
                     action);
        }
        
        public void Argument(string name,
                             string longName,
                             string description,
                             string paramName,
                             uint flags,
                             Action<CommandParser, string> action) {
            if (!ValidateArgument(name)) {
                throw new ArgumentException("Invalid command argument 'name' = " + name);
            }

            if (!ValidateArgument(longName)) {
                throw new ArgumentException("Invalid command argument 'longName' = " + longName);
            }

            this.arguments.Add(new CommandArgument() {
                    Name = name,
                    LongName = longName,
                    Description = description,
                    ParameterName = paramName,
                    Flags = flags,
                    Action = action,
                });
        }

        public void Parse() {
            //
            // This parser attempts to emulate, roughly, the behavior
            // of the POSIX getopt C runtime function for parsing
            // command line arguments.  This mechanism is fairly
            // easy to use as it is quite flexible in how it
            // lets you submit arguments for parsing.
            //
            // For example, all of these would be valid and equivalent 
            // command line arguments if you had flags 
            // p, q, and z where z takes an argument.
            //
            // -p -q -z7
            // -p -q -z 7
            // -pqz7
            // -p -qz7
            //
            // -p -qz "7"
            // -p -qz"7"
            //
            // The main difference between this parser and getopt, however,
            // is that with getopt you have to do command handling dispatch
            // yourself in a big switch statement.  This parser does
            // the dispatching automatically leveraging C#'s Action<> convention.
            //
            // This parser also provides a slightly more cumbersome syntax for
            // specifying arguments, but by paying this syntax tax, you get the
            // benefit of a help screen that can be generated automatically
            // for you based on the list of command arguments you supply to the 
            // parser.  This reduces the common burden a writer of a command line
            // tool has.  It also ensures that the help screen for the application
            // is always up to date whenever new flags or arguments are added
            // to the tool.
            //

            //
            // reset the tracking collections for unknown and missing
            // required commands
            //
            ResetTrackingCollections();

            //
            // first, we merge the whole command line into a single string
            // since we're going to have to parse char by char
            //
            var args = Environment.GetCommandLineArgs();
            var joined = String.Join(" ", args.Skip(1).ToArray());

            //
            // we keep track of all commands dispatched to determine if 
            // any commands that are required were not supplied
            //
            var dispatchedCommands = new List<CommandArgument>();

            //
            // these are the state variables that are used to track what's 
            // going on in the command line as we walk character by character
            // through it.
            //
            bool isLongArg = false;
            var argBuffer = String.Empty;
            CommandArgument currentCommand = null;

            //
            // now we walk through the characters of the array until
            // we determine if we've found a matching switch
            //
            for (int i = 0; i < joined.Length; i++) {
                if (IsArgStart(joined, i)) {
                    //
                    // if we've reached a new arg, but there is a current 
                    // command, that means we've been gathering a parameter
                    // for it and it needs to be dispatched now.
                    //
                    if (currentCommand != null) {
                        dispatchedCommands.Add(currentCommand);
                        currentCommand = DispatchCommand(currentCommand, argBuffer);
                    } else if ((currentCommand == null) && !String.IsNullOrEmpty(argBuffer.Trim())) {
                        this.unknownCommands.Add(argBuffer);
                    }
                    
                    //
                    // now that we're moving on to something new, we clear out
                    // the argument buffer.
                    //
                    argBuffer = String.Empty;

                    //
                    // we check if we're about to deal with a long argument
                    //
                    isLongArg = IsLongArg(joined, i);
                    if (isLongArg) { i++; }
                } else if (currentCommand == null) {
                    argBuffer += joined[i];

                    currentCommand = GetCommand(argBuffer, isLongArg);

                    if (currentCommand != null) {
                        argBuffer = String.Empty;

                        //
                        // if the current command doesn't take a parameter,
                        // then we just dispatch it to it's handler
                        //
                        if (CommandArgumentFlags.FlagDisabled(currentCommand.Flags, 
                                                              CommandArgumentFlags.TakesParameter)) {
                            dispatchedCommands.Add(currentCommand);
                            currentCommand = DispatchCommand(currentCommand, String.Empty);
                        }
                    }
                } else if (currentCommand != null) {
                    argBuffer += joined[i];
                }
            }

            //
            // if we exit the loop, and there's still a command waiting to
            // be dispatched, then we've been gathering the parameter to the
            // end of the string, so we need to dispatch it now
            //
            if (currentCommand != null) {
                dispatchedCommands.Add(currentCommand);
                currentCommand = DispatchCommand(currentCommand, argBuffer);
            } else if ((currentCommand == null) && !String.IsNullOrEmpty(argBuffer.Trim())) {
                this.unknownCommands.Add(argBuffer);
            }
            
            //
            // now that we're done with all the dispatching, we need to determine
            // if there were any required commands that didn't get supplied
            // and store that set for the caller to use
            //
            this.missingRequired = DetermineMissingRequiredCommands(dispatchedCommands);
        }

        public string GetHelp() {
            StringBuilder text = new StringBuilder();

            var appName = System.AppDomain.CurrentDomain.FriendlyName.ToLower();

            WriteLine(text, String.Empty);

            //
            // write out the application header
            //
            if (!String.IsNullOrEmpty(this.ApplicationDescription)) {
                WriteLine(text, appName + " - " + this.ApplicationDescription);
            } else {
                WriteLine(text, appName);
            }

            //
            // write out the usage string
            //
            WriteLine(text, String.Empty);
            WriteLine(text, GetUsageString(appName));
            WriteLine(text, String.Empty);

            //
            // write out the commands
            //
            WriteLine(text, "Available commands:");
            WriteLine(text, "-------------------");

            //
            // figure out the longest command expression
            //
            var exprLength = this.arguments.Select(c => (GetCommandDisplayName(c.Name).Length + 
                                                         GetCommandDisplayLongName(c.LongName).Length)).Max();

            foreach (var command in this.arguments) {
                WriteLine(text, 
                          GetCommandHelpDisplay(command.Name, command.LongName).PadRight(exprLength + 5, ' ') +
                          command.Description);
            }
            
            return text.ToString();
        }
        
        private bool IsArgStart(string joined, int index) {
            return this.ArgumentPrefixList.Contains(joined[index]);
        }

        private bool IsLongArg(string joined, int index) {
            bool isLong = false;

            if (((index + 1) < joined.Length) &&
                this.ArgumentPrefixList.Contains(joined[index + 1])) {
                isLong = true;
            }

            return isLong;
        }

        private CommandArgument DispatchCommand(CommandArgument ca,
                                                string param) {
            ca.Action(this, param.Trim());
            return null;
        }

        private CommandArgument GetCommand(string argBuffer, bool useLong) {
            CommandArgument ca = null;

            if (!useLong) {
                ca = this.arguments.Where(a => a.Name.Equals(argBuffer)).FirstOrDefault();
            } else {
                ca = this.arguments.Where(a => a.LongName.Equals(argBuffer)).FirstOrDefault();
            }

            return ca;
        }

        private string GetCommandDisplayName(string c) {
            return this.ArgumentPrefixList[0] + c;
        }

        private string GetCommandDisplayLongName(string c) {
            var sb = new StringBuilder();
            sb.Append(this.ArgumentPrefixList[0]);
            sb.Append(this.ArgumentPrefixList[0]);
            sb.Append(c);

            return sb.ToString();
        }

        private string GetUsageString(string appName) {
            var sb = new StringBuilder();

            //
            // usage start
            //
            sb.Append("Usage: ");
            sb.Append(appName);
            sb.Append(' ');

            //
            // required arguments
            //
            var required = this.arguments.Where(a => 
                                                CommandArgumentFlags.FlagEnabled(a.Flags, CommandArgumentFlags.Required) &&
                                                CommandArgumentFlags.FlagDisabled(a.Flags, CommandArgumentFlags.HideInUsage)).ToList();
            if (required.Count > 0) {
                AppendArgumentsToUsage(sb, required);
            }
            
            //
            // optional arguments
            //
            var optional = this.arguments.Where(a => 
                                                CommandArgumentFlags.FlagDisabled(a.Flags, CommandArgumentFlags.Required) &&
                                                CommandArgumentFlags.FlagDisabled(a.Flags, CommandArgumentFlags.HideInUsage)).ToList();
            if (optional.Count > 0) {
                sb.Append(" [");
                AppendArgumentsToUsage(sb, optional);
                sb.Append("]");
            }

            return sb.ToString();
        }

        private void AppendArgumentsToUsage(StringBuilder sb, IList<CommandArgument> arguments) {
            foreach (var opt in arguments) {
                sb.Append(GetCommandDisplayName(opt.Name));
                if (CommandArgumentFlags.FlagEnabled(opt.Flags, CommandArgumentFlags.TakesParameter)) {
                    if (!String.IsNullOrEmpty(opt.ParameterName)) {
                        sb.Append(" <");
                        sb.Append(opt.ParameterName);
                        sb.Append(">");
                    } else {
                        sb.Append(" <arg>");
                    }
                }

                sb.Append(' ');
            }
            
            sb.Remove(sb.Length - 1, 1);
        }

        private string GetCommandHelpDisplay(string name, string longName) {
            return GetCommandDisplayName(name) + ", " + 
                   GetCommandDisplayLongName(longName);
        }

        private bool ValidateArgument(string arg) {
            bool valid = true;

            if (!String.IsNullOrEmpty(arg)) {
                foreach (var prefix in this.ArgumentPrefixList) {
                    if (arg.Contains(prefix)) {
                        valid = false;
                        break;
                    }
                }
            } else {
                valid = false;
            }

            return valid;
        }

        private void ResetTrackingCollections() {
            this.unknownCommands = new List<string>();
            this.missingRequired = new List<string>();
        }

        private IList<string> DetermineMissingRequiredCommands(IList<CommandArgument> dispatchedCommands) {
            IList<string> missing = new List<string>();

            //
            // figure out which arguments are required
            //
            var required = 
                this.arguments.Where(a => 
                                     CommandArgumentFlags.FlagEnabled(a.Flags, CommandArgumentFlags.Required)).ToList();
            
            if (required.Count > 0) {
                //
                // if we actually have some required arguments, then some might
                // not have been dispatched, which means they're missing
                //
                foreach (var requiredCommand in required) {
                    if (!dispatchedCommands.Contains(requiredCommand)) {
                        missing.Add(requiredCommand.LongName);
                    }
                }
            }

            return missing;
        }

        private static void WriteLine(StringBuilder sb, string s) {
            sb.Append(s);
            sb.Append(Environment.NewLine);
        }
    }
}