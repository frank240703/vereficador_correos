import dns.resolver

# Ruta al archivo con la lista de correos
input_file_path = 'lista_correos.txt'
# Ruta al archivo de salida
output_file_path = 'correos_validos.txt'  # Nombre cambiado para reflejar el contenido

# Dominios comunes a ignorar
common_domains = {'gmail.com', 'hotmail.com', 'yahoo.com'}

def extract_domain(email):
    return email.split('@')[-1].strip()

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return bool(answers)
    except:
        return False

def read_emails_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            for email in line.split(','):
                yield email.strip()

def main():
    unique_domains = set()
    valid_emails = []  # Almacena correos válidos

    for email in read_emails_from_file(input_file_path):
        domain = extract_domain(email)
        if domain not in common_domains and domain not in unique_domains:
            unique_domains.add(domain)
            if has_mx_record(domain):
                valid_emails.append(email)  # Agrega el correo electrónico a la lista de válidos
                print(f"Correo válido: {email}")

    with open(output_file_path, 'w') as file:
        for email in valid_emails:
            file.write(f"{email}\n")  # Escribe cada correo válido en el archivo

    print(f"Los correos válidos han sido guardados en el archivo {output_file_path}")

if __name__ == '__main__':
    main()
