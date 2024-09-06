import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Sign up"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    
    def add(e):
        page.add(
            ft.Text(f"Nom : {nom_complet.value}")
        )
        page.add(
            ft.Text(f"Nom : {email.value}")
        )
        if password.value != confirm_password.value:
            page.add(
                ft.Text("Les mot deux ne correspondent pas", color='red')
            )
        else:
            page.add(
                ft.Text("Compte creer avec succès")
            )
        nom_complet.value = ""
        email.value = ""
        password.value = ""
        confirm_password.value = ""
    
    page.add(
        ft.Text("Sign up", size=25, weight=ft.FontWeight.BOLD)
    )
    nom_complet = ft.TextField(label="Nom complet", width=400)
    email = ft.TextField(label="Email", width=400)
    password = ft.TextField(label="Mot de passe", width=190, password=True)
    confirm_password = ft.TextField(label="Confirmer mot de passe", width=200)
    
    page.add(
        ft.Column(
            [
                nom_complet, email
            ]
        )
    )
    page.add(
        ft.Row(
            [
                password, confirm_password
            ],
            alignment=ft.MainAxisAlignment.CENTER,

        )
    )
    page.add(
        ft.CupertinoFilledButton(content=ft.Text("Sign up"), width=400, on_click=add),
    )
    page.add(
        ft.Text("Do you have account? Sign in",)
    )
    
ft.app(main)