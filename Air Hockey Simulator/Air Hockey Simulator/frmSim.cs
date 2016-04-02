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
    public partial class frmSim : Form
    {
        AirHockeySimCtrl ctrl = new AirHockeySimCtrl();

        public frmSim() {
            InitializeComponent();
            ctrl.Dock = DockStyle.Fill;
            this.Controls.Add(ctrl);
        }

        protected override void OnClosing(CancelEventArgs e) {
            ctrl.tm.Stop();
            base.OnClosing(e);
        }

        private void button1_Click(object sender, EventArgs e) {
            ctrl.Puck.Radius = 0.13175;
        }

        private void button2_Click(object sender, EventArgs e) {
            ctrl.Puck.Radius = 0.03175;
        }

        private void button3_Click(object sender, EventArgs e) {
            ctrl.Puck.Velocity.Speed += 2.30 / 1000;
        }
    }
}
