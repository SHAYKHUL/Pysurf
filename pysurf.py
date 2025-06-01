import sys
import json  # Add this import at the top of the file
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

def main():
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL, False)  # Enable software rendering
    QApplication.setApplicationName("Python Web Browser")
    QApplication.setOrganizationName("YourOrganization")
    QApplication.setOrganizationDomain("yourdomain.com")

    # Disable GPU acceleration
    import os
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"

    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())

class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if "ads" in url or "tracker" in url:
            info.block(True)  # Block the request

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_file = "browser_config.json"
        
        # Load configuration
        self.load_config()

        # Set up the browser window
        self.setWindowTitle("Python Web Browser")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon('C:/Users/USER/Documents/khulshay/Web browser/browsericon.png'))  # Update the icon path

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.tab_context_menu)

        # Add new tab button to the tab bar
        self.tabs.setCornerWidget(self.create_new_tab_button(), Qt.TopRightCorner)

        self.setCentralWidget(self.tabs)

        # Create a navigation bar
        navbar = QToolBar()
        navbar.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        self.addToolBar(navbar)

        # Update navigation bar buttons with modern icons
        back_button = QAction(QIcon("icons/back.png"), 'Back', self)
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_button)

        forward_button = QAction(QIcon("icons/forward.png"), 'Forward', self)
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_button)

        reload_button = QAction(QIcon("icons/reload.png"), 'Reload', self)
        reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_button)

        home_button = QAction(QIcon("icons/home.png"), 'Home', self)
        home_button.triggered.connect(self.navigate_home)
        navbar.addAction(home_button)

        stop_button = QAction(QIcon("icons/stop.png"), 'Stop', self)
        stop_button.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navbar.addAction(stop_button)

        # Add address bar
        self.url_bar = QLineEdit(self)
        self.url_bar.setStyleSheet("padding: 5px;")
        self.url_bar.returnPressed.connect(self.load_url_from_address_bar)
        navbar.addWidget(self.url_bar)

        # Add search engine selection
        self.search_engine = QComboBox(self)
        self.search_engine.addItems(["Google", "Bing", "DuckDuckGo"])
        navbar.addWidget(self.search_engine)

        # Add bookmarks button
        bookmarks_button = QAction(self.style().standardIcon(QStyle.SP_FileDialogListView), 'Bookmarks', self)
        bookmarks_button.triggered.connect(self.show_bookmarks)
        navbar.addAction(bookmarks_button)

        # Add dark mode toggle
        self.dark_mode = QAction(self.style().standardIcon(QStyle.SP_DialogYesButton), 'Dark Mode', self, checkable=True)
        self.dark_mode.triggered.connect(self.toggle_dark_mode)
        navbar.addAction(self.dark_mode)

        # Add download manager button
        download_manager_button = QAction(self.style().standardIcon(QStyle.SP_DriveHDIcon), 'Downloads', self)
        download_manager_button.triggered.connect(self.show_downloads)
        navbar.addAction(download_manager_button)

        # Add history button
        history_button = QAction(self.style().standardIcon(QStyle.SP_FileDialogDetailedView), 'History', self)
        history_button.triggered.connect(self.show_history)
        navbar.addAction(history_button)

        # Add settings button
        settings_button = QAction(self.style().standardIcon(QStyle.SP_FileDialogContentsView), 'Settings', self)
        settings_button.triggered.connect(self.show_settings)
        navbar.addAction(settings_button)

        # Initialize bookmarks
        self.bookmarks = []

        # Initialize history
        self.history = []

        # Initialize downloads
        self.downloads = []

        # Add a new tab
        # Replace the default homepage with the loaded homepage
        homepage_url = self.config.get("homepage", "http://www.google.com")
        self.add_new_tab(QUrl(homepage_url), 'Homepage')

        # Add status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.closed_tabs = []  # Store closed tabs

        # Set the initial style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                padding: 5px;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px;
                margin: 2px;
                border-radius: 10px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                font-weight: bold;
            }
            QLineEdit {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLabel {
                font-size: 14px;
            }
        """)

        # Restore session
        self.restore_session()

        # Enable disk caching
        profile = QWebEngineProfile.defaultProfile()
        cache_path = QStandardPaths.writableLocation(QStandardPaths.CacheLocation)
        profile.setCachePath(cache_path)
        profile.setPersistentStoragePath(cache_path)
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # Set cache size to 100 MB

        profile.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        profile.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)

        # Enable request interception
        self.interceptor = RequestInterceptor()
        profile.setUrlRequestInterceptor(self.interceptor)  # Updated method

    def preload_dns(self, domains):
        for domain in domains:
            QHostInfo.lookupHost(domain, lambda info: None)

    def create_new_tab_button(self):
        new_tab_button = QPushButton("+", self)
        new_tab_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                width: 30px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        new_tab_button.clicked.connect(self.add_new_tab)
        return new_tab_button

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None or not isinstance(qurl, QUrl):
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Explicitly load the URL when the tab is created
        browser.setUrl(qurl)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

        # Connect download requested signal
        browser.page().profile().downloadRequested.connect(self.handle_download)
        # Connect load progress signal
        browser.loadProgress.connect(self.update_status)

        # Enable request interception
        self.interceptor = RequestInterceptor()
        profile = QWebEngineProfile.defaultProfile()
        profile.setRequestInterceptor(self.interceptor)

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        if self.tabs.currentWidget():
            qurl = self.tabs.currentWidget().url()
            self.update_urlbar(qurl, self.tabs.currentWidget())
            self.update_title(self.tabs.currentWidget())

            # Update connections to the current tab's signals
            self.tabs.currentWidget().urlChanged.connect(lambda qurl: self.update_urlbar(qurl, self.tabs.currentWidget()))
            self.tabs.currentWidget().loadProgress.connect(self.update_status)

    def close_current_tab(self, i):
        """Close the tab at the given index."""
        if self.tabs.count() < 2:
            QMessageBox.warning(self, "Warning", "Cannot close the last tab!")
            return

        # Remove the tab immediately
        widget = self.tabs.widget(i)
        if widget:
            widget.deleteLater()
        self.tabs.removeTab(i)

    def reopen_closed_tab(self):
        if self.closed_tabs:
            url, label = self.closed_tabs.pop()
            self.add_new_tab(QUrl(url), label)

    def tab_context_menu(self, point):
        index = self.tabs.tabBar().tabAt(point)
        if index != -1:
            browser = self.tabs.widget(index)
            thumbnail = browser.grab()  # Capture a thumbnail of the tab
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(thumbnail.scaled(200, 150, Qt.KeepAspectRatio))
            thumbnail_label.show()

    def update_urlbar(self, qurl, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Python Web Browser")

    def load_url_from_address_bar(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        search_engine = self.search_engine.currentText()
        if search_engine == "Google":
            search_url = f"https://www.google.com/search?q={url}"
        elif search_engine == "Bing":
            search_url = f"https://www.bing.com/search?q={url}"
        else:
            search_url = f"https://duckduckgo.com/?q={url}"
        self.tabs.currentWidget().setUrl(QUrl(search_url))

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def update_status(self, progress):
        if not hasattr(self, 'progress_bar'):
            self.progress_bar = QProgressBar(self)
            self.progress_bar.setMaximum(100)
            self.statusBar().addWidget(self.progress_bar, 1)

        self.progress_bar.setValue(progress)
        if progress == 100:
            self.progress_bar.hide()
        else:
            self.progress_bar.show()

    def show_bookmarks(self):
        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Bookmarks")
        layout = QVBoxLayout()
        for bookmark in self.bookmarks:
            bookmark_layout = QHBoxLayout()
            btn = QPushButton(bookmark, self)
            btn.clicked.connect(lambda _, url=bookmark: self.tabs.currentWidget().setUrl(QUrl(url)))
            delete_btn = QPushButton("Delete", self)
            delete_btn.clicked.connect(lambda _, url=bookmark: self.delete_bookmark(url))
            bookmark_layout.addWidget(btn)
            bookmark_layout.addWidget(delete_btn)
            layout.addLayout(bookmark_layout)
        bookmarks_dialog.setLayout(layout)
        bookmarks_dialog.exec_()

    def delete_bookmark(self, url):
        self.bookmarks.remove(url)

    def toggle_dark_mode(self):
        if self.dark_mode.isChecked():
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
            self.tabs.setStyleSheet("background-color: #2e2e2e; color: white;")
        else:
            self.setStyleSheet("")
            self.tabs.setStyleSheet("")

    def handle_download(self, download):
        download_path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if download_path:
            download.setPath(download_path)  # Set the path before accepting the download
            download.accept()
            self.downloads.append(download_path)
            self.show_download_progress(download)

    def show_download_progress(self, download):
        progress_dialog = QProgressDialog("Downloading...", "Cancel", 0, 100, self)
        progress_dialog.setWindowTitle("Download Progress")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setAutoClose(True)
        progress_dialog.setAutoReset(True)
        
        def update_progress(received, total):
            if total > 0:
                progress_value = int(received / total * 100)
                progress_dialog.setValue(progress_value)
            else:
                progress_dialog.setValue(0)
        
        download.downloadProgress.connect(update_progress)
        download.finished.connect(progress_dialog.close)
        download.finished.connect(lambda: QMessageBox.information(self, "Download Completed", f"Download finished: {download.path()}"))
        
        progress_dialog.show()

    def show_downloads(self):
        downloads_dialog = QDialog(self)
        downloads_dialog.setWindowTitle("Downloads")
        layout = QVBoxLayout()
        for download in self.downloads:
            layout.addWidget(QLabel(download))
        downloads_dialog.setLayout(layout)
        downloads_dialog.exec_()

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("History")
        layout = QVBoxLayout()
        for url in self.history:
            btn = QPushButton(url, self)
            btn.clicked.connect(lambda _, url=url: self.tabs.currentWidget().setUrl(QUrl(url)))
            layout.addWidget(btn)
        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def show_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        layout = QVBoxLayout()

        homepage_label = QLabel("Homepage URL:")
        self.homepage_input = QLineEdit(self)
        self.homepage_input.setText("http://www.google.com")
        layout.addWidget(homepage_label)
        layout.addWidget(self.homepage_input)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        settings_dialog.setLayout(layout)
        settings_dialog.exec_()

    def load_config(self):
        try:
            with open(self.config_file, "r") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {"homepage": "http://www.google.com"}

    def save_config(self):
        with open(self.config_file, "w") as file:
            json.dump(self.config, file)

    def save_settings(self):
        homepage_url = self.homepage_input.text()
        self.config["homepage"] = homepage_url
        self.save_config()
        self.tabs.currentWidget().setUrl(QUrl(homepage_url))

    def save_session(self):
        session = [{"url": self.tabs.widget(i).url().toString(), "title": self.tabs.tabText(i)} for i in range(self.tabs.count())]
        with open("session.json", "w") as file:
            json.dump(session, file)

    def restore_session(self):
        try:
            with open("session.json", "r") as file:
                session = json.load(file)
                for tab in session:
                    self.add_new_tab(QUrl(tab["url"]), tab["title"])
        except FileNotFoundError:
            pass

    def handle_request_intercept(self, request):
        url = request.requestUrl().toString()
        if "tracker" in url:
            request.abort()

    def create_sidebar(self):
        self.sidebar = QDockWidget("Sidebar", self)
        self.sidebar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sidebar.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)

        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()

        bookmarks_label = QLabel("Bookmarks")
        bookmarks_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        sidebar_layout.addWidget(bookmarks_label)

        for bookmark in self.bookmarks:
            btn = QPushButton(bookmark, self)
            btn.clicked.connect(lambda _, url=bookmark: self.tabs.currentWidget().setUrl(QUrl(url)))
            sidebar_layout.addWidget(btn)

        history_label = QLabel("History")
        history_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        sidebar_layout.addWidget(history_label)

        for url in self.history:
            btn = QPushButton(url, self)
            btn.clicked.connect(lambda _, url=url: self.tabs.currentWidget().setUrl(QUrl(url)))
            sidebar_layout.addWidget(btn)

        sidebar_widget.setLayout(sidebar_layout)
        self.sidebar.setWidget(sidebar_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)
if __name__ == '__main__':
    main()
