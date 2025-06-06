import React, { useState } from "react";
import "./App.css";

function App() {
  const [userInput, setUserInput] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    const newChatLog = [...chatLog, { role: "user", content: userInput }];
    setChatLog(newChatLog);
    setUserInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: newChatLog }),
      });

      const data = await response.json();
      const botReply = { role: "assistant", content: data.response || "❌ لا يوجد رد" };

      setChatLog([...newChatLog, botReply]);
    } catch (error) {
      console.error("Error:", error);
      const errorMsg = { role: "assistant", content: "❌ حصل خطأ أثناء الاتصال بالخادم." };
      setChatLog([...newChatLog, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h2> سَمَى</h2>
      <div className="chat-box">
        {chatLog.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <strong>{msg.role === "user" ? "أنت" : "سَمَى"}:</strong> {msg.content}
          </div>
        ))}
        {loading && <div className="message assistant">سَمَى: ...</div>}
      </div>

      <div className="input-section">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="اكتب رسالتك هنا..."
        />
        <button onClick={handleSend}>إرسال</button>
      </div>
    </div>
  );
}

export default App;
