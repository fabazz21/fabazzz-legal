"""
Script de capture automatique AMÉLIORÉ avec installation automatique de ChromeDriver
Version simplifiée - installation automatique de tous les drivers
"""

import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException

try:
    from webdriver_manager.chrome import ChromeDriverManager
    AUTO_DRIVER = True
except ImportError:
    AUTO_DRIVER = False
    print("⚠️  webdriver-manager non installé. Installation manuelle requise.")
    print("   Pour installer: pip install webdriver-manager")

class HTMLFunctionCapture:
    def __init__(self, html_path, output_dir="html_captures"):
        self.html_path = Path(html_path).absolute()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Initialize driver with auto-installation if available
        if AUTO_DRIVER:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.wait = WebDriverWait(self.driver, 10)
        self.screenshot_count = 0

    def open_html(self):
        """Open the HTML file in browser"""
        file_url = f"file:///{self.html_path.as_posix()}"
        print(f"\n📂 Opening: {file_url}")
        self.driver.get(file_url)
        time.sleep(3)
        self.take_screenshot("000_initial_load")

    def take_screenshot(self, name):
        """Take a screenshot"""
        self.screenshot_count += 1
        filename = f"{self.screenshot_count:03d}_{name}.png"
        filepath = self.output_dir / filename
        self.driver.save_screenshot(str(filepath))
        print(f"  📸 {filename}")
        return filepath

    def safe_click(self, element, name, wait_after=1):
        """Safely click an element"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)

            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)

            time.sleep(wait_after)
            self.take_screenshot(name)
            return True
        except Exception as e:
            print(f"  ⚠️  {name}: {str(e)[:50]}")
            return False

    def capture_by_id(self, element_id, name, wait_after=1):
        """Capture element by ID"""
        try:
            element = self.driver.find_element(By.ID, element_id)
            if element.is_displayed():
                return self.safe_click(element, name, wait_after)
        except:
            pass
        return False

    def capture_gizmos(self):
        """Capture gizmo modes"""
        print("\n🎯 Gizmo Modes:")
        self.capture_by_id("gizmo-move-btn-top", "gizmo_move")
        self.capture_by_id("gizmo-rotate-btn-top", "gizmo_rotate")
        self.capture_by_id("gizmo-scale-btn-top", "gizmo_scale")

    def capture_panels(self):
        """Capture all panels"""
        print("\n📋 Panels:")
        panels = self.driver.find_elements(By.CLASS_NAME, "collapsible-panel")

        for panel in panels:
            try:
                panel_id = panel.get_attribute("id") or "unknown"
                name = panel_id.replace("panel-", "panel_")

                header = panel.find_element(By.CLASS_NAME, "panel-header")
                self.safe_click(header, name)
            except:
                pass

    def capture_all_buttons(self):
        """Capture all visible buttons"""
        print("\n🔘 Buttons:")
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        captured = set()

        for button in buttons:
            try:
                if not button.is_displayed() or not button.is_enabled():
                    continue

                btn_id = button.get_attribute("id")
                btn_text = button.text.strip()[:20]
                onclick = button.get_attribute("onclick")

                # Generate name
                if btn_id and btn_id not in captured:
                    name = f"btn_{btn_id}"
                    captured.add(btn_id)
                elif onclick:
                    func = onclick.split('(')[0]
                    name = f"btn_{func}"
                elif btn_text:
                    name = f"btn_{btn_text.replace(' ', '_')}"
                else:
                    continue

                self.safe_click(button, name, wait_after=0.5)

            except:
                pass

    def capture_menus(self):
        """Capture menu items"""
        print("\n📑 Menus:")

        menu_items = self.driver.find_elements(By.CSS_SELECTOR, "[id*='menu'], [class*='menu-item']")

        for item in menu_items:
            try:
                if item.is_displayed():
                    item_id = item.get_attribute("id") or item.text.strip()[:20]
                    self.safe_click(item, f"menu_{item_id}", wait_after=0.3)
            except:
                pass

    def capture_all(self):
        """Run complete capture"""
        try:
            print("=" * 60)
            print("  🎬 DÉMARRAGE DE LA CAPTURE")
            print("=" * 60)

            self.open_html()

            # Sequence
            self.capture_gizmos()
            self.capture_panels()
            self.capture_menus()
            self.capture_all_buttons()

            print("\n" + "=" * 60)
            print(f"  ✅ TERMINÉ! {self.screenshot_count} captures")
            print(f"  📁 Dossier: {self.output_dir}")
            print("=" * 60)

        except KeyboardInterrupt:
            print("\n\n⏸️  Capture interrompue par l'utilisateur")

        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

        finally:
            print("\n⏳ Fermeture du navigateur dans 3 secondes...")
            time.sleep(3)
            self.driver.quit()

def main():
    HTML_FILE = "projector_TIMELINE_PROJECTOR_FIX_2.html"
    OUTPUT_DIR = "html_function_captures"

    print("\n🚀 HTML FUNCTION AUTO-CAPTURE v2.0")
    print(f"📄 Fichier: {HTML_FILE}")
    print(f"📁 Sortie: {OUTPUT_DIR}\n")

    if not Path(HTML_FILE).exists():
        print(f"❌ ERREUR: {HTML_FILE} introuvable!")
        print(f"   Placez ce script dans le même dossier que le HTML\n")
        return

    capturer = HTMLFunctionCapture(HTML_FILE, OUTPUT_DIR)
    capturer.capture_all()

if __name__ == "__main__":
    main()
