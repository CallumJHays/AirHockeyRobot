using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Air_Hockey_Simulator.Physics
{
    public class Puck
    {
        public double Weight { get; set; }
        public double Radius { get; set; }

        public PointD Location { get; set; }
        public Velocity Velocity { get; set; }
        public Line Path { get { return new Line(Location, Velocity.Direction); } }

        public Puck() {
            Velocity = new Velocity();
            Location = new PointD(0, 0);
        }
    }
}
