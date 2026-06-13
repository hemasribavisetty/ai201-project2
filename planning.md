# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
Searches the mock secondhand listings dataset for items that match the user's requested description, size, and maximum price. It filters listings and returns the best matching items for the agent to consider.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): A natural language description of the item the user wants, such as "vintage graphic tee" or "black denim jacket".
- `size` (str): The user's requested size, such as "S", "M", "L", or None if the user does not specify a size.
- `max_price` (float): The maximum price the user wants to pay.

**What it returns:**
A list of matching listing dictionaries. Each listing may contain fields such as id, title, description, category, style_tags, size, condition, price, colors, brand, and platform.

**What happens if it fails or returns nothing:**
If no listings match, the tool returns an empty list. The agent stops the workflow and tells the user that no matching listings were found. It should suggest trying a broader description, higher max price, or no size filter.

---

### Tool 2: suggest_outfit

**What it does:**
Takes the selected secondhand item and the user's wardrobe, then suggests one or more ways to style the new item with clothing the user already owns.

**Input parameters:**

- `new_item` (dict): The listing selected from search_listings. It contains item information such as title, category, colors, price, size, and platform.
- `wardrobe` (dict): The user's wardrobe data, including a list of clothing items the user already owns.

**What it returns:**
A string containing a complete outfit suggestion. The response should mention the selected item and explain what wardrobe pieces to pair it with.

**What happens if it fails or returns nothing:**
If the wardrobe is empty or very small, the tool should still return general styling advice using the new item. It should not crash or return an empty response.

---

### Tool 3: create_fit_card

**What it does:**
Creates a short, shareable outfit description based on the selected item and outfit suggestion. The fit card should sound like a social media caption rather than a technical product description.

**Input parameters:**

- `outfit` (...): The outfit suggestion produced by suggest_outfit.
- `new_item` (dict): The selected listing from search_listings.

**What it returns:**
A short caption-style string describing the outfit and new item. It should vary depending on the item and outfit.

**What happens if it fails or returns nothing:**
If the outfit string is missing or empty, the tool returns a clear error message such as "I need an outfit suggestion before I can create a fit card." It should not crash.

---

### Additional Tools (if any)
No additional tools are planned for the base version of this project.

---

## Planning Loop

**How does your agent decide which tool to call next?**
The agent starts by reading the user's request and extracting the desired item description, size, max price, and wardrobe/style context.

First, the agent calls search_listings(description, size, max_price). If the search returns an empty list, the agent stores an error message in the session and stops. It does not call suggest_outfit or create_fit_card.

If search results are found, the agent selects the top result and stores it in the session as selected_item. Then it calls suggest_outfit(selected_item, wardrobe).

If suggest_outfit returns a valid outfit suggestion, the agent stores it as outfit_suggestion. Then it calls create_fit_card(outfit_suggestion, selected_item).

The agent is done when it has either returned an error message or produced a selected item, outfit suggestion, and fit card.

---

## State Management

**How does information from one tool get passed to the next?**
The agent uses a session dictionary to pass information between tools during a single interaction.

The session stores:

- query: the original user request
- description: the item description extracted from the user request
- size: the requested size
- max_price: the user's maximum price
- wardrobe: the wardrobe data used for styling
- search_results: the list returned by search_listings
- selected_item: the top listing selected by the agent
- outfit_suggestion: the result returned by suggest_outfit
- fit_card: the result returned by create_fit_card
- error: an error message if the workflow cannot continue

This makes state available across tools without requiring the user to re-enter information.

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool |               Failure mode       |                       Agent response |
|-----------------|-------------|----------------|
| search_listings | No results match the query| The agent returns a message such as: "I could not find any matching    listings. Try using a broader description, increasing your max price, or removing the size filter."

suggest_outfit	   |       Wardrobe is empty	  |     The tool returns general outfit advice based on the selected item instead of crashing.
create_fit_card  |	Outfit input is missing or incomplete | The tool returns: "I need an outfit suggestion before I can create a fit card."
---

## Architecture


                              User query
                              |
                              
                              Planning Loop
                              |
                              |-- Extract description, size, max_price, wardrobe context
                              |
                              
                              search_listings(description, size, max_price)
                              |
                              |-- results = []
                              |       |
                              |       
                              |   Session error = "No listings found"
                              |       |
                              |       
                              |   Return error to user
                              |
                              |-- results found
                                        |
                                        
                              Session selected_item = results[0]
                                        |
                                        
                              suggest_outfit(selected_item, wardrobe)
                                        |
                                        
                              Session outfit_suggestion = outfit response
                                        |
                                        
                              create_fit_card(outfit_suggestion, selected_item)
                                        |
                                        
                              Session fit_card = caption
                                        |
                                        
                              Return selected item + outfit suggestion + fit card to user

---

## AI Tool Plan

**Milestone 3 — Individual tool implementations:**
I will use ChatGPT to help implement each tool in tools.py one at a time. For search_listings, I will provide the Tool 1 specification and ask it to use load_listings() from utils/data_loader.py. I will verify that the generated code filters by description, size, and max price and returns an empty list instead of crashing when no listings match.

For suggest_outfit, I will provide the Tool 2 specification and ask ChatGPT to generate a Groq-powered styling function. I will verify that it handles both the example wardrobe and the empty wardrobe.

For create_fit_card, I will provide the Tool 3 specification and ask ChatGPT to generate a caption-style function. I will verify that it returns an error message when the outfit input is empty and produces varied captions for different inputs.

**Milestone 4 — Planning loop and state management:**
I will provide ChatGPT with the Planning Loop, State Management, Error Handling, and Architecture sections. I will ask it to help implement run_agent() in agent.py using the session dictionary. I will verify that the agent stops early when search_listings returns no results and does not call the later tools in that case.
---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
The agent extracts:
description = "vintage graphic tee"
size = None or "M" if size is provided
max_price = 30.0
wardrobe/style context = baggy jeans and chunky sneakers

Then the agent calls:

search_listings("vintage graphic tee", size=None, max_price=30.0)

If matching listings are found, the agent stores them in session["search_results"].

**Step 2:**
The agent selects the first matching listing from the results and stores it as:

session["selected_item"] = search_results[0]

Then it calls:

suggest_outfit(selected_item, wardrobe)

This returns a styling suggestion using the selected item and the user's wardrobe or stated style.

**Step 3:**
The agent stores the outfit suggestion as:

session["outfit_suggestion"]

Then it calls:

create_fit_card(outfit_suggestion, selected_item)

This returns a short shareable caption for the outfit.
**Final output to user:**
The user sees:

- The selected secondhand item
- A suggested outfit using that item
- A short fit card caption
- An error message instead if no matching listings are found
