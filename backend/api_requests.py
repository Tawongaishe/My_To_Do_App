import requests

def get_lists():
    api_url = 'http://localhost:5000/api/lists'  # Replace with your actual API URL
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        lists = response.json()
        return lists
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []
    

def get_tasks(list_id):
    api_url = f'http://localhost:5000/api/lists/{list_id}'  # Replace with your actual API URL
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        tasks = data['tasks']  # Extract the tasks from the JSON response
        return tasks
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []