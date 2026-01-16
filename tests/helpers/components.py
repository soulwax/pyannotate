# File: tests/helpers/components.py

"""Zentralisierte Test-Samples und Helfer zum Vermeiden von Code-Duplizierung."""

from pathlib import Path
from typing import Dict, List, Tuple

# --- Web-Framework Templates -------------------------------------------------
WEB_FRAMEWORK_TEMPLATES: Dict[str, str] = {
    "vue_component": """<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Welcome to your Vue.js application
    </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: { msg: String }
}
</script>

<style scoped>
h1 { margin: 40px 0 0; color: #42b983; }
</style>
""",
    "vue_setup": """<script setup>
import { ref, onMounted } from 'vue'
const count = ref(0)
const message = ref('Hello Vue 3!')
onMounted(() => { console.log('Component mounted') })
</script>

<template>
  <div class="container">
    <h1>{{ message }}</h1>
    <button @click="count++">Count: {{ count }}</button>
  </div>
</template>

<style scoped>
.container { text-align: center; margin-top: 60px; }
</style>
""",
    "svelte_component": """<script>
  export let name = 'world';
  let count = 0;
  function handleClick() { count += 1; }
</script>

<main>
  <h1>Hello {name}!</h1>
  <button on:click={handleClick}>
    Clicked {count} {count === 1 ? 'time' : 'times'}
  </button>
</main>

<style>
  main { text-align: center; padding: 1em; max-width: 240px; margin: 0 auto; }
  h1 { color: #ff3e00; font-size: 4em; font-weight: 100; }
  button { background-color: #ff3e00; color: white; border: none; padding: 8px 12px; border-radius: 4px; }
</style>
""",
    "astro_component": """---
import { Button } from '../components/Button.astro';
const { title = 'Default Title' } = Astro.props;
---

<section class="hero">
  <h1>{title}</h1>
  <p>Welcome to my Astro site!</p>
  <Button text="Learn more" />
</section>

<style>
  .hero { padding: 4rem; text-align: center; }
  h1 { font-size: 3rem; font-weight: 800; }
</style>

<script>
  document.querySelector('h1').addEventListener('click', () => { alert('Hello from Astro!'); });
</script>
""",
    "react_component": """import React, { useState, useEffect } from 'react';
function Counter() {
  const [count, setCount] = useState(0);
  useEffect(() => { document.title = `You clicked ${count} times`; }, [count]);
  return (
    <div className="counter">
      <h1>You clicked {count} times</h1>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
}
export default Counter;
""",
    "html_file": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sample Page</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>Welcome to our website</h1>
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <section>
      <h2>Main Content</h2>
      <p>This is a sample HTML page for testing the Annot8 tool.</p>
    </section>
  </main>
  <footer><p>&copy; 2025 Annot8 Example</p></footer>
  <script src="main.js"></script>
</body>
</html>
""",
    "legacy_js": """// Filename: legacy-component.js
// Author: Legacy Developer
// Created: 2022-01-01
// Version: 1.0.0
class LegacyComponent {
  constructor(props) { this.props = props; this.state = { count: 0 }; }
  incrementCount() { this.state.count++; console.log(`Count is now ${this.state.count}`); }
  render() { return `<div class="legacy-component">
    <h2>${this.props.title}</h2>
    <p>Count: ${this.state.count}</p>
    <button onClick="this.incrementCount()">Increment</button>
  </div>`; }
}
export default LegacyComponent;
""",
    "css_with_header": """/* Source: styles.css
 * Description: Main stylesheet for the application
 * Author: Design Team
 */
:root { --primary-color: #4a90e2; --secondary-color: #e74c3c; --text-color: #333; --background-color: #f9f9f9; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: var(--text-color); background-color: var(--background-color); margin: 0; padding: 0; }
""",
}

# --- Header-Pattern Samples ---------------------------------------------------
COMMENT_STYLE_TEST_CASES: List[Tuple[str, str, str]] = [
    (".py", "#", ""),
    (".js", "//", ""),
    (".css", "/*", "*/"),
    (".html", "<!--", "-->"),
    (".sh", "#", ""),
    (".cpp", "//", ""),
]

ENV_FILE_NAMES = [".env.example", ".env.local", ".env.development", ".env.production"]
LICENSE_FILE_NAMES = ["LICENSE", "COPYING", "NOTICE"]
COMMON_IGNORED_FILES = {
    ".prettierrc": '{"semi": false, "singleQuote": true, "trailingComma": "es5"}',
    ".eslintrc": '{"extends": ["eslint:recommended"], "env": {"node": true}}',
    ".babelrc": '{"presets": ["@babel/preset-env", "@babel/preset-react"]}',
    "package-lock.json": '{"name": "test", "version": "1.0.0", "lockfileVersion": 2}',
}


def create_web_framework_test_files(test_dir: Path) -> None:
    """Erzeuge Web-Framework-Testdateien aus den Templates."""
    for dir_name in ["vue", "svelte", "astro", "react", "html", "legacy"]:
        (test_dir / dir_name).mkdir(exist_ok=True, parents=True)
    (test_dir / "vue" / "Component.vue").write_text(WEB_FRAMEWORK_TEMPLATES["vue_component"])
    (test_dir / "vue" / "SetupComponent.vue").write_text(WEB_FRAMEWORK_TEMPLATES["vue_setup"])
    (test_dir / "svelte" / "Component.svelte").write_text(
        WEB_FRAMEWORK_TEMPLATES["svelte_component"]
    )
    (test_dir / "astro" / "Component.astro").write_text(WEB_FRAMEWORK_TEMPLATES["astro_component"])
    (test_dir / "react" / "Counter.jsx").write_text(WEB_FRAMEWORK_TEMPLATES["react_component"])
    (test_dir / "html" / "index.html").write_text(WEB_FRAMEWORK_TEMPLATES["html_file"])
    (test_dir / "legacy" / "legacy-component.js").write_text(WEB_FRAMEWORK_TEMPLATES["legacy_js"])
    (test_dir / "legacy" / "styles.css").write_text(WEB_FRAMEWORK_TEMPLATES["css_with_header"])


def create_header_test_pattern_files(test_dir: Path) -> List[Tuple[str, str, str]]:
    """Lege Testdateien mit unterschiedlichen Header-Patterns an und gib die Patterns zurück."""
    patterns = [
        ("# File: test.py", "#", ""),
        ("// Filename: test.js", "//", ""),
        ("/* Source: test.css */", "/*", "*/"),
        ("<!-- Path: test.html -->", "<!--", "-->"),
        ("# @file test.rb", "#", ""),
    ]
    for i, (header, _start, _end) in enumerate(patterns):
        file_path = test_dir / f"pattern_{i}.txt"
        file_path.write_text(f"{header}\nprint('test')\n")
    return patterns
