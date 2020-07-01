using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace StuffProject
{
    class Program
    {
        static void Main(string[] args)
        {
            int[] a = { 0, 0, 0, 0, 0 };
            int aa = a.Count(x => x == 0);
            int bb = a.GroupBy(x => x != 0).Count();
            if (a.GroupBy(x => x == 0).Count() == 5)
            {
                int i = 4;
            }
        }
    }
}
