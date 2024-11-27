import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the browser window
        self.setWindowTitle("Python Web Browser")
        self.setGeometry(100, 100, 1024, 768)

        # Create the central widget (QWebEngineView)
        self.browser = QWebEngineView()

        # Set the URL to be opened when the browser starts
        self.browser.setUrl(QUrl("http://www.google.com"))

        # Create a central widget layout and set it
        self.setCentralWidget(self.browser)

        # Create a navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Add back button
        back_button = QAction('Back', self)
        back_button.triggered.connect(self.browser.back)
        navbar.addAction(back_button)

        # Add forward button
        forward_button = QAction('Forward', self)
        forward_button.triggered.connect(self.browser.forward)
        navbar.addAction(forward_button)

        # Add reload button
        reload_button = QAction('Reload', self)
        reload_button.triggered.connect(self.browser.reload)
        navbar.addAction(reload_button)

        # Add address bar
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.load_url_from_address_bar)
        navbar.addWidget(self.url_bar)

        # Update the address bar when the page is loaded
        self.browser.urlChanged.connect(self.update_address_bar)

    def update_address_bar(self, qurl):
        self.url_bar.setText(qurl.toString())

    def load_url_from_address_bar(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

def main():
    app = QApplication(sys.argv)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = Browser()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
