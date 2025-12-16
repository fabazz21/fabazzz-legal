"""
Export Utilities
Export renders, videos, PDFs, and project data
"""

import os
import json
from datetime import datetime
from PIL import Image
import numpy as np


class ImageExporter:
    """Export rendered images"""

    @staticmethod
    def export_framebuffer(ctx, width, height, filepath, format='PNG'):
        """
        Export current framebuffer to image

        Args:
            ctx: ModernGL context
            width: Image width
            height: Image height
            filepath: Output file path
            format: Image format (PNG, JPEG, TIFF, EXR)
        """
        # Read pixels from framebuffer
        pixels = ctx.screen.read(components=3)

        # Convert to PIL Image
        img = Image.frombytes('RGB', (width, height), pixels)

        # Flip vertically (OpenGL origin is bottom-left)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        # Save
        img.save(filepath, format=format)

        print(f"  ✅ Exported image: {filepath} ({width}x{height})")

    @staticmethod
    def export_render(renderer, scene, camera, width, height, filepath, format='PNG'):
        """
        Render and export scene to image

        Args:
            renderer: Renderer instance
            scene: Scene to render
            camera: Camera viewpoint
            width: Render width
            height: Render height
            filepath: Output file path
            format: Image format
        """
        # TODO: Implement off-screen rendering at custom resolution
        print(f"  ⚠️ Custom resolution rendering not yet implemented")
        print(f"     Will export current viewport")

        # For now, export current framebuffer
        ImageExporter.export_framebuffer(renderer.ctx, width, height, filepath, format)


class VideoExporter:
    """Export animation to video"""

    @staticmethod
    def export_video(renderer, scene, camera, timeline, output_path, fps=30, width=1920, height=1080):
        """
        Export timeline animation to video

        Args:
            renderer: Renderer instance
            scene: Scene to render
            camera: Camera viewpoint
            timeline: Timeline with animation
            output_path: Output video file path
            fps: Frames per second
            width: Video width
            height: Video height
        """
        try:
            import cv2
        except ImportError:
            print("  ⚠️ OpenCV not installed. Cannot export video.")
            print("     Install with: pip install opencv-python")
            return

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Calculate frame count
        duration = timeline.duration
        frame_count = int(duration * fps)

        print(f"  🎬 Exporting video: {frame_count} frames at {fps}fps")

        # Render each frame
        for frame in range(frame_count):
            time = frame / fps

            # Update timeline
            timeline.seek(time)

            # Render scene
            renderer.render_scene(scene, camera)

            # Read framebuffer
            pixels = renderer.ctx.screen.read(components=3)

            # Convert to numpy array
            frame_data = np.frombuffer(pixels, dtype=np.uint8)
            frame_data = frame_data.reshape((height, width, 3))

            # Flip vertically
            frame_data = np.flipud(frame_data)

            # Convert RGB to BGR (OpenCV format)
            frame_data = cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR)

            # Write frame
            video_writer.write(frame_data)

            # Progress
            if frame % 30 == 0:
                progress = (frame / frame_count) * 100
                print(f"     Progress: {progress:.1f}%")

        # Release video writer
        video_writer.release()

        print(f"  ✅ Video exported: {output_path}")


