"""
Script de capture automatique pour projector_TIMELINE_PROJECTOR_FIX_2.html
Ouvre le HTML, clique sur chaque fonction et capture des screenshots
"""

import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class HTMLFunctionCapture:
    def __init__(self, html_path, output_dir="html_captures"):
        """
        Initialize the capture tool

        Args:
            html_path: Path to the HTML file
            output_dir: Directory to save screenshots
        """
        self.html_path = Path(html_path).absolute()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        # Uncomment to run in headless mode:
        # chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        self.screenshot_count = 0

    def open_html(self):
        """Open the HTML file in browser"""
        file_url = f"file:///{self.html_path.as_posix()}"
        print(f"📂 Opening: {file_url}")
        self.driver.get(file_url)
        time.sleep(3)  # Wait for page to load

    def take_screenshot(self, name):
        """Take a screenshot with given name"""
        self.screenshot_count += 1
        filename = f"{self.screenshot_count:03d}_{name}.png"
        filepath = self.output_dir / filename
        self.driver.save_screenshot(str(filepath))
        print(f"  📸 Captured: {filename}")
        return filepath

    def click_and_capture(self, element, name, wait_after=1):
        """Click element and capture screenshot"""
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)

            # Try to click
            try:
                element.click()
            except ElementClickInterceptedException:
                # Try JavaScript click if normal click fails
                self.driver.execute_script("arguments[0].click();", element)

            time.sleep(wait_after)
            self.take_screenshot(name)
            return True

        except Exception as e:
            print(f"  ⚠️  Failed to click {name}: {e}")
            return False

    def capture_initial_state(self):
        """Capture initial state of the application"""
        print("\n🎬 Capturing initial state...")
        self.take_screenshot("000_initial_state")

    def capture_gizmo_modes(self):
        """Capture all gizmo modes (Move, Rotate, Scale)"""
        print("\n🎯 Capturing Gizmo Modes...")

        gizmo_buttons = [
            ("gizmo-move-btn-top", "gizmo_move_mode"),
            ("gizmo-rotate-btn-top", "gizmo_rotate_mode"),
            ("gizmo-scale-btn-top", "gizmo_scale_mode"),
        ]

        for btn_id, name in gizmo_buttons:
            try:
                btn = self.driver.find_element(By.ID, btn_id)
                self.click_and_capture(btn, name)
            except Exception as e:
                print(f"  ⚠️  Could not find {btn_id}: {e}")

    def capture_panels(self):
        """Capture all collapsible panels"""
        print("\n📋 Capturing Panels...")

        panels = self.driver.find_elements(By.CLASS_NAME, "collapsible-panel")

        for i, panel in enumerate(panels):
            try:
                panel_id = panel.get_attribute("id")
                panel_name = panel_id.replace("panel-", "") if panel_id else f"panel_{i}"

                # Click panel header to expand
                header = panel.find_element(By.CLASS_NAME, "panel-header")
                self.click_and_capture(header, f"panel_{panel_name}_open", wait_after=0.5)

            except Exception as e:
                print(f"  ⚠️  Could not capture panel {i}: {e}")

    def capture_menu_items(self):
        """Capture top menu items"""
        print("\n📑 Capturing Menu Items...")

        # Try to find and click menu items
        menu_selectors = [
            ('id', 'undo-btn', 'menu_undo'),
            ('id', 'redo-btn', 'menu_redo'),
        ]

        for selector_type, selector_value, name in menu_selectors:
            try:
                if selector_type == 'id':
                    element = self.driver.find_element(By.ID, selector_value)
                elif selector_type == 'class':
                    element = self.driver.find_element(By.CLASS_NAME, selector_value)

                # Just capture the menu, don't always click (some might be disabled)
                self.take_screenshot(f"menu_{name}")

            except Exception as e:
                print(f"  ⚠️  Could not find {name}: {e}")

    def capture_buttons(self):
        """Capture all button interactions"""
        print("\n🔘 Capturing Buttons...")

        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        captured_buttons = set()

        for i, button in enumerate(buttons):
            try:
                btn_id = button.get_attribute("id")
                btn_text = button.text.strip()
                onclick = button.get_attribute("onclick")

                # Generate unique name
                if btn_id and btn_id not in captured_buttons:
                    name = f"button_{btn_id}"
                    captured_buttons.add(btn_id)
                elif btn_text:
                    name = f"button_{btn_text.replace(' ', '_')[:30]}"
                elif onclick:
                    func_name = onclick.split('(')[0]
                    name = f"button_{func_name}"
                else:
                    name = f"button_{i}"

                # Check if visible and enabled
                if button.is_displayed() and button.is_enabled():
                    self.click_and_capture(button, name, wait_after=0.8)

            except Exception as e:
                pass  # Skip buttons that can't be clicked

    def capture_tabs(self):
        """Capture different tabs if they exist"""
        print("\n📑 Capturing Tabs...")

        tabs = self.driver.find_elements(By.CSS_SELECTOR, "[data-tab], .tab, .tab-button")

        for i, tab in enumerate(tabs):
            try:
                tab_name = tab.get_attribute("data-tab") or tab.text.strip() or f"tab_{i}"
                if tab.is_displayed():
                    self.click_and_capture(tab, f"tab_{tab_name}", wait_after=0.5)
            except Exception as e:
                pass

    def capture_all(self):
        """Run complete capture sequence"""
        try:
            self.open_html()

            # Capture sequence
            self.capture_initial_state()
            self.capture_gizmo_modes()
            self.capture_panels()
            self.capture_tabs()
            self.capture_menu_items()
            self.capture_buttons()

            print(f"\n✅ Capture complete! {self.screenshot_count} screenshots saved to: {self.output_dir}")

        except Exception as e:
            print(f"\n❌ Error during capture: {e}")
            import traceback
            traceback.print_exc()

        finally:
            # Keep browser open for 3 seconds before closing
            time.sleep(3)
            self.driver.quit()
            print("\n👋 Browser closed")

def main():
    """Main function"""
    # Configuration
    HTML_FILE = "projector_TIMELINE_PROJECTOR_FIX_2.html"
    OUTPUT_DIR = "html_function_captures"

    print("=" * 60)
    print("  HTML FUNCTION AUTO-CAPTURE")
    print("=" * 60)
    print(f"📄 HTML File: {HTML_FILE}")
    print(f"📁 Output Directory: {OUTPUT_DIR}")
    print("=" * 60)

    # Check if HTML exists
    if not Path(HTML_FILE).exists():
        print(f"❌ Error: {HTML_FILE} not found!")
        print(f"   Place this script in the same folder as {HTML_FILE}")
        return

    # Run capture
    capturer = HTMLFunctionCapture(HTML_FILE, OUTPUT_DIR)
    capturer.capture_all()

    print("\n" + "=" * 60)
    print("  DONE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
