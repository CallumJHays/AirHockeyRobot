using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Air_Hockey_Simulator.Physics
{
    public static class Physics
    {
        public static bool energy_loss_enabled = true;

        public static InformationPacket Update(Puck p, Puck c, Table table, double delta_time) {
            double offset = p.Velocity.Speed * delta_time;
            double x = offset * Math.Cos(p.Velocity.Direction);
            double y = offset * Math.Sin(p.Velocity.Direction);
            PointD ghost_puck_location = p.Location.Offset(x, y);

            //Collect debugging information as we loop through the collision algorithm
            InformationPacket info = new InformationPacket();
            info.Points.Add(ghost_puck_location);

            //Collision correction
            CollisionData data;
            while ((data = GetClosestCollisionData(p, offset, ghost_puck_location, c, table)) != null) {     
                p.Location = data.collision_point;
                p.Velocity.Direction = p.Velocity.Direction.Reflect(data.projection_line.Perpendicular(data.collision_point).Angle) + Angle._180;

                PointD translation_reflection_point = data.projection_line.IntersectionWith(data.projection_line.Perpendicular(ghost_puck_location));
                ghost_puck_location = translation_reflection_point.Offset(translation_reflection_point.X - ghost_puck_location.X, translation_reflection_point.Y - ghost_puck_location.Y);
                offset = ghost_puck_location.DistanceTo(p.Location);

                if (energy_loss_enabled)
                    p.Velocity.Speed *= .8;

                info.Points.Add(ghost_puck_location);
            }

            //Shazam (physics calculations are complete)
            p.Location = ghost_puck_location;

            if (energy_loss_enabled) {
                p.Velocity.Speed -= delta_time * table.Friction;
                if (p.Velocity.Speed < 0) { p.Velocity.Speed = 0; }
            }

            return info;
        }

        public static CollisionData GetClosestCollisionData(Puck p, double offset, PointD ghost_puck_location, Puck c, Table table) {
            List<Line> collision_lines = new List<Line>();
            collision_lines.AddRange(table.Walls);

            for (int j = 0; j < table.Arcs.Count; ++j)
            {
                PointD[] center_point_collisions = p.Path.IntersectionWith(table.Arcs[j]);
                if (center_point_collisions != null)
                {
                    for (int i = 0; i < center_point_collisions.Length; ++i)
                    {
                        if (center_point_collisions[i] != null)
                        {
                            Line line_thru_center = new Line(table.Arcs[j].Point, (double?)((center_point_collisions[i].Y - table.Arcs[j].Point.Y) / (center_point_collisions[i].X - table.Arcs[j].Point.X)));
                            Line projection_line = line_thru_center.Perpendicular(center_point_collisions[i]);
                            collision_lines.Add(projection_line);
                        }
                    }
                }
            }

            List<CollisionData> potential_collision_points = new List<CollisionData>();
            for (int j = 0; j < collision_lines.Count; ++j) {
                PointD center_point_collision = p.Path.IntersectionWith(collision_lines[j]);
                if (center_point_collision != null) {
                    double sc = p.Location.DistanceTo(center_point_collision);
                    double fc = ghost_puck_location.DistanceTo(center_point_collision);
                    if (!(fc > sc && fc > offset)) {
                        Line projection_line = ProjectionLine(p, collision_lines[j]);
                        PointD projection_collision = p.Path.IntersectionWith(projection_line);
                        if (offset > projection_collision.DistanceTo(p.Location)) {
                            potential_collision_points.Add(new CollisionData(projection_collision, projection_line));
                        }
                    }
                }
            }

            //TODO: check for collision with computer puck, add result to potential collision points right here
            //for (int j = 0; j < table.Arcs.Count; ++j)
            //{
            //    Arc projection_arc = p.Location.DistanceTo(table.Arcs[j].Point) < table.Arcs[j].Radius
            //        ? new Arc(table.Arcs[j].Point, table.Arcs[j].Radius - p.Radius)
            //        : new Arc(table.Arcs[j].Point, table.Arcs[j].Radius + p.Radius);
            //
            //    PointD[] center_point_collisions = p.Path.IntersectionWith(table.Arcs[j]);
            //    if (center_point_collisions != null)
            //    {
            //        for (int i = 0; i < center_point_collisions.Length; ++i)
            //        {
            //            if (center_point_collisions[i] != null)
            //            {
            //                double sc = p.Location.DistanceTo(center_point_collisions[i]);
            //                double fc = ghost_puck_location.DistanceTo(center_point_collisions[i]);
            //                if (!(fc > sc && fc > offset))
            //                {
            //                    PointD[] projection_collisions = p.Path.IntersectionWith(projection_arc);
            //                    foreach (var projection_collision in projection_collisions)
            //                    {
            //                        Line line_thru_center = new Line(table.Arcs[j].Point, (double?)((projection_collision.Y - projection_arc.Point.Y) / (projection_collision.X - projection_arc.Point.X)));
            //                        Line projection_line = line_thru_center.Perpendicular(projection_collision);
            //                        if (offset > projection_collision.DistanceTo(p.Location)) {
            //                            potential_collision_points.Add(new CollisionData(projection_collision, projection_line));
            //                        }
            //                    }
            //                }
            //            }
            //        }
            //    }
            //}

            potential_collision_points = potential_collision_points.OrderBy(z => z.collision_point.DistanceTo(p.Location)).ToList();
            return potential_collision_points.Count > 0 ? potential_collision_points[0] : null;
        }

        public static Line ProjectionLine(Puck p, Line reference) {
            PointD ij = reference.IntersectionWith(reference.Perpendicular(p.Location));
            double dist = p.Location.DistanceTo(ij);
            double scale = p.Radius / dist;
            PointD projection_line_point = ij.Offset((p.Location.X - ij.X) * scale, (p.Location.Y - ij.Y) * scale);
            return reference.Parallel(projection_line_point);
        }
    }

    /// <summary>
    /// Potential Todo: Just use a line class instead, with the point of the line set to the collision point?
    /// </summary>
    public class CollisionData
    {
        public PointD collision_point { get; set; }
        public Line projection_line { get; set; }

        public CollisionData(PointD cp, Line pl) {
            collision_point = cp; projection_line = pl;
        }
    }

    public class InformationPacket
    {
        public List<PointD> Points = new List<PointD>();
        public List<Line> Lines = new List<Line>();

        public InformationPacket() {
            
        }
    }
}
