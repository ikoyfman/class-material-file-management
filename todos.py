import json
from pathlib import Path
from datetime import date

class TodoManager(object):
    STATUS_ALL = 'all'
    STATUS_DONE = 'done'
    STATUS_PENDING = 'pending'
    CATEGORY_GENERAL = 'general'

    def __init__(self, base_todos_path, create_dir=True):
        self.base_todos_path = base_todos_path
        self.path = Path(self.base_todos_path)
        # continue here
        if create_dir:
            self.path.mkdir(exist_ok=True)
    
    
    def list(self, status=STATUS_ALL, category=CATEGORY_GENERAL):
        results = {}
        for json_file in self.path.glob('*.json'):
            
            with open(json_file,'r') as file:
                data = json.load(file)

                if data['category_name'] not in results.keys():
                    results[data['category_name']] = []
                
                for todo in data['todos']:
                    if status == self.STATUS_ALL or todo['status'] == status:
                        results[data['category_name']].append(todo)
        


        return results
                    

    def new(self, task, category=CATEGORY_GENERAL, description=None,
            due_on=None):

        if due_on:
            if type(due_on) == date:
                due_on = due_on.isoformat()
            elif type(due_on) == str:
                # all good
                pass
            else:
                raise ValueError('Invalid due_on type. Must be date or str')

        file_name = "{}.json".format(category)
        file_path = self.path / file_name

        if not file_path.exists():
            file_contents = {
                'category_name':category.title(),
                'todos':[]
                }
        else:
            with open(file_path,'r') as file:
                file_contents = json.load(file)
        
        todo_task = {
            'task': task,
            'description': description,
            'due_on': due_on,
            'status':self.STATUS_PENDING
        }

        file_contents['todos'].append(todo_task)

        with open(file_path,'w') as file:
            json.dump(file_contents,file)