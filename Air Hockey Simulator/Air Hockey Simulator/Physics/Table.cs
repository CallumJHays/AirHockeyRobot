using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Air_Hockey_Simulator.Physics
{
    public class Table
    {
        public double Width { get; set; }
        public double Height { get; set; }

        public double Friction { get; set; }
        public double Goal_Width { get; set; }

        public List<Line> Walls { get; set; }
        public List<Arc> Arcs { get; set; } 

        public Table() {
            Walls = new List<Line>();
            Arcs = new List<Arc>();
        }
    }
}
