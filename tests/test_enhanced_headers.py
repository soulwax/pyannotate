# File: tests/test_enhanced_headers.py
"""Tests for the enhanced header handling functionality."""

import os
import shutil
from pathlib import Path

import pytest

from pyannotate.annotate_headers import (
    _detect_header_pattern,
    _has_existing_header,
    _merge_headers,
    _remove_existing_header,
    process_file,
    walk_directory,
)

# Directory for temporary test files
TEST_DIR = Path("tests/enhanced_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True)

    # Create test directories
    web_dir = TEST_DIR / "web"
    web_dir.mkdir()

    # Create sample files with different header patterns
    _create_test_pattern_files()
    _create_web_framework_test_files()

    yield

    # Cleanup after tests
    shutil.rmtree(TEST_DIR)


def _create_test_pattern_files():
    """Create test files with different header patterns."""
    patterns = [
        ("# File: test.py", "#", ""),
        ("// Filename: test.js", "//", ""),
        ("/* Source: test.css */", "/*", "*/"),
        ("<!-- Path: test.html -->", "<!--", "-->"),
        ("# @file test.rb", "#", ""),
    ]

    for i, (header, start, end) in enumerate(patterns):
        file_path = TEST_DIR / f"pattern_{i}.txt"
        content = f"{header}\nprint('test')\n"
        file_path.write_text(content)


def _create_web_framework_test_files():
    """Create test files for web frameworks."""
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

    # Create subdirectories
    web_dirs = ["vue", "svelte", "astro", "react", "html"]
    for dir_name in web_dirs:
        os.makedirs(TEST_DIR / dir_name, exist_ok=True)

    # Write test files
    (TEST_DIR / "vue" / "Component.vue").write_text(vue_component)
    (TEST_DIR / "vue" / "SetupComponent.vue").write_text(vue_setup)
    (TEST_DIR / "svelte" / "Component.svelte").write_text(svelte_component)
    (TEST_DIR / "astro" / "Component.astro").write_text(astro_component)
    (TEST_DIR / "react" / "Counter.jsx").write_text(react_component)
    (TEST_DIR / "html" / "index.html").write_text(html_file)


# Rest of your test cases here...
