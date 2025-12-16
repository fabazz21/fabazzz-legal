"""
Timeline Panel
Animation timeline with playback controls
"""

import imgui


class TimelinePanel:
    """Timeline panel for animation"""

    def __init__(self, ui):
        """Initialize timeline panel"""
        self.ui = ui

    def render(self):
        """Render timeline panel"""
        imgui.set_next_window_size(800, 200, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(560, 860, imgui.FIRST_USE_EVER)

        expanded, opened = imgui.begin("Timeline", True)
        if not opened:
            self.ui.show_timeline_panel = False
            imgui.end()
            return

        if expanded:
            timeline = self.ui.app.timeline

            # Playback controls
            imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (8, 4))

            # Play/Pause button
            if timeline.playing:
                if imgui.button("⏸ Pause"):
                    timeline.pause()
            else:
                if imgui.button("▶ Play"):
                    timeline.play()

            imgui.same_line()

            # Stop button
            if imgui.button("⏹ Stop"):
                timeline.stop()

            imgui.same_line()

            # Record button
            if timeline.recording:
                imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.2, 0.2)
                if imgui.button("⏺ Stop Recording"):
                    timeline.stop_recording()
                imgui.pop_style_color()
            else:
                if imgui.button("⏺ Record"):
                    timeline.start_recording()

            imgui.pop_style_var()

            imgui.same_line()
            imgui.spacing()
            imgui.same_line()

            # Loop checkbox
            changed, timeline.loop = imgui.checkbox("Loop", timeline.loop)

            imgui.same_line()

            # Playback speed
            changed, timeline.playback_speed = imgui.slider_float(
                "Speed", timeline.playback_speed, 0.1, 4.0, "%.1fx"
            )

            # Time display
            imgui.separator()
            imgui.text(f"Time: {timeline.current_time:.2f}s / {timeline.duration:.2f}s")
            imgui.same_line(imgui.get_window_width() - 150)
            imgui.text(f"Progress: {timeline.get_progress()*100:.1f}%%")

            # Timeline scrubber
            changed, progress = imgui.slider_float(
                "##timeline_scrubber",
                timeline.get_progress(),
                0.0, 1.0,
                ""
            )
            if changed:
                timeline.set_progress(progress)

            # Duration control
            changed, timeline.duration = imgui.slider_float(
                "Duration", timeline.duration, 1.0, 300.0, "%.1fs"
            )

            imgui.separator()

            # Keyframes
            if imgui.collapsing_header("Keyframes", imgui.TREE_NODE_DEFAULT_OPEN)[0]:
                keyframes = timeline.get_all_keyframes()

                if len(keyframes) == 0:
                    imgui.text_colored("No keyframes", 0.6, 0.6, 0.6)
                    imgui.text_colored("Select an object and press 'K' to add keyframe", 0.5, 0.5, 0.5)
                else:
                    imgui.text(f"Total keyframes: {len(keyframes)}")

                    # Keyframe list
                    if imgui.begin_child("keyframe_list", 0, 100, border=True):
                        for i, kf in enumerate(keyframes):
                            target_name = kf.target.name if hasattr(kf.target, 'name') else str(kf.target)

                            if imgui.selectable(
                                f"[{kf.time:.2f}s] {target_name}.{kf.property_name} = {kf.value}",
                                False
                            )[0]:
                                # Seek to keyframe time
                                timeline.seek(kf.time)

                            # Context menu
                            if imgui.begin_popup_context_item(f"ctx_kf_{i}"):
                                if imgui.selectable("Go to Time")[0]:
                                    timeline.seek(kf.time)

                                if imgui.selectable("Delete Keyframe")[0]:
                                    timeline.remove_keyframe(kf)

                                imgui.separator()

                                # Easing submenu
                                if imgui.begin_menu("Change Easing"):
                                    from ...animation.easing import get_easing_names
                                    for easing_name in get_easing_names():
                                        if imgui.selectable(easing_name)[0]:
                                            kf.easing = easing_name
                                    imgui.end_menu()

                                imgui.end_popup()

                        imgui.end_child()

                    # Add keyframe button
                    if imgui.button("Add Keyframe (K)"):
                        if self.ui.selected_object or self.ui.selected_projector:
                            obj = self.ui.selected_object or self.ui.selected_projector
                            timeline.add_keyframe(obj, 'position')
                        else:
                            print("  ⚠️ No object selected")

                    imgui.same_line()

                    if imgui.button("Clear All Keyframes"):
                        timeline.clear_animation()

            # Animation clips
            if imgui.collapsing_header("Animation Clips")[0]:
                if len(timeline.clips) == 0:
                    imgui.text_colored("No animation clips", 0.6, 0.6, 0.6)
                else:
                    for i, clip in enumerate(timeline.clips):
                        is_active = (timeline.active_clip == clip)

                        if imgui.selectable(
                            f"{'[ACTIVE] ' if is_active else ''}{clip.name}",
                            is_active
                        )[0]:
                            timeline.set_active_clip(clip)

                        # Context menu
                        if imgui.begin_popup_context_item(f"ctx_clip_{i}"):
                            if imgui.selectable("Rename")[0]:
                                # TODO: Rename dialog
                                pass

                            if imgui.selectable("Delete")[0]:
                                timeline.remove_clip(clip)

                            imgui.end_popup()

                if imgui.button("New Animation Clip"):
                    timeline.create_clip(f"Animation {len(timeline.clips) + 1}")

        imgui.end()
