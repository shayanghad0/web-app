import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit,
    QAction, QStatusBar, QProgressBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Programer Panel MeherSaz Pars | پنل برنامه نویسی مهر‍‍ساز پارس')
        self.setGeometry(100, 100, 1024, 768)

        # --- Web View ---
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # --- Navigation Toolbar ---
        self.navbar = QToolBar('Navigation')
        self.addToolBar(self.navbar)

        # Back button
        back_btn = QAction('◀', self)
        back_btn.triggered.connect(self.browser.back)
        self.navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction('▶', self)
        forward_btn.triggered.connect(self.browser.forward)
        self.navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction('⟳', self)
        reload_btn.triggered.connect(self.browser.reload)
        self.navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction('🏠', self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # --- Status Bar with Progress ---
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.progress = QProgressBar()
        self.progress.setMaximumWidth(120)
        self.progress.setVisible(False)
        self.status.addPermanentWidget(self.progress)

        # --- Connect Web Signals ---
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.titleChanged.connect(self.update_title)
        self.browser.loadProgress.connect(self.progress.setValue)
        self.browser.loadStarted.connect(lambda: self.progress.setVisible(True))
        self.browser.loadFinished.connect(lambda: self.progress.setVisible(False))

        # --- Set default home page ---
        self.home_url = QUrl("https://MeherSazPars.ir")
        self.navigate_home()

    def navigate_home(self):
        """Go to the default home page."""
        self.browser.setUrl(self.home_url)

    def navigate_to_url(self):
        """Navigate to the URL typed in the address bar."""
        text = self.url_bar.text().strip()
        if not text:
            return
        # If no scheme is provided, assume https
        if not text.startswith(('http://', 'https://')):
            text = 'https://' + text
        self.browser.setUrl(QUrl(text))

    def update_url_bar(self, url):
        """Update the address bar when the page changes."""
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)

    def update_title(self, title):
        """Update the window title with the page title."""
        base_title = 'Programer Panel MeherSaz Pars | پنل برنامه نویسی مهر‍‍ساز پارس'
        self.setWindowTitle(f'{title} - {base_title}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
