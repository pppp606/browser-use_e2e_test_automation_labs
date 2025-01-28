import argparse
import asyncio
import glob
import json
import os
import re

from datetime import datetime
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("URL")
user_id = os.getenv("USER_ID")
password = os.getenv("PASSWORD")
scenario_language = os.getenv("SCENARIO_LANGUAGE")

async def create_scenario():
  site_structure_task = f"""
Analyze the website starting from {url}. Identify and output:
1. All accessible pages and subpages within the domain ({url}). Include dynamically loaded content and hidden links.
2. For each page, provide the purpose or functionality in concise terms.
3. Ensure the analysis includes:
   - Static links
   - Dynamic or JavaScript-driven links
   - Form actions and submission endpoints
   - API endpoints if visible
4. For pages with similar structures but different parameters (e.g., query strings like ?id=), group them under one representative page.

## Output JSON Format:
[
  {{ "path": "<path or URL>", "purpose": "<brief description of the page's purpose or functionality>" }},
  ...
]

## Login Information
- id: {user_id}
- password: {password}
"""

  site_structure_result = await Agent(
    task=site_structure_task,
    llm=ChatOpenAI(model="gpt-4o", temperature=0.8),
  ).run()

  site_structure_content = extract_content(site_structure_result)

  if isinstance(site_structure_content, str):
    site_structure = json.loads(site_structure_content)
  else:
    print("site_structure_content is not a string, converting to string.")
    site_structure = json.loads(str(site_structure_content))

  all_scenarios = []

  for page in site_structure:
    page_path = page.get("path")
    page_purpose = page.get("purpose")

    if not page_path or not page_purpose:
      continue

    scenario_task = f"""
Generate exhaustive test scenarios for the following page:
- Page: {page_path}
  Purpose: {page_purpose}

For this page, include all possible user actions, such as:
  - Form submissions
  - Button clicks
  - Dropdown selections
  - Interactions with modals or dynamic elements

Test both expected behaviors and edge cases for each action.
Output format:
path: {page_path},
actions:
  - test: <description of action>,
    expect: <expected result>,
  - test: <description of action>,
    expect: <expected result>,

The output must be written in {scenario_language}.

## Root URL
{url}

## Login Information
- id: {user_id}
- password: {password}
"""

    result = await Agent(
        task=scenario_task,
        llm=ChatOpenAI(model="gpt-4o", temperature=0.8, max_tokens=5000),
    ).run()

    scenario_content = extract_content(result)
    all_scenarios.append(scenario_content)

  final_scenario_output = "\n\n".join(all_scenarios)
  print(final_scenario_output)
  save_result_to_file("./scenario", final_scenario_output)

async def create_code():
  url = os.getenv("URL")
  latest_file = get_latest_file("./scenario", "*.log")
  if not latest_file:
      print("No log files found.")
      return

  latest_file_content = ""
  with open(latest_file, "r", encoding="utf-8") as file:
      latest_file_content = file.read()


  for scenario in latest_file_content.strip().split("\n\n"):
    task = f"""
Based on the provided URL and scenario, generate the necessary test code for end-to-end testing.
The code should be written using Jest and Playwright, including all necessary imports and configurations.
Ensure the output is in a fully executable state, ready to be copied and run immediately.
Do not include any markdown code formatting. Output only the code.

## URL
{url}

## Login Information
- id: {user_id}
- password: {password}

## Scenario
{scenario}
"""
    print(task)

    path = scenario.split("\n")[0].split(":")[1].strip().replace(",", "")
    file_name = generate_filename(path)

    result = await Agent(
      task=task,
      llm=ChatOpenAI(model="gpt-4o", temperature=0.8),
    ).run()

    result_content = extract_content(result)
    print(result_content)

    save_test_file("./tests", file_name, result_content)


def generate_filename(path):
  if path == "/":
    return "index.test.js"
  else:
    sanitized_path = path.strip("/")
    sanitized_path = re.sub(r"[/]", "_", sanitized_path)
    sanitized_path = re.sub(r"\..*", "", sanitized_path)
    return f"{sanitized_path}.test.js"

def extract_content(result):
  if callable(result.final_result):
      content = result.final_result()
      if isinstance(content, str):
          return content
  return ""

def save_result_to_file(directory: str, content: str):
  abs_directory = os.path.abspath(directory)
  os.makedirs(abs_directory, exist_ok=True)

  timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
  file_path = os.path.join(abs_directory, f"{timestamp}.log")
  print(f"File path: {file_path}")

  with open(file_path, "w", encoding="utf-8") as file:
    file.write(content)

  print(f"Result saved to {file_path}")

def save_test_file(directory: str, file_name: str, content: str):
  abs_directory = os.path.abspath(directory)
  os.makedirs(abs_directory, exist_ok=True)

  file_path = os.path.join(abs_directory, f"{file_name}")
  print(f"File path: {file_path}")

  with open(file_path, "w", encoding="utf-8") as file:
    file.write(content)

  print(f"Test file saved to {file_path}")

def get_latest_file(directory: str, pattern: str) -> str:
  files = glob.glob(os.path.join(directory, pattern))
  if not files:
      return None
  latest_file = max(files, key=os.path.getmtime)
  return latest_file

def main():
  parser = argparse.ArgumentParser(description="Choose which function to execute.")
  parser.add_argument(
    "option",
    choices=["scenario", "code"],
    help="Choose 'scenario' to create a scenario or 'code' to create code."
  )
  args = parser.parse_args()

  if args.option == "scenario":
    asyncio.run(create_scenario())
  elif args.option == "code":
    asyncio.run(create_code())

# scenario -> create_scenario()
# code -> create_code()
if __name__ == "__main__":
  main()




