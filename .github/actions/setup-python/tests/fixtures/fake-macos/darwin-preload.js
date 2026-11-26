// Preloaded via NODE_OPTIONS=--require to make the action believe it runs on
// macOS, so its logic can be exercised on the Linux act runner.
Object.defineProperty(process, 'platform', { value: 'darwin' });
