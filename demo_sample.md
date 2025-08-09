# README Editor Demo

This file demonstrates all the markdown features supported by the enhanced preview panel.

## Headers and Typography

### Level 3 Header
#### Level 4 Header
##### Level 5 Header
###### Level 6 Header

This is **bold text** and this is *italic text*. You can also use ~~strikethrough~~ text.

> This is a blockquote. It can contain multiple lines and even other markdown elements.
> 
> - Like this list item
> - And this one too

---

## Links and References

Here are some example links:
- [GitHub](https://github.com)
- [Python.org](https://python.org)
- [Markdown Guide](https://www.markdownguide.org)

Email links work too: [contact@example.com](mailto:contact@example.com)

## Lists

### Unordered Lists
- First item
- Second item
  - Nested item
  - Another nested item
    - Deeply nested item
- Back to first level

### Ordered Lists
1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step

### Task Lists
- [x] Completed task
- [x] Another completed task
- [ ] Incomplete task
- [ ] Another incomplete task

## Code Examples

Inline code: `print("Hello, World!")`

### Python Code Block
```python
def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    return sequence

# Example usage
result = fibonacci(10)
print(f"First 10 Fibonacci numbers: {result}")
```

### JavaScript Code Block
```javascript
// Arrow function example
const greetUser = (name, time) => {
    const greeting = time < 12 ? 'Good morning' : 
                    time < 18 ? 'Good afternoon' : 
                    'Good evening';
    
    return `${greeting}, ${name}!`;
};

console.log(greetUser('Alice', 14)); // Good afternoon, Alice!
```

### Bash/Shell Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python readme_editor.py

# Run tests
python test_app.py
```

## Tables

| Feature | General Editor | Structured Editor |
|---------|----------------|-------------------|
| Text Editing | ✅ | ✅ |
| File Operations | ✅ | ✅ |
| Template Structure | ❌ | ✅ |
| Section Navigation | ❌ | ✅ |
| Live Preview | ✅ | ✅ |

### Complex Table

| Language | Extension | Syntax Highlighting | Use Case |
|----------|-----------|-------------------|----------|
| Python | `.py` | ✅ | Backend, Scripts, Data Science |
| JavaScript | `.js` | ✅ | Frontend, Node.js, Full-stack |
| TypeScript | `.ts` | ✅ | Type-safe JavaScript |
| Markdown | `.md` | ✅ | Documentation |
| JSON | `.json` | ✅ | Configuration, Data |

## Images and Media

![Markdown Logo](https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg)

*Note: Image rendering depends on network connectivity and file access.*

## Special Elements

### Keyboard Keys
Press `Ctrl` + `S` to save your work.
Use `F12` to toggle the preview panel.

### Horizontal Rules

Above this line...

---

Below this line...

### Highlighted Text
This is ==highlighted text== (if supported by extensions).

### Mathematical Expressions

Here's an inline equation: E = mc²

Block equation:
```
∑(i=1 to n) i = n(n+1)/2
```

## Advanced Markdown Features

### Definition Lists
Term 1
:   Definition 1

Term 2
:   Definition 2a
:   Definition 2b

### Footnotes
Here's a sentence with a footnote[^1].

[^1]: This is the footnote content.

### Abbreviations
The HTML specification is maintained by W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium

## Conclusion

This demo showcases the comprehensive markdown rendering capabilities of the README Editor's preview panel, including:

1. **Typography**: Headers, emphasis, strikethrough
2. **Links**: External, email, and reference links  
3. **Lists**: Ordered, unordered, and task lists
4. **Code**: Inline code and syntax-highlighted blocks
5. **Tables**: Simple and complex table layouts
6. **Special elements**: Blockquotes, horizontal rules, keyboard keys
7. **Advanced features**: Footnotes, definitions, abbreviations

The preview updates in real-time as you edit, making it easy to create professional documentation. 