import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("Generate a futuristic city");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);
    try {
      const res = await axios.post("http://localhost:8000/generate", {
        prompt,
      });

      if (res.data.error) {
        setError(res.data.error); // Backend returned an error message
      } else {
        setResponse(res.data); // Valid response
      }
    } catch (error) {
      setError("Failed to connect to the server. Please try again.");
      console.error("Error generating world:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>AI World Generator 🌍</h1>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        style={{
          width: "400px",
          padding: "10px",
          borderRadius: "5px",
          border: "1px solid #ccc",
        }}
      />
      <button
        onClick={handleGenerate}
        disabled={loading}
        style={{
          marginLeft: "10px",
          padding: "10px",
          borderRadius: "5px",
          backgroundColor: loading ? "#ccc" : "#007bff",
          color: "white",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Generating..." : "Generate"}
      </button>

      {loading && (
        <p style={{ marginTop: "20px", fontSize: "18px" }}>
          ⏳ Generating world, please wait...
        </p>
      )}

      {/* Error message display */}
      {error && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "20px",
          }}
        >
          <div
            style={{
              color: "red",
              marginTop: "10px",
              fontSize: "16px",
              padding: "10px",
              backgroundColor: "#ffdddd",
              borderRadius: "5px",
              border: "1px solid red",
              display: "inline-block",
            }}
          >
            ❌ {error}
          </div>
        </div>
      )}

      {/* Valid response display */}
      {response && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "20px",
          }}
        >
          <pre
            style={{
              textAlign: "left",
              backgroundColor: "#f4f4f4",
              padding: "20px",
              borderRadius: "5px",
              width: "40%",
              whiteSpace: "pre-wrap",
              wordWrap: "break-word",
              boxShadow: "0px 0px 10px rgba(0, 0, 0, 0.1)",
            }}
          >
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
