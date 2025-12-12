# ☁️ Asynchronous Weather Aggregation and Filtering with browser-use

## Project Summary

This project presents a robust and asynchronous solution for gathering real-time weather data for different cities using the [`browser-use`](https://github.com/browser-use/browser-use/tree/main) agent framework. It extracts and parses weather information from an AI agent's execution history, and the final data is then filtered based on a temperature threshold.

---

## ⚙️ Setup and Installation

This project uses **`uv`** for dependency management and ensures the correct installation of the `browser-use` library and its required browser environment.

### 1. Initialize and Install Dependencies

First, ensure you have Python (version **3.11 or higher**) and the `uv` tool installed.

```bash
# 1. Create environment with uv
uv init

# 2. Install browser-use package (always latest)
uv add browser-use
uv sync
```

---

### 2. Configure API Key

Create a `.env` file in your project root:

```bash
# .env
BROWSER_USE_API_KEY=your-key
```

You can get your key from [Browser Use Cloud](https://cloud.browser-use.com/).

---

### 3. Install Chromium Browser

Install the required automated Chromium instance:

```bash
uvx browser-use install
```

---

### 4. Run the Application

```bash
uv run main.py
```

---

## 🚀 Architectural Flow

The application executes in a clear, three-stage pipeline:

---

### 1. Concurrent Data Fetching (`get_city_weather`)

- A `browser-use` Agent is assigned a strict task:  
  **Search for the weather of a specific city and return the result ONLY in a JSON format.**

- `asyncio.gather` launches all city requests **in parallel**, drastically improving speed.

---

### 2. Robust Data Extraction (`extract_clean_json_from_result`)

This utility solves the main problem: **extracting clean JSON from noisy agent logs.**

- A regex such as:

  ```
  r"\{'city':.*?\}"
  ```

  is used to locate the final dictionary-like JSON block.

- Because the block uses **single quotes**, standard `json.loads()` fails.

- So it is safely converted using:

  ```python
  ast.literal_eval()
  ```

- All extracted JSON dictionaries are appended into `all_clean_data`.

---

### 3. Filtering and Presentation  
(`filter_warm_cities` and `if __name__ == "__main__"`)

- The filtering step keeps only cities where:

  ```
  temperature > 10°C
  ```

- The script prints:
  1. **All extracted clean JSON**  
  2. **Filtered warm cities**  
  3. **Final list of warm city names**

---

## 📝 Example Output Structure

```
## Clean JSON for ALL Cities (Extracted) ##
{
    "city": "Berlin",
    "temperature": 8,
    "weather_summary": "Clear"
}
{
    "city": "Amsterdam",
    "temperature": 10,
    "weather_summary": "Cloudy"
}
{
    "city": "Pune",
    "temperature": 23,
    "weather_summary": "Sunny"
}

## Filtered Cities (Temp > 10°C) ##
[
    {"city": "Amsterdam", "temperature": 10, "weather_summary": "Cloudy"},
    {"city": "Pune", "temperature": 23, "weather_summary": "Sunny"}
]

Cities with temp above 10°C: ['Pune']
```
