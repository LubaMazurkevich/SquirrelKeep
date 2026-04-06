(function () {
    if (typeof window.escape !== 'function') {
        return;
    }

    const nativeEscape = window.escape;

    // DAL 3.9.x calls escape() for selected labels; keep ASCII behavior,
    // but return non-ASCII text as-is so Cyrillic is not converted to %uXXXX.
    window.escape = function (value) {
        if (typeof value === 'string' && /[^\x00-\x7F]/.test(value)) {
            return value;
        }
        return nativeEscape(value);
    };
})();
