// Disable localStorage and sessionStorage for Node 22+ environments
// to prevent SecurityError during build processes that access global storage properties.
delete global.localStorage;
delete global.sessionStorage;
Object.defineProperty(global, "localStorage", { get: () => undefined, configurable: true });
Object.defineProperty(global, "sessionStorage", { get: () => undefined, configurable: true });
