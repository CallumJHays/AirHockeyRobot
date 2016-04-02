using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Air_Hockey_Simulator.Physics
{
    public class Arc
    {
        public PointD Point { get; set; }
        public double Radius { get; set; }

        public Angle Start { get; set; }
        public Angle End { get; set; }

        public Arc(PointD point, double radius)
        {
            Point = point;
            Radius = radius;
        }
    }
}
