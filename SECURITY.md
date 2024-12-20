# **Security Policy**

## **Supported Versions**
The following versions of the PyQt5 Web Browser are currently supported with security updates:

| Version      | Supported          |
|--------------|--------------------|
| Latest (main) | ✅ Yes             |
| Older versions | ❌ No             |

Users are encouraged to always use the latest version of the browser for the most up-to-date security patches.

---

## **Security Features**
1. **Safe Browsing:**
   - Supports HTTPS by default for secure communication.
   - Warns users when navigating to non-HTTPS sites.

2. **Sandboxing:**
   - Utilizes `QWebEngineView`, which includes a sandbox for web content, isolating web processes from system resources.

3. **Download Protection:**
   - Prompts users to confirm file downloads to prevent unintentional execution of harmful files.

4. **Customizable JavaScript Settings:**
   - Allows users to disable JavaScript to mitigate the risk of malicious scripts.

5. **Minimal Permissions:**
   - The application does not request or require sensitive system-level permissions.

---

## **Potential Risks**
1. **Third-Party Content:**
   - The browser allows access to any website, which may expose users to malicious sites.
   - Educate users to avoid untrusted URLs.

2. **Add-ons or Extensions:**
   - No add-ons or plugins are supported in this browser, reducing the attack surface.

3. **File Downloads:**
   - Files downloaded through the browser are not scanned for malware. Users should use a trusted antivirus to inspect downloads.

---

## **Best Practices for Users**
1. Always browse websites with HTTPS to ensure data encryption.
2. Avoid entering sensitive information on untrusted websites.
3. Regularly update the browser to receive the latest security fixes.
4. Use the dark mode only for trusted environments, as custom stylesheets may occasionally hide malicious elements.

---

## **Reporting a Vulnerability**
If you discover a security vulnerability in the PyQt5 Web Browser, please report it immediately. We are committed to addressing all security issues promptly.

### How to Report:
- Email: [Shaykhul2004@gmail.cim](mailto: Shaykhul2004@gmail.com)
- Subject: `Security Vulnerability Report - PyQt5 Web Browser`
- Include:
  - A description of the vulnerability.
  - Steps to reproduce the issue.
  - Any potential impact or risk associated with the vulnerability.

### Response Time:
- **Acknowledgment:** Within 24 hours of receiving the report.
- **Investigation:** We will assess the issue within 7 days.
- **Patch Release:** Critical vulnerabilities will be patched and released within 30 days.

---

## **Acknowledgments**
We thank the security researchers and users who report vulnerabilities responsibly, helping make the PyQt5 Web Browser safer for everyone.

---

## **Future Enhancements**
- Add support for **content blocking** (e.g., ads, trackers).
- Introduce **certificate validation** warnings for invalid SSL certificates.
- Provide **sandbox mode** for downloads to inspect potential threats.
