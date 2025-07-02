import React, { useState, useRef } from "react";
import "./App.css";

const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const recognitionRef = useRef(null);

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!recognitionRef.current && SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = "ar-SA";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      setUserInput(speechResult);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
    };

    recognitionRef.current = recognition;
  }

  const startListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
      console.log("Listening started...");
    } else {
      alert("متصفحك لا يدعم التعرف على الصوت");
    }
  };

  return (
    <div>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="اكتب أو تكلم هنا"
      />
      <button onClick={startListening}>🎤 تكلم</button>
    </div>
  );
};

export default Chatbot;
