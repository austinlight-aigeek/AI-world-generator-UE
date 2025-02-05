import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("Generate a futuristic city");
  const [response, setResponse] = useState(null);

  const handleGenerate = async () => {
    try {
      const res = await axios.post("http://localhost:8000/generate", {
        prompt,
      });
      setResponse(res.data);
    } catch (error) {
      console.error("Error generating world:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>AI World Generator 🌍</h1>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        style={{ width: "400px", padding: "10px" }}
      />
      <button
        onClick={handleGenerate}
        style={{ marginLeft: "10px", padding: "10px" }}
      >
        Generate
      </button>
      {response && (
        <pre style={{ marginTop: "20px", textAlign: "left" }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
