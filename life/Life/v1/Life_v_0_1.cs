using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Life.v1
{

    public class Life_v_0_1
    {
        private Grid _grid;
        public Life_v_0_1()
        {
            _grid = new Grid(0, Constants.N);
            StartLife();
        }
        private void StartLife()
        {
            bool alive = true;
            while (alive)
            {
                var newGen = new Grid(_grid);
                _grid = newGen;
                alive = _grid.Count > 0;
            }
        }
    }

    public class Cell
    {
        private int _x;
        private int _y;
        private bool _alive;
        private List<Cell> _neighbours;

        public Cell(int x, int y, bool alive = false)
        {
            _x = x;
            _y = y;
            _alive = alive;
            _neighbours = new List<Cell>();
        }

        public int AliveNeighboursCount()
        {
            int neighboursCount = 0;
            foreach (var cell in _neighbours)
                if (cell.Alive) neighboursCount++;
            return neighboursCount;
        }

        public int PrintAliveNeighbours()
        {
            int neighboursCount = 0;
            Console.Write("( ");
            foreach (var cell in _neighbours)
                if (cell.Alive) Console.Write(" [" + cell.X + "," + cell.Y + "]");
            Console.WriteLine(" )");
            return neighboursCount;
        }


        public bool Alive
        {
            get { return _alive; }
            set { _alive = value; }
        }

        public void AddNeighbour(ref Cell cell)
        {
            //Console.WriteLine("Adding neighbour: [" + cell.X + ", " + cell.Y + "]");
            _neighbours.Add(cell);
        }

        public override string ToString()
        {
            return _x.ToString("D2") + " " + _y.ToString("D2") + " " + (_alive ? "+" : "-");
        }

        public int X { get { return _x; } }
        public int Y { get { return _y; } }
    }

    public class Grid
    {
        private int N;
        private int _gen;
        private Cell[,] _grid;

        public Grid(int gen, int n = 10)
        {
            _gen = gen;
            N = n;
            _grid = new Cell[N, N];
            for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++)
                    _grid[i, j] = new Cell(i, j);
            FillNeighbours();
            if (_gen == 0)
            {
                SetInitial(3);
            }
            Console.WriteLine(ToString());
        }

        public Grid(Grid grid)
        {
            N = grid.N;
            _gen = grid.Gen + 1;
            _grid = new Cell[N, N]; for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++)
                    _grid[i, j] = new Cell(i, j);

            FillNeighbours();

            //Console.WriteLine("Just created: ");
            //Print();
            Console.Clear();
            Console.WriteLine("Initial: ");
            grid.Print();

            for (int i = 0; i < N; i++)
            {
                for (int j = 0; j < N; j++)
                {
                    var cell = grid.Cells()[i, j];
                    var cnt = cell.AliveNeighboursCount();
                    if (!cell.Alive && cnt == Constants.CountToBorn)
                        _grid[i, j].Alive = true;
                    if (cell.Alive && cnt >= Constants.CountToStayAliveMin && cnt <= Constants.CountToStayAliveMax)
                        _grid[i, j].Alive = true;
                }
            }
            //Print();

            System.Threading.Thread.Sleep(100);
            //Console.ReadLine();
            //Print();
        }

        private void FillNeighbours()
        {
            for (int i = 0; i < N; i++)
            {
                for (int j = 0; j < N; j++)
                {
                    //Console.WriteLine("For cell [ " + i + ", " + j + " ]");
                    _grid[i, j].AddNeighbour(ref _grid[(N + i - 1) % N, (N + j - 1) % N]);
                    _grid[i, j].AddNeighbour(ref _grid[(N + i - 1) % N, (N + j - 0) % N]);
                    _grid[i, j].AddNeighbour(ref _grid[(N + i - 1) % N, (N + j + 1) % N]);

                    _grid[i, j].AddNeighbour(ref _grid[(N + i - 0) % N, (N + j - 1) % N]);
                    _grid[i, j].AddNeighbour(ref _grid[(N + i - 0) % N, (N + j + 1) % N]);

                    _grid[i, j].AddNeighbour(ref _grid[(N + i + 1) % N, (N + j - 1) % N]);
                    _grid[i, j].AddNeighbour(ref _grid[(N + i + 1) % N, (N + j - 0) % N]);
                    _grid[i, j].AddNeighbour(ref _grid[(N + i + 1) % N, (N + j + 1) % N]);
                    //Console.ReadLine();
                }
            }
        }


        private void SetInitial(int regime = 0)
        {
            if (regime == 0)
            {
                for (int i = 0; i < N; i += 2)
                    for (int j = 0; j < N; j++)
                        _grid[i, j].Alive = true;
            }
            else if (regime == 1)
            {
                var rnd = new Random();
                for (int i = 0; i < N; i += 2)
                    for (int j = 0; j < N; j++)
                        _grid[i, j].Alive = rnd.NextDouble() > 0.5 ? true : false;

            }
            else if (regime == 2)
            {
                // Set Stable
                _grid[1, 2].Alive = true;
                _grid[2, 1].Alive = true;
                _grid[2, 3].Alive = true;
                _grid[3, 1].Alive = true;
                _grid[3, 3].Alive = true;
                _grid[4, 2].Alive = true;
            }
            else if (regime == 3)
            {
                // Set planner
                _grid[6, 3].Alive = true;
                _grid[7, 1].Alive = true;
                _grid[7, 3].Alive = true;
                _grid[8, 2].Alive = true;
                _grid[8, 3].Alive = true;
            }
            else if (regime == 4)
            {
                // Set pasek
                _grid[1, 6].Alive = true;

                _grid[2, 5].Alive = true;
                _grid[2, 7].Alive = true;

                _grid[3, 5].Alive = true;
                _grid[3, 7].Alive = true;

                _grid[4, 6].Alive = true;

                _grid[5, 2].Alive = true;
                _grid[5, 3].Alive = true;
                _grid[5, 9].Alive = true;
                _grid[5, 10].Alive = true;

                _grid[6, 1].Alive = true;
                _grid[6, 4].Alive = true;
                _grid[6, 8].Alive = true;
                _grid[6, 11].Alive = true;

                _grid[7, 2].Alive = true;
                _grid[7, 3].Alive = true;
                _grid[7, 9].Alive = true;
                _grid[7, 10].Alive = true;

                _grid[8, 6].Alive = true;

                _grid[9, 5].Alive = true;
                _grid[9, 7].Alive = true;

                _grid[10, 5].Alive = true;
                _grid[10, 7].Alive = true;

                _grid[11, 6].Alive = true;
            }
        }

        public Cell GetCell(int x, int y)
        {
            return _grid[x, y];
        }

        public Cell[,] Cells()
        {
            return _grid;
        }

        public int Gen { get { return _gen; } }

        public int Count
        {
            get
            {
                var count = 0;
                foreach (var cell in _grid)
                    if (cell.Alive) count++;
                return count;
            }
        }

        public override string ToString()
        {
            string str = "";
            str += "Gen: " + _gen + " Alive: " + Count;
            return str;
        }

        public void Print()
        {
            Console.WriteLine("Generation: " + Gen);
            Console.Write(" ");
            for (int i = 0; i < Constants.N; i++)
                Console.Write(i.ToString("d2"));

            Console.WriteLine();
            for (int i = 0; i < Constants.N; i++)
            {
                Console.Write(i.ToString("d2"));
                for (int j = 0; j < Constants.N; j++)
                    Console.Write(_grid[i, j].Alive ? "+ " : "  ");
                Console.WriteLine();
            }
        }
    }

    public static class Constants
    {
        public static int N = 30;
        public static int CountToBorn = 3;
        public static int CountToStayAliveMin = 2;
        public static int CountToStayAliveMax = 3;
    }
}
