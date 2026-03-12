# Browser Console Warnings - Explanation and Fixes

## Feature Policy Warnings

The "Feature Policy: Skipping unsupported feature name" warnings you see in the browser console are **normal and safe**. They occur because:

### Why These Warnings Appear:

1. **Streamlit Components**: Streamlit renders certain UI elements (charts, widgets) in sandboxed iframes for security
2. **Third-Party Analytics**: Microsoft Clarity (in `analytics.py`) runs in an iframe
3. **Browser Security**: Modern browsers restrict features like clipboard access, camera, geolocation, etc. by default

### Features Being Restricted:

These features are being blocked/skipped (which is good for security):
- `autoplay`, `battery`, `clipboard-write` - Media and system access
- `document-domain`, `encrypted-media` - Cross-origin restrictions  
- `gyroscope`, `magnetometer`, `accelerometer` - Sensor access
- `payment`, `picture-in-picture` - Payment/media features
- `usb`, `vr`, `wake-lock`, `xr-spatial-tracking` - Hardware access

### Are These Warnings Harmful?

**No.** These are informational messages that:
- ✅ Don't break any functionality
- ✅ Don't affect end users (only visible in developer console)
- ✅ Are standard for Streamlit apps
- ✅ Indicate proper browser security is working

### Can These Be Fixed?

**Mostly no, and you wouldn't want to.** These warnings indicate the browser is correctly enforcing security policies. However:

#### ✅ Fixed Issues:
- **Font preload warning**: Fixed by adding `<link rel="preload">` tags in `ui_theme.py`

#### ⚠️ Cannot Be Fixed (Browser-Level):
- Feature Policy warnings from Streamlit's internal components
- Security restrictions in Microsoft Clarity analytics iframe
- Browser sandbox policies

### How to Reduce Warnings (Optional):

If you want to reduce console noise:

1. **Disable Microsoft Clarity** (removes some iframe warnings):
   - Don't set `CLARITY_PROJECT_ID` in secrets or environment
   - Analytics won't be collected

2. **Browser Dev Tools Filter**:
   - In Chrome/Edge: Console → Filters → Hide "Warnings"
   - Or use filter: `-Feature Policy`

### When to Investigate:

Only investigate if:
- ❌ Actual functionality is broken (e.g., file uploads don't work)
- ❌ You specifically need a blocked feature (e.g., clipboard access)
- ❌ New errors appear (not these existing warnings)

## Summary

**These warnings are expected and safe to ignore.** Your Streamlit app is working correctly, and the browser is properly enforcing security policies.

## Cookie Consent

The app includes a cookie consent modal popup to comply with privacy regulations (GDPR/CCPA) when using Microsoft Clarity analytics.

**Key Features:**
- ✅ Modern centered modal with backdrop overlay
- ✅ Only shows on first visit (per session)
- ✅ Smooth animations and professional design
- ✅ Analytics only loads if user accepts
- ✅ Can be disabled via `ENABLE_COOKIE_CONSENT = False` in `config.py`

**Privacy Compliance:**
- Users are informed about cookie usage
- Clear Accept/Decline buttons
- Analytics respects user choice
- Links to Microsoft's privacy statement
