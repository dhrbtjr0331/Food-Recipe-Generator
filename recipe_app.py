import requests

def get_user_input():
    food_name = input("Enter the name of the food you want to cook: ")
    return food_name

def fetch_id_from_api(food_name):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
    querystring = {"query": food_name, "number": 1}

    headers = {
        "X-RapidAPI-Key": "YOUR_ACTUAL_API_KEY_HERE",  # Replace with your real API key.
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]['id']
        else:
            print("No recipes found for that food name.")
            return None
    else:
        print("Failed to fetch recipe ID. Please try again.")
        return None

def fetch_recipe_from_api(recipe_id):
    if recipe_id is None:
        return None

    url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/information"

    headers = {
        "X-RapidAPI-Key": "YOUR_ACTUAL_API_KEY_HERE",  # Replace with your real API key.
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch recipe details. Please try again.")
        return None

def parse_recipe_data(response_data):
    analyzed_instructions = response_data.get('analyzedInstructions', [])
    instructions_output = []

    for instruction_set in analyzed_instructions:
        name = instruction_set.get('name', '')  
        steps = instruction_set.get('steps', [])
        
        instruction_set_output = {'name': name, 'steps': []}

        for step in steps:
            number = step.get('number', '')
            step_text = step.get('step', '')
            ingredients = step.get('ingredients', [])
            equipment = step.get('equipment', [])
            
            step_output = {'number': number, 'step': step_text}
            
            if ingredients:
                step_output['ingredients'] = [ingredient['localizedName'] for ingredient in ingredients]
            
            if equipment:
                step_output['equipment'] = [eq['localizedName'] for eq in equipment]
            
            instruction_set_output['steps'].append(step_output)
        
        instructions_output.append(instruction_set_output)
    
    return instructions_output

def main():
    while True:
        food_name = get_user_input()
        if food_name.lower() == 'exit':
            break
        
        recipe_id = fetch_id_from_api(food_name)
        response_data = fetch_recipe_from_api(recipe_id)
     
        if response_data:
            recipe_instructions = parse_recipe_data(response_data)

            # Print the instructions
            for instruction_set in recipe_instructions:
                print(f"Instruction Set: {instruction_set['name']}\n")
                for step in instruction_set['steps']:
                    print(f"Step {step['number']}: {step['step']}")
                    if 'ingredients' in step:
                       print(f"Ingredients: {', '.join(step['ingredients'])}")
                    if 'equipment' in step:
                        print(f"Equipment: {', '.join(step['equipment'])}")
                    print()
        else:
            print("Recipe not found. Please try again.")

main()

