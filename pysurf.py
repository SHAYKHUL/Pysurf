import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

def main():
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.setCentralWidget(self.tabs)

        # Create a navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Add back button
        back_button = QAction('Back', self)
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_button)

        # Add forward button
        forward_button = QAction('Forward', self)
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_button)

        # Add reload button
        reload_button = QAction('Reload', self)
        reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_button)

        # Add home button
        home_button = QAction('Home', self)
        home_button.triggered.connect(self.navigate_home)
        navbar.addAction(home_button)

        # Add stop button
        stop_button = QAction('Stop', self)
        stop_button.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navbar.addAction(stop_button)

        # Add address bar
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.load_url_from_address_bar)
        navbar.addWidget(self.url_bar)

        # Add search engine selection
        self.search_engine = QComboBox(self)
        self.search_engine.addItems(["Google", "Bing", "DuckDuckGo"])
        navbar.addWidget(self.search_engine)

        # Add bookmarks button
        bookmarks_button = QAction('Bookmarks', self)
        bookmarks_button.triggered.connect(self.show_bookmarks)
        navbar.addAction(bookmarks_button)

        # Add dark mode toggle
        self.dark_mode = QAction('Dark Mode', self, checkable=True)
        self.dark_mode.triggered.connect(self.toggle_dark_mode)
        navbar.addAction(self.dark_mode)

        # Add download manager button
        download_manager_button = QAction('Downloads', self)
        download_manager_button.triggered.connect(self.show_downloads)
        navbar.addAction(download_manager_button)

        # Add history button
        history_button = QAction('History', self)
        history_button.triggered.connect(self.show_history)
        navbar.addAction(history_button)

        # Add settings button
        settings_button = QAction('Settings', self)
        settings_button.triggered.connect(self.show_settings)
        navbar.addAction(settings_button)

        # Add new tab button
        new_tab_button = QAction('New Tab', self)
        new_tab_button.triggered.connect(self.add_new_tab)
        navbar.addAction(new_tab_button)

        # Initialize bookmarks
        self.bookmarks = []

        # Initialize history
        self.history = []

        # Initialize downloads
        self.downloads = []

        # Add a new tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        # Add status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None or not isinstance(qurl, QUrl):
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

        # Connect download requested signal
        browser.page().profile().downloadRequested.connect(self.handle_download)
        # Connect load progress signal
        browser.loadProgress.connect(self.update_status)

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
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def tab_context_menu(self, point):
        context_menu = QMenu(self)
        new_tab_action = QAction('New Tab', self)
        new_tab_action.triggered.connect(self.add_new_tab)
        context_menu.addAction(new_tab_action)
        context_menu.exec_(self.tabs.mapToGlobal(point))

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
        self.status.showMessage(f"Loading... {progress}%")

    def show_bookmarks(self):
        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Bookmarks")
        layout = QVBoxLayout()
        for bookmark in self.bookmarks:
            btn = QPushButton(bookmark, self)
            btn.clicked.connect(lambda _, url=bookmark: self.tabs.currentWidget().setUrl(QUrl(url)))
            layout.addWidget(btn)
        bookmarks_dialog.setLayout(layout)
        bookmarks_dialog.exec_()

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
            download.setPath(download_path)
            self.downloads.append(download_path)
            download.accept()
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

    def save_settings(self):
        homepage_url = self.homepage_input.text()
        self.tabs.currentWidget().setUrl(QUrl(homepage_url))

if __name__ == '__main__':
    main()
