import tkinter as tk
from tkinter import messagebox, simpledialog
import json

# Definição de cores e estilos
COLORS = {
    'primary': '#47ba00',
    'danger': '#e74c3c',
    'background': '#f0f0f0',
    'text': '#333333',
    'white': '#ffffff'
}

STYLES = {
    'title_font': ('Arial', 16, 'bold'),
    'heading_font': ('Arial', 14, 'bold'),
    'text_font': ('Arial', 12),
    'button_font': ('Arial', 12)
}

def load_products():
    try:
        with open('produtos.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open('produtos.json', 'w') as file:
        json.dump(products, file, indent=4)

def show_products(page=1, search_query=""):
    products = load_products()
    filtered_products = [p for p in products if search_query.lower() in p['nome'].lower()]
    products_per_page = 5
    start = (page - 1) * products_per_page
    end = start + products_per_page
    
    for widget in frame_list.winfo_children():
        widget.destroy()
    
    for product in filtered_products[start:end]:
        button = tk.Button(frame_list, 
                          text=product['nome'], 
                          command=lambda p=product: show_product_details(p),
                          font=STYLES['text_font'],
                          bg=COLORS['white'],
                          fg=COLORS['text'],
                          relief="solid", 
                          bd=1,
                          width=35, 
                          height=2, 
                          anchor='w', 
                          justify='left', 
                          padx=10, 
                          pady=5)
        button.pack(fill='x', padx=10, pady=5, ipadx=10)
        
        # Efeito hover
        button.bind('<Enter>', lambda e, b=button: b.config(bg='#f8f8f8'))
        button.bind('<Leave>', lambda e, b=button: b.config(bg=COLORS['white']))
    
    update_pagination(page, len(filtered_products), products_per_page)

def show_product_details(product):
    details_window = tk.Toplevel(root)
    details_window.title(f"Detalhes de {product['nome']}")
    details_window.config(bg=COLORS['background'])
    details_window.geometry("500x500")  # Aumentei a altura para acomodar o botão

    # Frame principal com padding
    main_frame = tk.Frame(details_window, bg=COLORS['background'], padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Título
    title_label = tk.Label(main_frame, 
                          text=product['nome'],
                          font=STYLES['title_font'],
                          bg=COLORS['background'],
                          fg=COLORS['text'])
    title_label.pack(pady=(0, 20))

    # Frame para os detalhes
    details_frame = tk.Frame(main_frame, bg=COLORS['white'], padx=20, pady=20, relief="solid", bd=1)
    details_frame.pack(fill="both", expand=True)

    # Campos dos detalhes
    fields = [
        ("Descrição", product['descricao']),
        ("Imagem", product['imagem']),
        ("Link", product['link'])
    ]
    
    for label_text, value in fields:
        field_frame = tk.Frame(details_frame, bg=COLORS['white'])
        field_frame.pack(fill="x", pady=10)
        
        label = tk.Label(field_frame,
                        text=label_text + ":",
                        font=STYLES['heading_font'],
                        bg=COLORS['white'],
                        fg=COLORS['text'])
        label.pack(anchor="w")
        
        value_label = tk.Label(field_frame,
                             text=value,
                             font=STYLES['text_font'],
                             bg=COLORS['white'],
                             fg=COLORS['text'],
                             wraplength=400)
        value_label.pack(anchor="w", pady=(5, 0))

    def delete_product():
        confirm = messagebox.askyesno("Deseja apagar?", f"Você deseja apagar o produto {product['nome']}?")
        if confirm:
            confirm_final = messagebox.askyesno("Tem Certeza?", f"Tem certeza que deseja apagar {product['nome']}?")
            if confirm_final:
                products = load_products()
                products = [p for p in products if p != product]
                save_products(products)
                details_window.destroy()
                show_products()

    # Frame para o botão de exclusão
    button_frame = tk.Frame(main_frame, bg=COLORS['background'])
    button_frame.pack(fill="x", pady=20)

    # Botão de exclusão
    delete_button = tk.Button(button_frame,
                            text="Excluir Produto",
                            command=delete_product,
                            font=STYLES['button_font'],
                            bg=COLORS['danger'],
                            fg=COLORS['white'],
                            relief="flat",
                            padx=20,
                            pady=10,
                            width=20)
    delete_button.pack(pady=10)

def add_product():
    new_name = simpledialog.askstring("Adicionar Nome", "Nome do produto:")
    new_desc = simpledialog.askstring("Adicionar Descrição", "Descrição do produto:")
    new_image = simpledialog.askstring("Adicionar Imagem", "Link da imagem:")
    new_link = simpledialog.askstring("Adicionar Link", "Link do produto:")

    if new_name and new_desc and new_image and new_link:
        products = load_products()
        new_product = {
            'nome': new_name,
            'descricao': new_desc,
            'imagem': new_image,
            'link': new_link
        }
        products.insert(0, new_product)
        save_products(products)
        show_products()


def update_pagination(page, total_products, products_per_page):
    total_pages = (total_products // products_per_page) + (1 if total_products % products_per_page > 0 else 0)
    
    for widget in frame_pagination.winfo_children():
        widget.destroy()
    
    if page > 1:
        prev_button = tk.Button(frame_pagination, 
                              text="Anterior", 
                              command=lambda: show_products(page-1), 
                              font=STYLES['button_font'], 
                              bg=COLORS['primary'], 
                              fg=COLORS['white'], 
                              relief="flat", 
                              padx=15,
                              pady=5)
        prev_button.pack(side="left", padx=10)
    
    if page < total_pages:
        next_button = tk.Button(frame_pagination, 
                              text="Próximo", 
                              command=lambda: show_products(page+1), 
                              font=STYLES['button_font'], 
                              bg=COLORS['primary'], 
                              fg=COLORS['white'], 
                              relief="flat",
                              padx=15,
                              pady=5)
        next_button.pack(side="right", padx=10)

def search_products():
    search_query = search_entry.get()
    show_products(page=1, search_query=search_query)

root = tk.Tk()
root.title("Gerenciador de Produtos")
root.state('normal')
root.config(bg=COLORS['background'])
root.geometry("600x700")

# Frame principal
main_container = tk.Frame(root, bg=COLORS['background'], padx=20, pady=20)
main_container.pack(fill="both", expand=True)

# Título
title_label = tk.Label(main_container,
                      text="Gerenciador de Produtos",
                      font=STYLES['title_font'],
                      bg=COLORS['background'],
                      fg=COLORS['text'])
title_label.pack(pady=(0, 20))

# Frame de busca
search_frame = tk.Frame(main_container, bg=COLORS['white'], padx=20, pady=20, relief="solid", bd=1)
search_frame.pack(fill="x", pady=(0, 20))

search_label = tk.Label(search_frame,
                       text="Buscar Produto:",
                       font=STYLES['heading_font'],
                       bg=COLORS['white'],
                       fg=COLORS['text'])
search_label.pack(pady=(0, 10))

search_entry = tk.Entry(search_frame,
                       font=STYLES['text_font'],
                       width=35,
                       relief="solid",
                       bd=1)
search_entry.pack(pady=(0, 10))

search_button = tk.Button(search_frame,
                         text="Buscar",
                         command=search_products,
                         font=STYLES['button_font'],
                         bg=COLORS['primary'],
                         fg=COLORS['white'],
                         relief="flat",
                         padx=20,
                         pady=5)
search_button.pack()

# Frame da lista
frame_list = tk.Frame(main_container, bg=COLORS['background'])
frame_list.pack(fill="both", expand=True)

# Frame de paginação
frame_pagination = tk.Frame(main_container, bg=COLORS['background'])
frame_pagination.pack(pady=20)

# Botão de adicionar
add_button = tk.Button(main_container,
                      text="Adicionar Produto",
                      command=add_product,
                      font=STYLES['button_font'],
                      bg=COLORS['primary'],
                      fg=COLORS['white'],
                      relief="flat",
                      padx=20,
                      pady=10)
add_button.pack(pady=20)

show_products()

root.mainloop()
