# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of web pages featuring ASCII art. Focus on clean, fast, dark-mode-first design.

## Design Principles

- Dark mode by default (dark backgrounds, light text)
- Minimal dependencies - prefer vanilla HTML/CSS/JS
- Use monospace fonts for ASCII art display
- Fast loading - no heavy frameworks
- Preserve ASCII art formatting with `<pre>` tags or CSS `white-space: pre`

## File Structure

- `index.html` - Landing page
- `styles.css` - Shared styles
- Individual pages for different ASCII art pieces

## CSS Defaults

```css
body {
  background: #0d0d0d;
  color: #e0e0e0;
  font-family: monospace;
}
```
