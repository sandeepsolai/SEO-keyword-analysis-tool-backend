async function analyze() {
  const url = document.getElementById('url').value.trim();
  const top_n = parseInt(document.getElementById('top_n').value);

  if (!url) {
    alert("Please enter a website URL");
    return;
  }
  if (!top_n || top_n <= 0) {
    alert("Please enter a valid number for Top N words");
    return;
  }

  const resultDiv = document.getElementById("results");
  resultDiv.innerHTML = "<p><em>Analyzing...</em></p>";

  try {
    const response = await fetch("https://seo-keyword-analysis.onrender.com/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, top_n })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    if (data.length === 0) {
      resultDiv.innerHTML = "<p>No significant words found. Try another URL.</p>";
      return;
    }

    // Build the result HTML string
    let html = `<h2>Top ${top_n} Words in <em>${url}</em>:</h2>`;

    data.forEach(item => {
      html += `
        <div class="word-block">
          <h3>${capitalize(item.word)} <span class="count">(${item.count})</span></h3>
          
          <div class="context-block">
            <strong>Prefix Examples:</strong>
            ${item.prefix.length > 0 ? `<ul>${item.prefix.map(p => `<li>${escapeHtml(p)}</li>`).join('')}</ul>` : '<p><em>None</em></p>'}
          </div>

          <div class="context-block">
            <strong>Suffix Examples:</strong>
            ${item.suffix.length > 0 ? `<ul>${item.suffix.map(s => `<li>${escapeHtml(s)}</li>`).join('')}</ul>` : '<p><em>None</em></p>'}
          </div>
        </div>
      `;
    });

    resultDiv.innerHTML = html;

  } catch (error) {
    resultDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
  }
}

// Helper to capitalize first letter
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// Helper to escape HTML entities (to avoid injection issues)
function escapeHtml(text) {
  return text.replace(/[&<>"']/g, function (m) {
    switch (m) {
      case '&': return '&amp;';
      case '<': return '&lt;';
      case '>': return '&gt;';
      case '"': return '&quot;';
      case "'": return '&#39;';
      default: return m;
    }
  });
}
