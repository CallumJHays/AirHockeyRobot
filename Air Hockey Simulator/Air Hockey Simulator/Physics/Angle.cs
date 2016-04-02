using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Air_Hockey_Simulator.Physics
{
    public class Angle
    {
        public AngleType Type { get; set; }
        public double Measure { get; set; }

        public Angle(double measure, AngleType type) {
            Measure = measure; Type = type;
        }

        public static Angle _0 { get { return new Angle(0, AngleType.Degrees); } }
        public static Angle _90 { get { return new Angle(90, AngleType.Degrees); } }
        public static Angle _180 { get { return new Angle(180, AngleType.Degrees); } }
        public static Angle _270 { get { return new Angle(270, AngleType.Degrees); } }

        public static Angle operator +(Angle a1, Angle a2) {
            double new_measure = a1.ToRadians().Measure + a2.ToRadians().Measure;
            return new Angle(new_measure, AngleType.Radians);
        }

        public static Angle operator -(Angle a1, Angle a2) {
            double new_measure = a1.ToRadians().Measure - a2.ToRadians().Measure;
            return new Angle(new_measure, AngleType.Radians);
        }

        public static bool operator ==(Angle a1, Angle a2) {
            if (System.Object.ReferenceEquals(a1, a2)) return true;
            if ((object)a1 == null || (object)a2 == null) return false;
            return a1.Measure == a2.Measure;
        }

        public static bool operator !=(Angle a1, Angle a2) {
            return !(a1 == a2);
        }

        public static implicit operator double (Angle d) {
            return d.ToRadians().Measure;
        }
        public static implicit operator Angle(double d) {
            return new Angle(d, AngleType.Radians);
        }

        public override string ToString() {
            return this.Measure.ToString();
        }
        public string ToString(AngleType type) {
            return type == AngleType.Degrees ? this.ToDegrees().Measure.ToString() : this.ToRadians().Measure.ToString();
        }

        public Angle ToDegrees() {
            return Type == AngleType.Radians ? ToDegrees(this.Measure) : this;
        }
        private static Angle ToDegrees(double radians) {
            return new Angle((radians * 180) / Math.PI, AngleType.Degrees);
        }

        public Angle ToRadians() {
            return Type == AngleType.Degrees ? ToRadians(this.Measure) : this;
        }
        private static Angle ToRadians(double degrees) {
            return new Angle((degrees * Math.PI) / 180, AngleType.Radians);
        }

        public Angle Simplify() {
            return Simplify(this);
        }
        private static Angle Simplify(Angle angle) {
            double remainder = 0;
            if (angle.Type == AngleType.Degrees) {
                remainder = angle.Measure % 360;
                if (remainder < 0)
                    remainder = 360 + remainder;
            }
            else if (angle.Type == AngleType.Radians) {
                remainder = angle.Measure % (2 * Math.PI);
                if (remainder < 0)
                    remainder = (2 * Math.PI) + remainder;
            }
            else {
                throw new Exception("Unknown angle type");
            }
            return new Angle(remainder, angle.Type);
        }

        public Angle Reduce() {
            return Reduce(this);
        }
        private static Angle Reduce(Angle angle) {
            angle = angle.Simplify();
            if (angle.Measure > Angle._270) { angle -= Angle._270; }
            else if (angle.Measure > Angle._180) { angle -= Angle._180; }
            else if (angle.Measure > Angle._90) { angle -= Angle._90; }
            return angle;
        }

        public Angle Reflect(Angle mirror_line) {
            return Reflect(this, mirror_line);
        }
        private static Angle Reflect(Angle angle, Angle mirror_line) {
            mirror_line = mirror_line.Simplify();
            Angle diff = (mirror_line - angle.Simplify()).Simplify();
            if (Math.Abs(diff) > Angle._90) {
                mirror_line = (mirror_line + Angle._180).Simplify();
                diff = mirror_line - angle.Simplify();
            }
            return (new Angle(mirror_line + diff, AngleType.Radians)).Simplify();
        }
    }

    public enum AngleType
    {
        Degrees,
        Radians
    }
}
