#define PY_SSIZE_T_CLEAN
#include <Python.h>
#ifdef __linux__
#include <dlfcn.h>
#endif
#ifdef _WIN32
#include <Objbase.h>
#include <Shobjidl.h>
#include <Windows.h>
#endif

static PyObject*
mpl_display_is_valid(PyObject* module)
{
#ifdef __linux__
    void* libX11;
    // The getenv check is redundant but helps performance as it is much faster
    // than dlopen().
    if (getenv("DISPLAY")
        && (libX11 = dlopen("libX11.so.6", RTLD_LAZY))) {
        struct Display* display = NULL;
        struct Display* (* XOpenDisplay)(char const*) =
            dlsym(libX11, "XOpenDisplay");
        int (* XCloseDisplay)(struct Display*) =
            dlsym(libX11, "XCloseDisplay");
        if (XOpenDisplay && XCloseDisplay
                && (display = XOpenDisplay(NULL))) {
            XCloseDisplay(display);
        }
        if (dlclose(libX11)) {
            PyErr_SetString(PyExc_RuntimeError, dlerror());
            return NULL;
        }
        if (display) {
            Py_RETURN_TRUE;
        }
    }
    void* libwayland_client;
    if (getenv("WAYLAND_DISPLAY")
        && (libwayland_client = dlopen("libwayland-client.so.0", RTLD_LAZY))) {
        struct wl_display* display = NULL;
        struct wl_display* (* wl_display_connect)(char const*) =
            dlsym(libwayland_client, "wl_display_connect");
        void (* wl_display_disconnect)(struct wl_display*) =
            dlsym(libwayland_client, "wl_display_disconnect");
        if (wl_display_connect && wl_display_disconnect
                && (display = wl_display_connect(NULL))) {
            wl_display_disconnect(display);
        }
        if (dlclose(libwayland_client)) {
            PyErr_SetString(PyExc_RuntimeError, dlerror());
            return NULL;
        }
        if (display) {
            Py_RETURN_TRUE;
        }
    }
    Py_RETURN_FALSE;
#else
    Py_RETURN_TRUE;
#endif
}

static PyObject*
mpl_GetCurrentProcessExplicitAppUserModelID(PyObject* module)
{
#ifdef _WIN32
    wchar_t* appid = NULL;
    HRESULT hr = GetCurrentProcessExplicitAppUserModelID(&appid);
    if (FAILED(hr)) {
        return PyErr_SetFromWindowsErr(hr);
    }
    PyObject* py_appid = PyUnicode_FromWideChar(appid, -1);
    CoTaskMemFree(appid);
    return py_appid;
#else
    Py_RETURN_NONE;
#endif
}

static PyObject*
mpl_SetCurrentProcessExplicitAppUserModelID(PyObject* module, PyObject* arg)
{
#ifdef _WIN32
    wchar_t* appid = PyUnicode_AsWideCharString(arg, NULL);
    if (!appid) {
        return NULL;
    }
    HRESULT hr = SetCurrentProcessExplicitAppUserModelID(appid);
    PyMem_Free(appid);
    if (FAILED(hr)) {
        return PyErr_SetFromWindowsErr(hr);
    }
    Py_RETURN_NONE;
#else
    Py_RETURN_NONE;
#endif
}

static PyObject*
mpl_GetForegroundWindow(PyObject* module)
{
#ifdef _WIN32
  return PyLong_FromVoidPtr(GetForegroundWindow());
#else
  Py_RETURN_NONE;
#endif
}

static PyObject*
mpl_SetForegroundWindow(PyObject* module, PyObject *arg)
{
#ifdef _WIN32
  HWND handle = PyLong_AsVoidPtr(arg);
  if (PyErr_Occurred()) {
    return NULL;
  }
  if (!SetForegroundWindow(handle)) {
    return PyErr_Format(PyExc_RuntimeError, "Error setting window");
  }
  Py_RETURN_NONE;
#else
  Py_RETURN_NONE;
#endif
}

static PyMethodDef functions[] = {
    {"display_is_valid", (PyCFunction)mpl_display_is_valid, METH_NOARGS,
     "display_is_valid()\n--\n\n"
     "Check whether the current X11 or Wayland display is valid.\n\n"
     "On Linux, returns True if either $DISPLAY is set and XOpenDisplay(NULL)\n"
     "succeeds, or $WAYLAND_DISPLAY is set and wl_display_connect(NULL)\n"
     "succeeds.  On other platforms, always returns True."},
    {"Win32_GetCurrentProcessExplicitAppUserModelID",
     (PyCFunction)mpl_GetCurrentProcessExplicitAppUserModelID, METH_NOARGS,
     "Win32_GetCurrentProcessExplicitAppUserModelID()\n--\n\n"
     "Wrapper for Windows's GetCurrentProcessExplicitAppUserModelID.  On \n"
     "non-Windows platforms, always returns None."},
    {"Win32_SetCurrentProcessExplicitAppUserModelID",
     (PyCFunction)mpl_SetCurrentProcessExplicitAppUserModelID, METH_O,
     "Win32_SetCurrentProcessExplicitAppUserModelID(appid, /)\n--\n\n"
     "Wrapper for Windows's SetCurrentProcessExplicitAppUserModelID.  On \n"
     "non-Windows platforms, a no-op."},
    {"Win32_GetForegroundWindow",
     (PyCFunction)mpl_GetForegroundWindow, METH_NOARGS,
     "Win32_GetForegroundWindow()\n--\n\n"
     "Wrapper for Windows' GetForegroundWindow.  On non-Windows platforms, \n"
     "always returns None."},
    {"Win32_SetForegroundWindow",
     (PyCFunction)mpl_SetForegroundWindow, METH_O,
     "Win32_SetForegroundWindow(hwnd, /)\n--\n\n"
     "Wrapper for Windows' SetForegroundWindow.  On non-Windows platforms, \n"
     "a no-op."},
    {NULL, NULL}};  // sentinel.
static PyModuleDef util_module = {
    PyModuleDef_HEAD_INIT, "_c_internal_utils", "", 0, functions, NULL, NULL, NULL, NULL};

#pragma GCC visibility push(default)
PyMODINIT_FUNC PyInit__c_internal_utils(void)
{
    return PyModule_Create(&util_module);
}
