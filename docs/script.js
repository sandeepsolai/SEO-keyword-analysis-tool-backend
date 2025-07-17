async function analyze() {
  const url = document.getElementById('url').value;
  const top_n = parseInt(document.getElementById('top_n').value);

  const response = await fetch("https://seo-keyword-analysis.onrender.com/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url, top_n })
  });

  const data = await response.json();
  const resultDiv = document.getElementById("results");
  resultDiv.innerHTML = "<h3>Results:</h3>";

  data.forEach(item => {
    resultDiv.innerHTML += `<p><strong>${item.word}</strong> (${item.count})<br>
      Prefix: ${item.prefix.join(", ")}<br>
      Suffix: ${item.suffix.join(", ")}</p>`;
  });
}
