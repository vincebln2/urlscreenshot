# URL Screenshot app

This web service takes screenshots of given URLs using Selenium and Chrome, deployed on fly.io

Uses the BiDi Selenium feature by default but will use WebDriver if BiDi fails.

### Prerequisites

- Have fly.io CLI installed
- That's it! Dockerfile handles the dependencies for the fly.io container.

### How to use

- Deploy with

```bash
fly deploy
```

- Take a screenshot with:
Replace "your-app" with the name of your fly.io app set in fly.toml
Also replace the URL after "url=" with the URL you want to screenshot.

```bash
curl "https://your-app.fly.dev/screenshot?url=https://google.com"
```

This will return something like

```bash
{"filename":"screenshot_####.png","url":"/screenshots/screenshot_####.png"}%
```

This is your screenshot name. You can view it in a browser at "<https://your-app.fly.dev/screenshots/screenshot_####.png>"
