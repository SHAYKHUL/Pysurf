# **PyQt5 Web Browser**

A lightweight, feature-rich, and customizable web browser built using Python and PyQt5. This project is perfect for learning, experimenting, or creating a personal web browser.

---

## **Features**
- **Tabbed Browsing:** Open and manage multiple websites simultaneously.
- **Bookmarks Manager:** Save and manage your favorite websites.
- **Search Engines:** Choose between Google, Bing, and DuckDuckGo.
- **Dark Mode:** Toggle dark mode for comfortable browsing.
- **Download Manager:** Manage and track file downloads with progress.
- **History Tracking:** View and revisit your browsing history.
- **Customizable Homepage:** Set your preferred homepage.
- **Responsive UI:** Optimized for modern screens and high DPI scaling.

---

## **Preview**
![Browser Icon](resources/icon.png)

---

## **Getting Started**
Follow the steps below to install and use the PyQt5 Web Browser.

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   https://github.com/SHAYKHUL/Pysurf.git ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python browser.py
   ```

---

## **Usage**
- Use the **address bar** to navigate to a URL or perform a search.
- **Toolbar Buttons**:
  - Back, Forward, Reload, Stop, Home.
- **Tabs**:
  - Open a new tab with the `+` button or double-click the tab bar.
- **Bookmarks**:
  - Save your favorite websites and access them from the Bookmarks menu.
- **Dark Mode**:
  - Toggle using the "Dark Mode" button.
- **Download Manager**:
  - Manage file downloads with a built-in progress tracker.

---

## **Distributing the Browser**
You can package this browser into an executable for distribution:

### Using PyInstaller
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create a standalone executable:
   ```bash
   pyinstaller --onefile --noconsole --windowed --icon=resources/icon.ico browser.py
   ```

3. Distribute the `dist/browser.exe` file.

---

## **Contributing**
Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Support**
For questions or support, open an issue in the GitHub repository
---

## **Acknowledgments**
- **PyQt5 Framework**: For making GUI development seamless.
- **Contributors**: Thanks to all who contribute to this project
