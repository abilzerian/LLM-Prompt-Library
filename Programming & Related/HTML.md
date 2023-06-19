# HTML

```HTML
<p>As an expert front end developer, I recommend the following practices for clean, optimized HTML:</p>

<h2>Use semantic HTML5 elements</h2>

<header>
  <nav>
  <main>
  <section>
  <article>
  <aside>
  <footer>

<h2>Write efficient, accessible markup</h2>

<img alt="..." />
<svg> / <canvas>
<video controls>
<audio controls>
<meta name="description" content="...">
<a href="..."><span>Link text</span></a>

<h2>Keep your code maintainable</h2>

<p>Use:</p>  
<ul>
  <li>Indentation for nested elements</li>
  <li>Comments where needed</li>
  <li>Break up long code lines for readability</li>
  <li>Use CSS for styling - don't include style attributes in HTML</li>
</ul>

<h2>Validate and optimize your HTML</h2>

<p>Use the W3C validator to check your code and:</p>
<ul>
  <li>Remove unused/empty elements</li>
  <li>Move inline CSS to an external stylesheet</li>
  <li>Minify HTML/CSS/JS before deployment</li>
  <li>Gzip/compress files for faster loading</li>
</ul>

<h2>Stay up-to-date with HTML5</h2>

<p>Use new HTML5 elements and APIs like:</p>

<details>/<summary> for expandable content
<picture> for responsive images
ARIA roles/attributes for accessibility
New form input types like email/url/range/date/etc.

<p>Here is an example HTML code snippet following best practices:</p>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Example</title>
</head>
<body>
  <h1>Welcome</h1>
  <p>This <span>website</span> was built using <em>HTML5</em> and <strong>CSS3</strong>.</p>

  <header>
    <nav>
      <ul>
        <li><a href="about.html">About</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section>
      <h2>Articles</h2>
      <article>
        <h3>First article</h3>
        <p>...</p>
      </article>
      <article>...</article>
    </section>
    <aside>Related links</aside>
  </main>

  <footer>&copy; 2020 My Website</footer>
</body>
</html>
```
