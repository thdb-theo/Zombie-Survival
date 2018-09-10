using System;
using System.Collections.Generic;
using System.Linq;
using System.Drawing;
using System.IO;

namespace MapFromBitmap
{
    class Program
    {
        static void Main(string[] args)
        {
            string cwd = Environment.CurrentDirectory + "\\";
            string filename;
            try
            {
                filename = args[0];
            }
            catch (IndexOutOfRangeException)
            {
                filename = "test";
            }
            string path = cwd + "bitmaps\\" + filename + ".bmp";
            Bitmap bmp = new Bitmap(path);
            int[] nums = GetNums(args);
            var spawns = GetSpawns(bmp, nums);
            var z_spawns = spawns[0];
            var p_spawns = spawns[1];
            List<string> map = new List<string> { };
            for (int i = 0; i < bmp.Height * bmp.Width; i++)
            {
                int x = i % bmp.Width;
                int y = i / bmp.Width;
                string tile = "";
                var pixel = bmp.GetPixel(x, y);
                if (IsBlack(pixel))
                    tile = "#";
                else
                    tile = ".";
                int[] coordinate = new int[] { x, y };

                if (IsArrayInArrayOfArrays(z_spawns, coordinate))
                    tile = "Z";
                else if (IsArrayInArrayOfArrays(p_spawns, coordinate))
                    tile = "P";

                map.Add(tile);
                if ((x + 1) % bmp.Width == 0 && y != bmp.Height - 1)
                {
                    map.Add(Environment.NewLine);
                }
            }
            string AsString = string.Join("", map);
            Console.WriteLine(AsString);
            File.WriteAllText(cwd + "output.txt", AsString);
            }
        static List<int[]>[] GetSpawns(Bitmap bmp, int[] nums)
        {
            var return_val = new List<int[]>[2];
            List<int[]> taken = new List<int[]> { };
            Random random_gen = new Random();
            for(int i = 0; i < 2; i++)
            {
                List<int[]> current_spawns = new List<int[]> { };
                while (current_spawns.Count() < nums[i])
                {
                    int rnd = random_gen.Next(0, bmp.Width * bmp.Height);
                    int x = rnd / bmp.Height;
                    int y = rnd % bmp.Height;
                    int[] coordinate = new int[] { x, y };
                    var pixel = bmp.GetPixel( x, y );
                    if ((!IsBlack(pixel)) && (!IsArrayInArrayOfArrays(taken, coordinate)))
                    {
                        current_spawns.Add(coordinate);
                        taken.Add(coordinate);
                    }
                }
                return_val[i] = current_spawns;
            }
            return return_val;
        }

        static int[] GetNums(string[] args)
        {
            int[] nums = new int[2];

            if (args.Count() <= 1 || args.Count() >= 4)
            {
                raise new ArgumentOutOfRangeException("Too many or too few arguments");
            }
            else if (args.Count() == 2)
            {
                nums[0] = int.Parse(args[1]);
                nums[1] = nums[0];
            }
            else if (args.Count() == 3)
            {
                nums[0] = int.Parse(args[1]);
                nums[1] = int.Parse(args[2]);
            }
            else
            {
                throw new ArgumentOutOfRangeException("Too many command line arguments");
            }
            return nums;
        }

        static bool IsBlack(Color pixel)
        {
            return pixel.R == 0 && pixel.G == 0 && pixel.B == 0;
        }

        static bool IsArrayInArrayOfArrays<T>(IList<T[]> array1, IList<T> array2)
        {
            foreach(var element in array1)
            {
                if (element.SequenceEqual(array2))
                    return true;
            }
            return false;
        }
    }
}
