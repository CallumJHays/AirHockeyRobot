using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Air_Hockey_Simulator.Physics
{
    public class Line
    {
        public PointD Point { get; set; }
        public double? Slope { get; set; }

        public Angle Angle {
            get {
                return this.Slope != null ? new Angle(Math.Atan((double)this.Slope), AngleType.Radians) : Angle._90;
            }
            set {
                if (value == Angle._90 || value == Angle._270)
                    Slope = null;
                else
                    Slope = Math.Tan(value);
            }
        }

        public Line(PointD point, double? slope) {
            Point = point; Slope = slope;
        }

        public Line(PointD point, Angle angle) {
            Point = point; Angle = angle;
        }

        public static bool operator ==(Line l1, Line l2) {
            if (System.Object.ReferenceEquals(l1, l2)) return true;
            if ((object)l1 == null || (object)l2 == null) return false;
            return l1.Point == l2.Point && l2.Slope == l2.Slope;
        }

        public static bool operator !=(Line l1, Line l2) {
            return !(l1 == l2);
        }

        public double? Y(double x) {
            return Slope == null ? null : Slope * (x - Point.X) + Point.Y;
        }

        public double? X(double y) {
            return Angle == Angle._0 || Angle == Angle._180 ? Point.X : (y - Point.Y) / Slope + Point.X;
        }

        public Line Parallel(PointD point) {
            return new Line(point, this.Slope);
        }

        public Line Perpendicular(PointD point) {
            return new Line(point, this.Slope != null ? -1 / this.Slope : 0);
        }

        public PointD IntersectionWith(Line line) {
            if (this.Slope == line.Slope) return null;
            else if (this.Slope == null) {
                return new PointD(Point.X, line.Y(Point.X).Value);
            }
            else if (line.Slope == null) {
                return line.IntersectionWith(this);
            }
            else {
                double x = (this.Point.Y + (double)line.Slope * line.Point.X - (double)this.Slope * this.Point.X - line.Point.Y) / ((double)line.Slope - (double)this.Slope);
                double y = (double)this.Slope * (x - this.Point.X) + this.Point.Y; //Basically just Y(x)
                return new PointD(x, y);
            }
        }

        public PointD[] IntersectionWith(Arc arc)
        {
            if (arc.Point.DistanceTo(this) > arc.Radius) return null;

            double a = Math.Pow(Slope.Value, 2) + 1;
            double b = 2 * ((Point.Y * Slope.Value) - (Point.X * Math.Pow(Slope.Value, 2)) - (arc.Point.Y * Slope.Value) - arc.Point.X);
            double c = Math.Pow(arc.Point.X, 2) - Math.Pow(arc.Radius, 2) +
                       (Math.Pow(Point.X, 2)*Math.Pow(Slope.Value, 2)) - (2*Point.X*Point.Y*Slope.Value) +
                       (2*Point.X*arc.Point.Y*Slope.Value) + Math.Pow(Point.Y, 2) - (2*Point.Y*arc.Point.Y) +
                       Math.Pow(arc.Point.Y, 2);

            double x1 = (-b + Math.Sqrt(b*b - 4*a*c))/(2*a);
            double x2 = (-b - Math.Sqrt(b*b - 4*a*c))/(2*a);
            return new PointD[] {new PointD(x1, Y(x1).Value), new PointD(x2, Y(x2).Value) };
        }
    }
}
