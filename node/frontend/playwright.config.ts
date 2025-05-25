import process from 'node:process'
import { defineConfig, devices } from '@playwright/test'

/**
 * ファイルから環境変数を読み込みます。
 * https://github.com/motdotla/dotenv
 */
// require('dotenv').config();

/**
 * Playwright のテスト設定については https://playwright.dev/docs/test-configuration を参照してください。
 */
export default defineConfig({
  testDir: './e2e',
  /* 1つのテストが実行できる最大時間（ミリ秒）。 */
  timeout: 30 * 1000,
  expect: {
    /**
     * expect() が条件を満たすまで待機する最大時間。
     * 例: `await expect(locator).toHaveText();`
     */
    timeout: 5000,
  },
  /* ソースコードに test.only が残っていた場合、CI でビルドを失敗させます。 */
  forbidOnly: !!process.env.CI,
  /* CI のみリトライを有効化 */
  retries: process.env.CI ? 2 : 0,
  /* CI では並列テストを無効化。 */
  workers: process.env.CI ? 1 : undefined,
  /* 使用するレポーター。詳細: https://playwright.dev/docs/test-reporters */
  reporter: 'html',
  /* 以下は全プロジェクト共通の設定。詳細: https://playwright.dev/docs/api/class-testoptions */
  use: {
    /* click() など各アクションの最大時間。デフォルトは 0（無制限）。 */
    actionTimeout: 0,
    /* `await page.goto('/')` などで使用するベースURL。 */
    baseURL: process.env.CI ? 'http://localhost:4173' : 'http://localhost:5173',

    /* 失敗したテストをリトライする際にトレースを収集。詳細: https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* CI 環境のみヘッドレスでテストを実行 */
    headless: !!process.env.CI,
  },

  /* 主要ブラウザ用のプロジェクト設定 */
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
      },
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
      },
    },

    /* モバイル画面サイズでのテスト例 */
    // {
    //   name: 'Mobile Chrome',
    //   use: {
    //     ...devices['Pixel 5'],
    //   },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: {
    //     ...devices['iPhone 12'],
    //   },
    // },

    /* ブランドブラウザでのテスト例 */
    // {
    //   name: 'Microsoft Edge',
    //   use: {
    //     channel: 'msedge',
    //   },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: {
    //     channel: 'chrome',
    //   },
    // },
  ],

  /* スクリーンショットや動画、トレースなどのテスト成果物の保存先 */
  // outputDir: 'test-results/',

  /* テスト開始前にローカル開発サーバーを起動 */
  webServer: {
    /**
     * デフォルトでは開発サーバーを使用し、フィードバックループを高速化。
     * CI ではプレビューサーバーを使用し、より現実的なテストを実施。
     * 既に dev-server が起動している場合は再利用します。
     */
    command: process.env.CI ? 'npm run preview' : 'npm run dev',
    port: process.env.CI ? 4173 : 5173,
    reuseExistingServer: !process.env.CI,
  },
})
