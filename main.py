from db import main_db
import flet as fl 


def main(page: fl.Page):
    page.title = "ToDo List"
    page.theme_mode = fl.ThemeMode.LIGHT

    task_list = fl.Column()

        
    counter_text = fl.Text("0/100", size=12, color="gray")
    warning_text = fl.Text("", color="red",)

    filter_type = 'all'

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, completed=completed))

        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = fl.TextField(value=task_text, read_only=True, expand=True)
        checkbox = fl.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))


        def enable_edit(_):
            task_field.read_only = False
            task_field.update()
        
        edit_button=fl.IconButton(icon=fl.Icons.EDIT, on_click=enable_edit)


        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            page.update()

        save_button = fl.IconButton(icon=fl.Icons.SAVE, on_click=save_task)

# dop zadanie lesson6
        def delete_task(_):
            main_db.delete_task(task_id=task_id)
            load_task()
            page.update()

        delete_button = fl.IconButton(icon=fl.Icons.DELETE, on_click=delete_task)

        return fl.Row([checkbox, task_field, edit_button, save_button, delete_button])
 

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completed=None))
            task_input.value = ""
            warning_text.value = ""
            counter_text.value = "0 / 100"
            
            page.update()


# HW 5,6
    def delete_all(_):

        main_db.delete_all_task()
        task_list.controls.clear()
            
        page.update()

# HW 7
    def len_task(_):
        current_len = len(task_input.value)
        counter_text.value = f"{current_len} / 100"

        if current_len > 100:
            task_input.value = task_input.value[:100]
            warning_text.value = "Enter only 100 symbols!"
            counter_text.value = "100 / 100"
        else:
            warning_text.value = ""
        
        page.update()
    

    task_input = fl.TextField(label='Enter task', expand=True, on_change=len_task)
    add_button = fl.ElevatedButton("ADD", on_click=add_task)
    delete_all_button = fl.ElevatedButton("DELETE ALL", on_click=delete_all)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task

    filter_buttons = fl.Row([
        fl.ElevatedButton('All tasks', on_click=lambda e: set_filter('all')),
        fl.ElevatedButton('Is running', on_click=lambda e: set_filter('uncompleted')),
        fl.ElevatedButton('Done', on_click=lambda e: set_filter('completed'))
    ], alignment=fl.MainAxisAlignment.SPACE_EVENLY)

    page.add(fl.Row([task_input, add_button]), 
             fl.Row([warning_text, counter_text], alignment=fl.MainAxisAlignment.END), 
             filter_buttons, task_list, delete_all_button)

    load_task()


if __name__ == "__main__":
    main_db.init_db()
    fl.app(target=main)