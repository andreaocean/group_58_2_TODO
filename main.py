from db import main_db
import flet as fl 


def main(page: fl.Page):
    page.title = "ToDo List"
    page.theme_mode = fl.ThemeMode.LIGHT

    task_list = fl.Column()

    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text))

        page.update()

    def create_task_row(task_id, task_text):
        task_field = fl.TextField(value=task_text, read_only=True, expand=True)

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
            main_db.delete_task(task_id=task_id, )
            task_list.controls.clear()
            page.update()

        delete_button = fl.IconButton(icon=fl.Icons.DELETE, on_click=delete_task)

        return fl.Row([task_field, edit_button, save_button, delete_button])
 

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task))
            task_input.value = ""
            page.update()


# HW 5,6
    def delete_all(_):

        main_db.delete_all_task()
        task_list.controls.clear()
            
        page.update()



    task_input = fl.TextField(label='Enter task', expand=True)
    add_button = fl.ElevatedButton("ADD", on_click=add_task)
    delete_all_button = fl.ElevatedButton("DELETE ALL", on_click=delete_all)

    page.add(fl.Row([task_input, add_button]),  task_list, delete_all_button)

    load_task()


if __name__ == "__main__":
    main_db.init_db()
    fl.app(target=main)