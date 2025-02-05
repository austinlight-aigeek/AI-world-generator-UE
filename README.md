# AI World Generator 🌍

This project is an **AI-powered world generation tool** built with **FastAPI (backend) and React (frontend)**.
It allows users to input a prompt (e.g., "Generate a futuristic city") and generates structured **JSON output** defining:

- **Terrain Type** (e.g., Desert, Urban, Mountain, etc.)
- **Key Buildings** (e.g., Skyscrapers, Markets, Factories, etc.)
- **Lighting Conditions** (e.g., Day/Night, Cyberpunk Neon, etc.)
- **NPC Behavior** (e.g., Crowded, Empty, Active Market, etc.)

The project integrates **OpenAI's GPT-4o** to intelligently classify and generate relevant world-building elements.

---

## 🏗️ How It Works

The AI-powered generator processes user input prompts and determines whether they are **relevant** to world generation.
If the prompt is not related to generating a city or a world, it will **reject the request**, ensuring accurate and meaningful outputs.
Additionally, it analyzes the prompt to determine if the city should be **small, medium, or large**, then generates an appropriate number of buildings based on the city size.
The output is also **contextually relevant**—if the prompt describes a modern city, it will generate a futuristic environment with skyscrapers and advanced technology, whereas if it describes an ancient city, it will create a historically accurate setting with castles, temples, and traditional markets.

### ✨ **Key Implementation Details**

✅ **Prompt Validation** - The AI ensures the input is relevant before proceeding.  
✅ **AI-Powered Classification** - Uses GPT-4o to categorize terrain, buildings, lighting, and NPC behavior.  
✅ **Dynamic Building Generation** - Adjusts the number and types of buildings based on the city type.  
✅ **Strict JSON Formatting** - The API provides structured JSON output for seamless integration into games or simulations.  
✅ **Error Handling** - Ensures smooth user experience by handling invalid prompts effectively.

---

## 🎮 How This Can Assist Game & Animation Content Creation

Traditionally, in video games, **players customize their world manually** by selecting from predefined options.  
However, this AI-powered world generator introduces a **new way of interacting with game environments**:

- 🏙️ **Procedural City Generation**: Instead of **handcrafting** game levels, developers can **generate cities dynamically** based on the player’s input.
- 🎨 **Creative Assistance for Artists**: Animators and game developers can use this AI tool to **quickly prototype environments**.
- 🎮 **Revolutionizing Character Customization**: Imagine **customizing a character with natural language** instead of clicking dropdowns.
  - **Example:** Instead of selecting "Elf" → "Blue Eyes" → "Long Hair", a player could type:
    > "Generate a fierce warrior with dragon tattoos and a cyberpunk outfit."
  - The AI would generate **a character matching this description**! 🚀
- 🌍 **Changing the Way We Play Games**: This technology could allow players to **design entire worlds using text prompts**, making games more immersive and personalized.

---

## 📂 Project Structure (main files)

```
AI-World-Generator
│── backend/                   # FastAPI Backend
│   ├── main.py                # Main FastAPI application
│   ├── config.json            # Predefined terrain, buildings, lighting, NPC behaviors
│   ├── requirements.txt       # Backend dependencies
│   ├── Dockerfile             # Docker setup for backend
│   └── .env.local             # Environment variables (API Keys, etc.)
│
│── frontend/                  # React Frontend
│   ├── src/                   # React source files
│   │   ├── App.js             # Main React Component
│   │   ├── index.js           # React entry point
│   │   ├── index.css          # Global styles
│   ├── public/                # Static assets
│   ├── package.json           # Frontend dependencies
│   ├── Dockerfile             # Docker setup for frontend
│   ├── .gitignore             # Ignore unnecessary files in frontend
│
│── README.md                  # Documentation
│── docker-compose.yml         # Container orchestration
│── .gitignore                 # # Ignore unnecessary files
```

---

## 🐳 Running the Project with Docker (Recommended)

For a **consistent and environment-independent** setup, it is recommended to **run the project using Docker**.  
This ensures the application works **across different OS and development environments** without dependency conflicts.

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/austinlight-aigeek/AI-world-generator-UE.git
cd AI-world-generator-UE
```

### **2️⃣ Run with Docker Compose**

```sh
docker-compose up --build
```

This will:

- Start **FastAPI Backend** on `http://localhost:8000`
- Start **React Frontend** on `http://localhost:3000`

To stop the containers:

```sh
docker-compose down
```

---

## 📡 API Endpoints

### **1️⃣ Generate a City (POST `/generate`)**

#### **Request**

```json
{
  "prompt": "Generate a futuristic city"
}
```

#### **Response**

```json
{
  "terrain": "urban",
  "lighting": "cyberpunk neon",
  "npc_behavior": "crowded",
  "buildings": ["skyscraper", "shopping mall", "hotel"]
}
```

---

## 🛠 Technologies Used

- **Backend:** FastAPI, Python 3, OpenAI API
- **Frontend:** React 18, Axios
- **Database:** JSON-based storage (config.json)
- **Deployment:** Docker, Docker Compose
- **Version Control:** Git, GitHub

---

## 📩 Contact

📧 **Email:** austinlight.fl@gmail.com  
🔗 **GitHub:** [Austin Light](https://github.com/austinlight-aigeek)

For any questions, feel free to reach out! 🚀
