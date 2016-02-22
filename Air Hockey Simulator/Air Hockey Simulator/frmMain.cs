using Air_Hockey_Simulator.Physics;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Air_Hockey_Simulator
{
    public partial class frmMain : Form
    {
        MicroTimer tm = new MicroTimer();
        DateTime last = DateTime.Now;

        public delegate void OnUpdate(string s);
        OnUpdate Update;

        public frmMain() {
            InitializeComponent();
            Update = Output; //Used to support calling Output() from a different thread.

            Angle angle = new Angle(60, AngleType.Degrees);
            Line line = new Line(new PointD(0, 0), angle);
            Arc arc = new Arc(new PointD(0, 0), 2);

            PointD[] intersections = line.IntersectionWith(arc);
            foreach (var point in intersections)
            {
                Output(point.ToString());
            }

            //tm.Interval = 1000 * 1000;
            //tm.MicroTimerElapsed += Tm_MicroTimerElapsed;
            //tm.Start();
        }

        private void Tm_MicroTimerElapsed(object sender, MicroTimerEventArgs timerEventArgs) {
            Output((DateTime.Now - last).TotalMilliseconds.ToString());
            last = DateTime.Now;
        }

        public void Output(string s) {
            if (!InvokeRequired)
                txOutput.Text += s + "\r\n";
            else
                this.Invoke(Update, s);
        }

        private void button1_Click(object sender, EventArgs e) {
            frmSim sim = new frmSim();
            sim.ShowDialog();
        }
    }
}
