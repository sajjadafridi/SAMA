import React, { useState } from "react";

const Chat = () => {
  const [userInput, setUserInput] = useState("");
  const [chatLog, setChatLog] = useState([]);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    const newChatLog = [...chatLog, { role: "user", content: userInput }];

    setChatLog(newChatLog);
    setUserInput("");

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: newChatLog }),
      });

      const data = await response.json();
      const botReply = { role: "assistant", content: data.response };

      setChatLog([...newChatLog, botReply]);
    } catch (error) {
      console.error("Error talking to chatbot:", error);
    }
  };

  return (
    <div>
      <h2> سَمَى</h2>
      <div
        style={{
          maxHeight: "300px",
          overflowY: "auto",
          border: "1px solid #ccc",
          padding: "10px",
          marginBottom: "10px",
        }}
      >
        {chatLog.map((msg, idx) => (
          <div
            key={idx}
            style={{ textAlign: msg.role === "user" ? "right" : "left" }}
          >
            <strong>{msg.role === "user" ? "أنت" : "سَمَى"}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="اكتب هنا..."
        style={{ width: "80%", marginRight: "10px" }}
      />
      <button onClick={handleSend}>إرسال</button>
    </div>
  );
};

export default Chat;
