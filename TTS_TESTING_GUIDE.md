# 🔊 TTS TESTING GUIDE - Step by Step

## 🎯 **HOW TO TEST TEXT-TO-SPEECH**

### **Step 1: Test TTS Support**
1. **Click the green "🔊 Test" button** in the header (next to the TTS toggle)
2. You should hear: "Hello! Text to speech is working correctly. This is a test from Aditya AI."
3. Check browser console (F12) for any error messages

### **Step 2: Enable Auto-TTS**
1. **Click the 🔊 button** (should be enabled by default now)
2. The button should show **🔊** (enabled) or **🔇** (disabled)
3. When enabled, the button should not be faded

### **Step 3: Test AI Response Speech**
1. **Type a message** like "Hello, how are you?"
2. **Press Enter or click Send**
3. **Wait for AI response** - it should automatically be spoken
4. Check browser console for debug messages

### **Step 4: Test Voice Input + Speech Output**
1. **Click the 🎤 microphone button**
2. **Speak your question** (e.g., "What is artificial intelligence?")
3. **The AI response should be spoken back to you**

### **Step 5: Manual Controls**
1. Each AI message has **🔊 Play** and **⏹️ Stop** buttons
2. Click **🔊 Play** to manually speak any message
3. Click **⏹️ Stop** to stop current speech

## 🐛 **TROUBLESHOOTING**

### **If TTS doesn't work:**

1. **Browser Support**: Make sure you're using Chrome, Firefox, Safari, or Edge
2. **User Interaction**: Click the "🔊 Test" button first (browsers require user interaction)
3. **Audio Settings**: Check your system volume and audio output
4. **Console Errors**: Open F12 → Console tab and look for errors

### **Common Browser Issues:**

- **Chrome/Edge**: Should work immediately
- **Firefox**: May need the test button clicked first
- **Safari**: Uses system voices, usually works well
- **Mobile Safari**: Should work with system TTS

## 🎵 **EXPECTED BEHAVIOR**

### **✅ What Should Happen:**
1. **Test Button**: Speaks test message immediately
2. **Auto-Speech**: AI responses automatically spoken when TTS enabled
3. **Visual Feedback**: TTS button pulses blue when speaking
4. **Manual Controls**: Play/Stop buttons work on each message
5. **Console Logs**: Debug messages showing TTS activity

### **❌ If Nothing Happens:**
1. Check browser console for errors
2. Try different browser
3. Check system audio settings
4. Test with different message length

## 🌟 **FEATURES WORKING:**

- ✅ **Auto-speech for AI responses**
- ✅ **Manual play/stop controls** 
- ✅ **TTS toggle on/off**
- ✅ **Test button for debugging**
- ✅ **Visual feedback when speaking**
- ✅ **Voice input + speech output combination**
- ✅ **Text cleaning for better speech**
- ✅ **Persistent settings**

## 🚀 **FULL WORKFLOW TEST:**

1. **Open**: http://localhost:3001
2. **Click "🔊 Test"** → Should speak test message
3. **Enable TTS** → Click 🔊 button (should be solid, not faded)
4. **Type question** → "Explain quantum computing"
5. **Send message** → AI response should be automatically spoken
6. **Try voice input** → Click 🎤, speak question, get spoken response
7. **Manual control** → Use play/stop buttons on messages

If all steps work, the TTS feature is fully functional! 🎉
