# main.py
import flet
from flet import (
    Page, Text, TextField, ElevatedButton, Column, Row, IconButton, icons, 
    ListView, Container, SnackBar, CupertinoFilledButton
)
from database import (
    create_table, add_task, get_tasks, delete_task, update_task
)

def main(page: Page):
    page.title = "Todo"
    page.vertical_alignment = "start"
    page.horizontal_alignment = "center"
    page.padding = 10
    page.window_width = 440  # Largeur typique pour les mobiles (en pixels)
    page.window_height = 667  # Hauteur typique pour les mobiles (en pixels)
    
    # Activer le mode "Responsive"
    page.scroll = "adaptive"  # Gérer le défilement si le contenu dépasse la fenêtre


    # Initialiser la base de données
    create_table()

    # Fonction pour rafraîchir la liste des tâches
    def refresh_tasks(e=None):
        task_list.controls.clear()
        tasks = get_tasks()
        for task in tasks:
            task_id, task_text = task
            task_container = Container(
                content=Row(
                    [
                        Text(task_text, expand=True, color="black", size=16),
                        IconButton(
                            icon=icons.DELETE,
                            icon_color="red",
                            on_click=lambda e, id=task_id: delete_and_refresh(id)
                        ),
                        IconButton(
                            icon=icons.EDIT,
                            icon_color="blue",
                            on_click=lambda e, id=task_id: edit_task(e, id)
                        ),
                    ],
                    alignment="spaceBetween"
                ),
                padding=10,
                bgcolor="#f9f9f9",
                border_radius=5,
                margin=5
            )
            task_list.controls.append(task_container)
        page.update()

    # Fonction pour ajouter une tâche
    def add_task_event(e):
        task = task_input.value.strip()
        if task:
            add_task(task)
            task_input.value = ""
            refresh_tasks()
            page.snack_bar = SnackBar(content=Text("Tâche ajoutée avec succès!"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = SnackBar(content=Text("Veuillez entrer une tâche valide."))
            page.snack_bar.open = True
            page.update()

    # Fonction pour supprimer une tâche
    def delete_and_refresh(task_id):
        delete_task(task_id)
        refresh_tasks()
        page.snack_bar = SnackBar(content=Text("Tâche supprimée."))
        page.snack_bar.open = True
        page.update()

    # Fonction pour éditer une tâche
    def edit_task(e, task_id):
        # Récupérer la tâche actuelle
        tasks = get_tasks()
        current_task = next((t for t in tasks if t[0] == task_id), None)
        if current_task:
            edit_window = flet.Popup(
                content=Column(
                    [
                        Text("Modifier la tâche", size=20),
                        TextField(
                            label="Nouvelle tâche",
                            value=current_task[1],
                            autofocus=True,
                            on_submit=lambda e: save_edit(task_id, edit_input.value)
                        ),
                        Row(
                            [
                                ElevatedButton("Enregistrer", on_click=lambda e: save_edit(task_id, edit_input.value)),
                                ElevatedButton("Annuler", on_click=lambda e: edit_window.close()),
                            ]
                        )
                    ],
                    tight=True
                )
            )
            edit_input = edit_window.content.controls[1]
            edit_window.open = True
            page.overlay.append(edit_window)
            page.update()

    # Fonction pour enregistrer l'édition
    def save_edit(task_id, new_task):
        if new_task.strip():
            update_task(task_id, new_task.strip())
            refresh_tasks()
            page.snack_bar = SnackBar(content=Text("Tâche mise à jour."))
            page.snack_bar.open = True
            page.update()
            # Fermer la popup
            for overlay in page.overlay:
                if isinstance(overlay, flet.Popup):
                    overlay.close()
            page.update()
        else:
            page.snack_bar = SnackBar(content=Text("La tâche ne peut pas être vide."))
            page.snack_bar.open = True
            page.update()

    # Interface de saisie
    task_input = TextField(
        label="Nouvelle tâche",
        width=300,
        on_submit=add_task_event
    )
    # add_button = CupertinoFilledButton(content=Text("Ajouter",), width=100, on_click=add_task_event),
    add_button = CupertinoFilledButton(content=Text("Ajouter"), width=100, padding=5, on_click=add_task_event)

    # Liste des tâches
    task_list = ListView(expand=True)

    # Ajouter les composants à la page
    page.add(
        Text("Liste des Tâches", size=24, weight="bold"),
        Row([task_input, add_button], alignment="center"),
        task_list
    )

    # Charger les tâches au démarrage
    refresh_tasks()

# Exécuter l'application Flet
flet.app(main)
