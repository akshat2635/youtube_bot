document.getElementById("askBtn").addEventListener("click", async () => {
  const question = document.getElementById("question").value.trim();
  const responseDiv = document.getElementById("response");
  responseDiv.innerHTML = "<em>Thinking...</em>";

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    const url = new URL(tab.url);
    const videoId = url.searchParams.get("v");

    if (!videoId) {
      responseDiv.innerHTML =
        "<strong>Error:</strong> Not a YouTube video URL.";
      return;
    }

    const response = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: videoId, question }),
    });

    const data = await response.json();
    const answer = data.answer || "No response.";

    // Convert line breaks into HTML line breaks
    const formatted = answer
      .replace(/\n/g, "<br>") // newline to <br>
      .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>") // **bold** markdown
      .replace(/\*(.*?)\*/g, "<i>$1</i>"); // *italic* markdown

    responseDiv.innerHTML = formatted;
  } catch (err) {
    console.error("Error:", err);
    responseDiv.innerHTML =
      "<strong>Error:</strong> Could not talk to the agent.";
  }
});
