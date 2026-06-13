# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## Overview

FitFindr is a multi-tool AI agent that helps users search for secondhand clothing, style the selected item with their wardrobe, and generate a short shareable outfit caption. The agent uses three tools: one for searching listings, one for suggesting outfits, and one for creating a fit card.


## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```



## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install python-dotenv groq gradio pytest
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_key_here
```

Run the app:

```bash
python app.py
```
## Tool Inventory

| Tool | Inputs | Output | Purpose |
|------|--------|--------|---------|
| `search_listings` | `description` (str), `size` (str or None), `max_price` (float or None) | List of matching listing dictionaries | Searches the mock listings dataset for items matching the user request. |
| `suggest_outfit` | `new_item` (dict), `wardrobe` (dict) | Outfit suggestion string | Suggests how to style the selected item with the user's wardrobe. |
| `create_fit_card` | `outfit` (str), `new_item` (dict) | Caption string | Creates a short social-media-style outfit description. |

---
## Planning Loop

The agent starts by parsing the user's natural language query into `description`, `size`, and `max_price`.

Then it calls:

```python
search_listings(description, size, max_price)
```

If no listings are found, the agent stores an error message in `session["error"]` and stops. It does not call the outfit or fit card tools.

If listings are found, the agent selects the first result and stores it in `session["selected_item"]`. Then it passes that item and the wardrobe into `suggest_outfit`.

After an outfit suggestion is created, the agent stores it in `session["outfit_suggestion"]` and passes it into `create_fit_card`. The final session contains the selected item, outfit suggestion, fit card, and any error message.

---
## State Management

The agent uses a session dictionary to track information across tool calls.

The session stores:

- `query`
- `parsed`
- `search_results`
- `selected_item`
- `wardrobe`
- `outfit_suggestion`
- `fit_card`
- `error`

This allows information from one tool to flow into the next tool without asking the user to re-enter it.

---

## Error Handling

| Tool | Failure Mode | Agent Response |
|------|--------------|----------------|
| `search_listings` | No matching listings | Returns a helpful message asking the user to broaden the description, increase the price, or remove the size filter. |
| `suggest_outfit` | Empty wardrobe | Returns general styling advice using common wardrobe basics instead of crashing. |
| `create_fit_card` | Empty outfit string | Returns `"I need an outfit suggestion before I can create a fit card."` |

### Example Failure

Query:

```text
designer ballgown size XXS under $5
```

Response:

```text
I could not find any matching listings. Try using a broader description, increasing your max price, or removing the size filter.
```
---

## Example Interaction

### User Query

```text
vintage graphic tee under $30
```

### Top Listing Found

```text
Title: Y2K Baby Tee — Butterfly Print
Price: $18.0
Platform: depop
Size: S/M
Condition: excellent
```

### Outfit Suggestion

```text
Pair the Y2K Baby Tee with baggy straight-leg jeans and chunky white sneakers. Add a vintage black denim jacket for a relaxed streetwear look.
```

### Fit Card

```text
Just scored the cutest Y2K Baby Tee — Butterfly Print on Depop for $18 and I'm obsessed. Paired it with baggy jeans and chunky sneakers for an easy everyday fit.
```

---

## Query Interface

The project includes a Gradio web interface.

### Inputs

- User query text box
- Wardrobe selector:
  - Example wardrobe
  - Empty wardrobe (new user)

### Outputs

- Top listing found
- Outfit suggestion
- Fit card caption

Run the interface:

```bash
python app.py
```

---

## Failure Mode Testing

### Test 1: No Matching Listings

Command:

```bash
python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"
```

Result:

```text
[]
```

Agent Response:

```text
I could not find any matching listings. Try using a broader description, increasing your max price, or removing the size filter.
```

### Test 2: Empty Wardrobe

Command:

```bash
python -c "from tools import search_listings, suggest_outfit; from utils.data_loader import get_empty_wardrobe; results=search_listings('vintage graphic tee', size=None, max_price=50); print(suggest_outfit(results[0], get_empty_wardrobe()))"
```

Result:

The tool generated general styling advice instead of crashing.

### Test 3: Empty Outfit Input

Command:

```bash
python -c "from tools import search_listings, create_fit_card; results=search_listings('vintage graphic tee', size=None, max_price=50); print(create_fit_card('', results[0]))"
```

Result:

```text
I need an outfit suggestion before I can create a fit card.
```

---

## Architecture


                                    User Query
                                        |
                                        
                                    Planning Loop
                                        |
                                        |-- Parse description, size, max_price
                                        |
                                        
                                    search_listings(description, size, max_price)
                                        |
                                        |-- No results
                                        |       |
                                        |       
                                        |   Session error
                                        |       |
                                        |       
                                        |   Return error message
                                        |
                                        |-- Results found
                                                |
                                                
                                        Session selected_item
                                                |
                                                
                                    suggest_outfit(selected_item, wardrobe)
                                                |
                                                
                                        Session outfit_suggestion
                                                |
                                                
                                    create_fit_card(outfit_suggestion, selected_item)
                                                |
                                                
                                        Session fit_card
                                                |
                                                
                                    Return results to user


---

## Testing

Run all tests:

```bash
pytest tests/
```

Result:

```text
5 passed
```

The tests verify:

- successful listing search
- no-results listing search
- price filtering
- empty wardrobe handling
- empty outfit handling

---

## Spec Reflection

### One way the spec helped

The planning document helped define the inputs, outputs, and failure modes for each tool before implementation. This made the planning loop easier to implement because each tool had a clearly defined responsibility.

### One way the implementation diverged from the spec

The original plan described parsing user queries in a general way. During implementation, I used regular expressions to extract size and maximum price because they were simple and reliable for the mock dataset.

---

## AI Usage

### Instance 1

**What I gave the AI:**

The Tool 1 specification from planning.md, including the inputs, return value, and failure mode.

**What it produced:**

Python code for `search_listings()` that loads listings, filters by size and price, scores keyword overlap, and returns matching items.

**What I changed or overrode:**

I tested the implementation using matching and no-result queries to verify the filtering and ranking behavior.

### Instance 2

**What I gave the AI:**

The Planning Loop, State Management, and Architecture sections from planning.md.

**What it produced:**

Code for `run_agent()` that passes state between tools using a session dictionary.

**What I changed or overrode:**

I corrected indentation issues, verified state passing between tools, and confirmed that the agent stops early when no listings are found.

---

