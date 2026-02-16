import re

# Leer archivo completo original
with open(r'c:\Users\Angel Sebastian\Documents\Proyectos\ait_anzoategui\posts\views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Leer las 3 funciones corregidas
with open(r'c:\Users\Angel Sebastian\Documents\Proyectos\ait_anzoategui\posts\views_partial.py', 'r', encoding='utf-8') as f:
    partial = f.read()

# Extraer manage_user
manage_pattern = r'@login_required\r?\ndef manage_user\(request, user_id\):.*?(?=\r?\n@login_required\r?\ndef toggle_user)'
manage_new = re.search(manage_pattern, partial, re.DOTALL).group(0)

# Extraer toggle_user  
toggle_pattern = r'@login_required\r?\ndef toggle_user\(request, user_id\):.*?(?=\r?\n@login_required\r?\ndef delete_user)'
toggle_new = re.search(toggle_pattern, partial, re.DOTALL).group(0)

# Extraer delete_user
delete_pattern = r'@login_required\r?\ndef delete_user\(request, user_id\):.*$'
delete_new = re.search(delete_pattern, partial, re.DOTALL).group(0)

# Reemplazar en el contenido original
content = re.sub(manage_pattern, manage_new, content, flags=re.DOTALL)
content = re.sub(toggle_pattern, toggle_new, content, flags=re.DOTALL)
content = re.sub(delete_pattern, delete_new, content, flags=re.DOTALL)

# Guardar
with open(r'c:\Users\Angel Sebastian\Documents\Proyectos\ait_anzoategui\posts\views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Funciones reemplazadas correctamente")
