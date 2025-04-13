# File: tests/create_web_test_files.py
"""
Script to generate sample web framework files for testing.
Run this script to create a set of test files in tests/sample_web_files directory.
"""

from pathlib import Path

# Basic Vue component
vue_component = """<template>
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
  props: {
    msg: String
  }
}
</script>

<style scoped>
h1 {
  margin: 40px 0 0;
  color: #42b983;
}
</style>
"""

# Vue with script setup
vue_setup = """<script setup>
import { ref, onMounted } from 'vue'

const count = ref(0)
const message = ref('Hello Vue 3!')

onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div class="container">
    <h1>{{ message }}</h1>
    <button @click="count++">Count: {{ count }}</button>
  </div>
</template>

<style scoped>
.container {
  text-align: center;
  margin-top: 60px;
}
</style>
"""

# Svelte component
svelte_component = """<script>
  export let name = 'world';
  let count = 0;
  
  function handleClick() {
    count += 1;
  }
</script>

<main>
  <h1>Hello {name}!</h1>
  <button on:click={handleClick}>
    Clicked {count} {count === 1 ? 'time' : 'times'}
  </button>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }
  
  h1 {
    color: #ff3e00;
    font-size: 4em;
    font-weight: 100;
  }
  
  button {
    background-color: #ff3e00;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
  }
</style>
"""

# Astro component
astro_component = """---
// Component imports and props
import { Button } from '../components/Button.astro';
const { title = 'Default Title' } = Astro.props;
---

<section class="hero">
  <h1>{title}</h1>
  <p>Welcome to my Astro site!</p>
  <Button text="Learn more" />
</section>

<style>
  .hero {
    padding: 4rem;
    text-align: center;
  }
  h1 {
    font-size: 3rem;
    font-weight: 800;
  }
</style>

<script>
  // Client-side JavaScript
  document.querySelector('h1').addEventListener('click', () => {
    alert('Hello from Astro!');
  });
</script>
"""

# React JSX component
react_component = """import React, { useState, useEffect } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    document.title = `You clicked ${count} times`;
  }, [count]);
  
  return (
    <div className="counter">
      <h1>You clicked {count} times</h1>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}

export default Counter;
"""

# HTML file with doctype
html_file = """<!DOCTYPE html>
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
            <p>This is a sample HTML page for testing the PyAnnotate tool.</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 PyAnnotate Example</p>
    </footer>
    
    <script src="main.js"></script>
</body>
</html>
"""

# File with different header format
different_header_js = """// Filename: legacy-component.js
// Author: Legacy Developer
// Created: 2022-01-01
// Version: 1.0.0

class LegacyComponent {
  constructor(props) {
    this.props = props;
    this.state = {
      count: 0
    };
  }
  
  incrementCount() {
    this.state.count++;
    console.log(`Count is now ${this.state.count}`);
  }
  
  render() {
    return `<div class="legacy-component">
      <h2>${this.props.title}</h2>
      <p>Count: ${this.state.count}</p>
      <button onClick="this.incrementCount()">Increment</button>
    </div>`;
  }
}

export default LegacyComponent;
"""

# CSS with header using different format
css_with_header = """/* Source: styles.css
 * Description: Main stylesheet for the application
 * Author: Design Team
 */

:root {
  --primary-color: #4a90e2;
  --secondary-color: #e74c3c;
  --text-color: #333;
  --background-color: #f9f9f9;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: var(--background-color);
  margin: 0;
  padding: 0;
}

header {
  background-color: var(--primary-color);
  color: white;
  padding: 1rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .container {
    padding: 0.5rem;
  }
}
"""


def create_test_files():
    """Create all test files for web frameworks."""
    # Set up test directory structure
    TEST_DIR = Path("tests/sample_web_files")

    # Create main directory if it doesn't exist
    TEST_DIR.mkdir(parents=True, exist_ok=True)

    # Create framework-specific directories
    dirs = {
        "vue": ["Component.vue", "SetupComponent.vue"],
        "svelte": ["Component.svelte"],
        "astro": ["Component.astro"],
        "react": ["Counter.jsx"],
        "html": ["index.html"],
        "legacy": ["legacy-component.js", "styles.css"],
    }

    # Create all directories and their files
    for dir_name, files in dirs.items():
        dir_path = TEST_DIR / dir_name
        dir_path.mkdir(exist_ok=True)

    # Write files
    (TEST_DIR / "vue" / "Component.vue").write_text(vue_component)
    (TEST_DIR / "vue" / "SetupComponent.vue").write_text(vue_setup)
    (TEST_DIR / "svelte" / "Component.svelte").write_text(svelte_component)
    (TEST_DIR / "astro" / "Component.astro").write_text(astro_component)
    (TEST_DIR / "react" / "Counter.jsx").write_text(react_component)
    (TEST_DIR / "html" / "index.html").write_text(html_file)
    (TEST_DIR / "legacy" / "legacy-component.js").write_text(different_header_js)
    (TEST_DIR / "legacy" / "styles.css").write_text(css_with_header)

    print(f"Test files created successfully in {TEST_DIR}")
    print("Directory structure:")
    for dir_name, files in dirs.items():
        print(f"  {dir_name}/")
        for file in files:
            print(f"    {file}")

    # Return the path for convenience
    return TEST_DIR


if __name__ == "__main__":
    test_dir = create_test_files()
    print(f"\nTo process these files, run: python -m pyannotate -d {test_dir}")
