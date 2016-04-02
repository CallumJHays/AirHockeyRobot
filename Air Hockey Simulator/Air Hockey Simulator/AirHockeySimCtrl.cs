using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Air_Hockey_Simulator.Physics;

namespace Air_Hockey_Simulator
{
    public partial class AirHockeySimCtrl : UserControl
    {
        #region Parts
        public Table Table { get; set; }
        public Puck Puck { get; set; }
        public Arm Robot { get; set; }
        #endregion

        #region Essential Drawing Varibles
        const int padding_top = 100;
        static Matrix flip_vertically = new Matrix(1, 0, 0, -1, 0, 0);
        double scale = 1;

        Pen p_thick_black = new Pen(Color.Black, 3);
        Pen p_thick_green = new Pen(Color.Green, 2);
        Pen p_thick_purple = new Pen(Color.Purple, 2);
        #endregion

        #region Refresh Timer
        DateTime lastGUIUpdate = DateTime.Now;
        public MicroTimer tm = new MicroTimer();
        public delegate void OnUpdate();
        OnUpdate Updated;
        #endregion

        #region Debugging
        List<InformationPacket> debugging_packets = new List<InformationPacket>();
        bool debug_break = false;

        public Pen getFromInt(int i) {
            switch (i) {
                case 0:
                    return Pens.Black;
                case 1:
                    return Pens.Blue;
                case 2:
                    return Pens.Red;
                case 3:
                    return Pens.Green;
                default:
                    return Pens.LightGray;
            }
        }
        #endregion

        List<double> times = new List<double>();

        #region Initialization
        public AirHockeySimCtrl() {
            InitializeComponent();
            this.ResizeRedraw = true;
            Init();
        }

        public void Init() {
            Table = new Table();
            Robot = new Arm();
            Puck = new Puck();

            #region Physical Defaults
            Table.Height = 1.987; //198.7 cm, or 8 feet
            Table.Width = 0.965;
            Line Left_Side = new Line(new PointD(0, 0), new Angle(90, AngleType.Degrees));
            Line Right_Side = new Line(new PointD(Table.Width, 0), new Angle(90, AngleType.Degrees));
            Line Light_Side = new Line(new PointD(0, Table.Height), new Angle(0.001, AngleType.Degrees));
            Line Dark_Side = new Line(new PointD(0, 0), new Angle(0.001, AngleType.Degrees));
            Table.Walls.Add(Left_Side); Table.Walls.Add(Right_Side); Table.Walls.Add(Light_Side); Table.Walls.Add(Dark_Side);
            Table.Friction = 0.000250 / 1000;
            Table.Goal_Width = .26; //26 cm

            Arc arc_test = new Arc(new PointD(Table.Width, Table.Height / 2), 0.4175);
            Table.Arcs.Add(arc_test);
            Arc arc_test2 = new Arc(new PointD(0, Table.Height / 2), Table.Width);
            Table.Arcs.Add(arc_test2);

            Robot.Arm_Length = .3; //30 cm
            Robot.Arm_Angle = new Angle(90, AngleType.Degrees);
            Robot.Forearm_Length = .3;
            Robot.Forearm_Angle = new Angle(90, AngleType.Degrees);

            Puck.Weight = 18; //18 grams
            Puck.Radius = 0.03175; //The diameter of a standard hockey puck is 6.35 cm
            Puck.Location = new PointD(Table.Width / 2, Table.Height / 2);
            Puck.Velocity.Direction = new Angle(((double)(new Random()).Next(0, 36000) / 100.0), AngleType.Degrees);
            //Puck.Velocity.Speed = 10.30 / 1000;
            #endregion

            //Timer
            Updated = OnUpdated;
            tm.Interval = (1000 * 1000) / 60;
            tm.MicroTimerElapsed += Tm_MicroTimerElapsed;
            tm.Start();
        }
        #endregion

        #region Timer
        private void Tm_MicroTimerElapsed(object sender, MicroTimerEventArgs timerEventArgs) {
            try { this.Invoke(Updated); } catch {  }
        }

        public void OnUpdated() {
            this.Invalidate();
        }
        #endregion

