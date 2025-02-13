# Release Process for DateTimeOps

This document outlines the release process for the DateTimeOps package. Follow these steps to ensure a smooth release cycle.

---

## **1️⃣ On Every Push (General Commit)**
✅ Runs tests only  
❌ Does not create a tag  
❌ Does not publish to PyPI  

---

## **2️⃣ On Version Bump (setup.py Updated)**
✅ Runs tests  
✅ Creates a new Git tag (e.g., `v0.2.0`) **only if the version is incremented correctly**  
❌ Does not publish to PyPI  

### **Version Bump Rules**
- The version in `setup.py` must be **greater** than the latest Git tag.
- The increment should be **one step forward** in either major, minor, or patch.
- Example:
  - ✅ Allowed: `0.1.0` → `0.1.1`, `0.1.0` → `0.2.0`, `0.1.0` → `1.0.0`
  - ❌ Not Allowed: `0.1.0` → `0.1.3`, `0.1.0` → `0.3.0`
- If the version is skipped or incorrect, the workflow will **fail before tagging**.

---

## **3️⃣ On GitHub Release (Release Created in UI)**
✅ Publishes to PyPI  

### **Steps to Release**
1. Ensure the **tests pass**.
2. Manually create a **GitHub Release**.
3. The workflow will build and upload the package to PyPI.

---

## **Commands for Manual Versioning**

### **Check Current Version and Tags**
```sh
python setup.py --version
git tag --list | sort -V | tail -1
```

### **Bump Version Manually**
1. Edit `setup.py` and update the `version` field.
2. Run:
   ```sh
   git add setup.py
   git commit -m "Bump version to X.Y.Z"
   ```
3. Push your changes:
   ```sh
   git push
   ```

### **Tagging the New Version (Triggered Automatically)**
If the setup.py version is correctly incremented:
```sh
git tag vX.Y.Z
git push origin vX.Y.Z
```
(This will happen **automatically** if the setup.py version is valid.)

---

## **Manual PyPI Publishing**
If needed, you can manually publish to PyPI with:
```sh
python -m build
twine upload dist/*
```

---

### **Notes**
- The `publish` job only runs if a **GitHub Release** is created.
- The **workflow prevents incorrect version bumps** to maintain proper tagging.
- General commits **do not trigger tags or publishing**, only testing.

🚀 Happy coding and smooth releases!
