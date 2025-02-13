# Changelog

## Migration from Old Code to New Code
This document outlines the key differences and improvements between the old implementation and the new refactored code in `DateTimeOps`.

### **Key Differences Between the Old and New Code**

| **Aspect**               | **Old Code** | **New Code** | **Impact** |
|--------------------------|-------------|-------------|------------|
| **`validate_date` Future Check** | Used `dt.strftime('%Y-%m-%d') >= now_utc('%Y-%m-%d')` | Now uses `dt >= datetime.datetime.now(datetime.timezone.utc)` | ✅ Corrected logic, now accounts for full datetime comparison |
| **`validate_date` Input Handling** | Only validated strings | Supports both `str` and `datetime` objects, rejects integers | ✅ Improved robustness |
| **`validate_date` Auto-Detection** | Required `fmt` to be passed explicitly | Auto-detects between `%Y-%m-%d %H:%M:%S` and `%Y-%m-%d` | ✅ Backward compatible, better usability |
| **`epoch()` Output Format** | Returned as a string (`str(int(time.time()))`) | Returns an integer (`int(time.time())`) | ⚠️ **Potential Change**—we decided to keep it |
| **`change_date_format()` Fail Handling** | Would raise an error on invalid input | Initially returned `None`, but now raises `ValueError` | ✅ Now matches old behavior |
| **`offset_date` Auto-Detection** | Required `from_fmt`, assumed `%Y-%m-%d %H:%M:%S` if not provided | Auto-detects format based on string length | ✅ More flexible, but ensures backward compatibility |
| **`offset_date` Offset Handling** | Used explicit `if-elif` for offset types | Uses `relativedelta(**{offset_type: offset_amount})` | ✅ More maintainable, but functionally identical |
| **`add_days_to_date` / `add_months_to_date` Defaults** | Required `to_fmt` | Defaults to `from_fmt` if `to_fmt` is `None` | ✅ More user-friendly, maintains backward compatibility |
| **`get_first_last_date_of_month` Uses `now_utc()`** | Used `utc_time.strftime(fmt)` | Uses `now_utc(fmt="%Y-%m-%d")` | ✅ Identical behavior |
| **`hhmmss_to_seconds()` Colon Handling** | Used regex (`re.findall(':', hhmmss)`) | Directly splits `hhmmss.split(':')` | ✅ Simpler, functionally identical |

---

## **Recent Fixes & Updates**
1. **Fixed `validate_date` to ensure full datetime comparison instead of just date-only.**
2. **Ensured `validate_date` properly handles both string and datetime inputs.**
3. **Updated `epoch()` to return an integer instead of a string (intentional change).**
4. **Restored `change_date_format` to raise a `ValueError` instead of returning `None` for invalid input.**
5. **Refactored `offset_date` for better maintainability while keeping identical functionality.**
6. **Added extensive test cases to cover all function permutations and edge cases.**

---

## **Testing Plan**
- ✅ **Ran `pytest tests/` to confirm all functions behave identically to the old implementation.**
- ✅ **Verified that all output formats and return values match the old implementation, except `epoch()`.**
- ✅ **Ensured proper error handling by making `change_date_format` raise a `ValueError`.**
- ✅ **Compared old vs. new outputs using automated tests and reviewed all mismatches.**

---
