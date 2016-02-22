using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Air_Hockey_Simulator.Physics
{
    public class PointD
    {
        public double X { get; set; }
        public double Y { get; set; }

        public PointD(double x, double y) {
            X = x; Y = y;
        }

        public static bool operator ==(PointD p1, PointD p2) {
            if (System.Object.ReferenceEquals(p1, p2)) return true;
            if ((object)p1 == null || (object)p2 == null) return false;
            return p1.X == p2.X && p1.Y == p2.Y;
        }

        public static bool operator !=(PointD p1, PointD p2) {
            return !(p1 == p2);
        }

        public override string ToString() {
            return string.Format("({0}, {1})", X, Y);
        }

        public double DistanceTo(PointD point) {
            return Math.Sqrt(Math.Pow(point.X - this.X, 2) + Math.Pow(point.Y - this.Y, 2));
        }

        public double DistanceTo(Line line) {
            Line perpendicular = line.Perpendicular(this);
            PointD intersection = line.IntersectionWith(perpendicular);
            return DistanceTo(intersection);
        }

        public PointD Offset(PointD point) {
            return new PointD(this.X + point.X, this.Y + point.Y);
        }
        public PointD Offset(double x, double y) {
            return new PointD(this.X + x, this.Y + y);
        }
    }
}
