using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SteamKit
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Title = "The Bot";

            Bot _mainB = new Bot();
            _mainB.Run();

            Console.ReadKey();
        }
    }
}
