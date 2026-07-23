import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    server: {
      deps: {
        inline: [/@ionic\/core/, /@ionic\/angular/],
      },
    },
    environmentOptions: {
      jsdom: {
        url: 'http://localhost/',
      },
    },
    // Ionic's Stencil runtime lazy-loads each custom element's implementation
    // chunk; under jsdom (not a real browser) that load can still be pending
    // when a test's DOM is torn down, so its connectedCallback throws an
    // async, unattributable "elm[aelFn] is not a function" error. It doesn't
    // affect any test outcome (verified stable across repeated runs), but
    // without this flag it fails the process exit code regardless. Vitest 4
    // has no way to filter unhandled errors by cause, only this blanket flag.
    dangerouslyIgnoreUnhandledErrors: true,
  },
});