        #region All-important Rendering
        protected override void OnPaint(PaintEventArgs e) {
            Graphics g = e.Graphics;
            double delta_time = (DateTime.Now - lastGUIUpdate).TotalMilliseconds;
            SetupGraphics(g, delta_time.ToString());

            if (!debug_break) {
                //DateTime tm_start = DateTime.Now;
                InformationPacket ip = Physics.Physics.Update(Puck, Puck, Table, delta_time);
                //times.Add((DateTime.Now - tm_start).TotalMilliseconds);
                //if (times.Count == 1000)
                //{
                //    tm.Stop();
                //    MessageBox.Show(times.Average().ToString());
                //}
                debugging_packets.Add(ip);
                if (debugging_packets.Count > 2)
                    debugging_packets.RemoveAt(0);
            }

            if (Puck.Location.X < 0 || Puck.Location.X > Table.Width || Puck.Location.Y < 0 || Puck.Location.Y > Table.Height) {
                tm.Stop();
                debug_break = true;
            }

            g.FillRectangle(Brushes.White, 0, 0, si(Table.Width), si(Table.Height));
            g.DrawRectangle(Pens.Black, 0, 0, si(Table.Width), si(Table.Height));

            foreach (Line w in Table.Walls) {
                DrawLine(g, w, Pens.Black);
            }

            foreach (Arc a in Table.Arcs) {
                DrawArc(g, a, Pens.Black);
            }

            g.FillEllipse(Brushes.Blue, getPuckRectangle(Puck));
            DrawLine(g, Puck.Path, Pens.Red);

            if (debug_break) {
                for (int j = 0; j < debugging_packets.Count; ++j) {
                    for (int i = 0; i < debugging_packets[j].Points.Count; ++i) {
                        g.DrawRectangle(getFromInt(i), s(debugging_packets[j].Points[i].X), s(debugging_packets[j].Points[i].Y), 10, 10);
                    }
                    for (int i = 0; i < debugging_packets[j].Lines.Count; ++i) {
                        DrawLine(g, debugging_packets[j].Lines[i], getFromInt(j));
                    }
                }
            }

            lastGUIUpdate = DateTime.Now;
            base.OnPaint(e);
        }
        #endregion

        #region Rendering Assistance
        public void SetupGraphics(Graphics g, string detail) {
            scale = (double)(this.Height - 2 * padding_top) / Table.Height;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.TranslateTransform((this.Width / 2) - (int)((scale * Table.Width) / 2), this.Height - padding_top);
            g.DrawString(detail, this.Font, Brushes.Black, 0, 10);
            g.MultiplyTransform(flip_vertically);
        }

        public void DrawArc(Graphics g, Arc a, Pen p)
        {
            g.DrawEllipse(p, s(a.Point.X - a.Radius), s(a.Point.Y - a.Radius), s(a.Radius * 2), s(a.Radius * 2));
        }

        public void DrawLine(Graphics g, Line l, Pen p) {
            if (l.Slope == null) {
                g.DrawLine(p, s(l.Point.X), 0, s(l.Point.X), s(Table.Height));
            } else {
                double bottom_x = 0;
                double bottom_y = l.Y(bottom_x).Value;
                if (bottom_y < 0) {
                    bottom_y = 0;
                    bottom_x = l.X(bottom_y).Value;
                }
                double top_x = Table.Width;
                double top_y = l.Y(top_x).Value;
                if (top_y > Table.Height) {
                    top_y = Table.Height;
                    top_x = l.X(top_y).Value;
                }
                try {
                    g.DrawLine(p, s(bottom_x), s(bottom_y), s(top_x), s(top_y));
                } catch {
                    //Somepin' not right. Figure this out later
                }
            }
        }

        private RectangleF getPuckRectangle(Puck p) {
            return new RectangleF(s(p.Location.X - p.Radius), s(p.Location.Y - p.Radius), s(p.Radius * 2), s(p.Radius * 2));
        }

        public float s(double input) { return (float)(scale * input); }
        public int si(double input) { return (int)(scale * input); }
        #endregion
    }
}