class PDFExporter:
    """Export technical reports as PDF"""

    @staticmethod
    def export_technical_report(scene, projectors, output_path):
        """
        Export technical report with scene configuration

        Args:
            scene: Scene instance
            projectors: List of projectors
            output_path: Output PDF file path
        """
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.units import inch
            from reportlab.pdfgen import canvas
            from reportlab.lib import colors
        except ImportError:
            print("  ⚠️ ReportLab not installed. Cannot export PDF.")
            print("     Install with: pip install reportlab")
            return

        # Create PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        # Title page
        c.setFont("Helvetica-Bold", 24)
        c.drawString(1*inch, height - 2*inch, "Projection Mapping")
        c.drawString(1*inch, height - 2.5*inch, "Technical Report")

        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 3*inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Project information
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, "Project Information")

        c.setFont("Helvetica", 12)
        y = height - 1.5*inch

        c.drawString(1*inch, y, f"Number of projectors: {len(projectors)}")
        y -= 0.3*inch
        c.drawString(1*inch, y, f"Number of objects: {len(scene.objects)}")
        y -= 0.3*inch
        c.drawString(1*inch, y, f"Number of lights: {len(scene.lights)}")

        # Projector specifications
        for i, proj in enumerate(projectors):
            c.showPage()
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1*inch, height - 1*inch, f"Projector {i+1}: {proj.name}")

            c.setFont("Helvetica", 12)
            y = height - 1.5*inch

            specs = [
                f"Model: {proj.config['name']}",
                f"Brightness: {proj.config['lumens']:,} lumens",
                f"Resolution: {proj.config['resolution']}",
                f"Aspect Ratio: {proj.config['aspect']:.2f}:1",
                f"",
                f"Lens: {proj.lens_config['name']}",
                f"Throw Ratio: {proj.throw_ratio:.2f}:1",
                f"FOV: {proj.get_fov():.1f}°",
                f"",
                f"Position: ({proj.position[0]:.2f}, {proj.position[1]:.2f}, {proj.position[2]:.2f})",
                f"Intensity: {proj.intensity:.2f}",
                f"",
                f"Lens Shift H: {proj.lens_shift_h:.3f}",
                f"Lens Shift V: {proj.lens_shift_v:.3f}",
                f"Keystone H: {proj.keystone_h:.1f}",
                f"Keystone V: {proj.keystone_v:.1f}",
            ]

            for spec in specs:
                c.drawString(1*inch, y, spec)
                y -= 0.25*inch

        # Save PDF
        c.save()

        print(f"  ✅ PDF report exported: {output_path}")


class ProjectExporter:
    """Export/Import project data"""

    @staticmethod
    def export_project_json(scene, timeline, output_path):
        """
        Export project as JSON

        Args:
            scene: Scene instance
            timeline: Timeline instance
            output_path: Output JSON file path
        """
        project_data = {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'scene': ProjectExporter._serialize_scene(scene),
            'timeline': ProjectExporter._serialize_timeline(timeline)
        }

        with open(output_path, 'w') as f:
            json.dump(project_data, f, indent=2)

        print(f"  ✅ Project exported: {output_path}")

    @staticmethod
    def _serialize_scene(scene):
        """Serialize scene to dictionary"""
        return {
            'objects': [
                {
                    'id': obj.id,
                    'name': obj.name,
                    'type': type(obj).__name__,
                    'position': list(obj.position),
                    'scale': list(obj.scale),
                    'visible': obj.visible,
                    'color': obj.color if hasattr(obj, 'color') else None
                }
                for obj in scene.objects
            ],
            'projectors': [
                {
                    'id': proj.id,
                    'name': proj.name,
                    'model_id': proj.model_id,
                    'lens_id': proj.lens_id,
                    'position': list(proj.position),
                    'throw_ratio': proj.throw_ratio,
                    'lens_shift_h': proj.lens_shift_h,
                    'lens_shift_v': proj.lens_shift_v,
                    'keystone_h': proj.keystone_h,
                    'keystone_v': proj.keystone_v,
                    'intensity': proj.intensity,
                    'active': proj.active
                }
                for proj in scene.projectors
            ]
        }

    @staticmethod
    def _serialize_timeline(timeline):
        """Serialize timeline to dictionary"""
        return {
            'duration': timeline.duration,
            'current_time': timeline.current_time,
            'loop': timeline.loop,
            'playback_speed': timeline.playback_speed,
            'clips': [
                {
                    'name': clip.name,
                    'duration': clip.duration,
                    'keyframes': [
                        {
                            'time': kf.time,
                            'target_id': id(kf.target),
                            'property': kf.property_name,
                            'value': str(kf.value),
                            'easing': kf.easing
                        }
                        for kf in clip.get_all_keyframes()
                    ]
                }
                for clip in timeline.clips
            ]
        }

    @staticmethod
    def export_project_zip(scene, timeline, output_path):
        """
        Export complete project as ZIP archive

        Args:
            scene: Scene instance
            timeline: Timeline instance
            output_path: Output ZIP file path
        """
        import zipfile
        import tempfile

        with zipfile.ZipFile(output_path, 'w') as zipf:
            # Export project JSON
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp:
                temp_path = temp.name
                ProjectExporter.export_project_json(scene, timeline, temp_path)

            # Add to ZIP
            zipf.write(temp_path, 'project.json')
            os.unlink(temp_path)

            # TODO: Add textures, models, etc.

        print(f"  ✅ Project ZIP exported: {output_path}")
