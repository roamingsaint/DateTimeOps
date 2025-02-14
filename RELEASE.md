# **Release Process for DateTimeOps**

This document outlines the release process for the DateTimeOps package. It ensures a structured and reliable release cycle.

---

## **1⃣ On Every Push (General Commit)**
✅ Runs tests  
❌ Does not create a tag  
❌ Does not publish to PyPI  

### **Purpose**
- Ensures the latest commits don’t break functionality.
- Allows continuous integration testing without affecting versioning.

---

## **2⃣ On Version Bump (setup.py Updated)**
✅ Runs tests  
✅ Creates a new Git tag (e.g., `v0.2.0`) if the version is incremented  
❌ Does not publish to PyPI  

### **Version Bump Rules**
The version in `setup.py` must be **greater** than the latest Git tag.

✅ **Allowed Increments**:
- `0.1.0` → `0.1.1` (Patch bump)
- `0.1.0` → `0.2.0` (Minor bump)
- `0.1.0` → `1.0.0` (Major bump)
- `0.1.0` → `1.1.1` (Flexible bump)

🚫 **Not Allowed**:
- **Downgrade or same version:** e.g., `1.0.1` → `1.0.0`
- **Re-tagging the same version:** If a tag exists, it must be incremented.

### **More Flexible Versioning**
Unlike before, **this workflow does not enforce absolute step-by-step increments**. You can jump from `0.1.0` to `1.1.1` if needed.

**If the version does not increment properly, the workflow will fail before tagging.**

---

## **3⃣ On GitHub Release (Manual Release in UI)**
✅ Publishes to PyPI  

### **Steps to Release**
1. Ensure all **tests pass**.
2. Manually create a **GitHub Release** (this triggers the `publish` job).
3. The workflow will:
   - Build the package.
   - Upload it to PyPI.

---

## **📌 Commands for Manual Versioning**

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
   git push
   ```

### **Tagging the New Version (Triggered Automatically)**
If the `setup.py` version is correctly incremented:
```sh
git tag vX.Y.Z
git push origin vX.Y.Z
```
(✅ **This happens automatically if the version is valid.**)

---

## **📦 Manual PyPI Publishing (If Needed)**
In case the workflow fails or you need to publish manually:
```sh
python -m build
twine upload dist/*
```

---

## **📝 Summary of Workflow Behavior**
| **Event**             | **Tests Run?** | **Tag Created?** | **Published to PyPI?** |
|----------------------|--------------|---------------|----------------|
| General Commit       | ✅ Yes        | ❌ No         | ❌ No         |
| Version Bump (`setup.py`) | ✅ Yes  | ✅ Yes (if valid) | ❌ No |
| Manual GitHub Release | ✅ Yes | ❌ No | ✅ Yes |

---

### **Notes**
- The **tagging process is now more flexible**, allowing jumps like `0.1.0 → 1.1.1`.
- **Manual GitHub releases control publishing**—automated tags do not trigger publishing.
- **General pushes only trigger tests**, avoiding unnecessary tags or releases.

🚀 **Happy coding and smooth releases!** 🚀

