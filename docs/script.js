async function analyze() {
    const url = document.getElementById("url").value;
    const top_n = document.getElementById("top_n").value;
    const resultDiv = document.getElementById("result");
    resultDiv.innerText = "Analyzing...";

    const response = await fetch("https://seo-keyword-analysis.onrender.com", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url, top_n: parseInt(top_n) })
    });

    const data = await response.json();
    let output = `🔍 Top ${top_n} Words:\n\n`;
    data.forEach((item, index) => {
        output += `${index + 1}. ${item.word} - ${item.count}\n`;
        output += `   Prefix:\n${item.prefix.length ? item.prefix.join("\n") : "-----------"}\n`;
        output += `   Suffix:\n${item.suffix.length ? item.suffix.join("\n") : "-----------"}\n\n`;
    });
    resultDiv.innerText = output;
}
