

def mostrar_integrantes():
   
  
    integrantes = [
        "Benjamin Leon"
        
    ]
    
    print("\n" + "="*50)
    print("        INTEGRANTES DEL GRUPO")
    print("="*50)
    

    for i, nombre in enumerate(integrantes, 1):
        print(f"  {i}. {nombre}")
    
    print("="*50)
    print(f"  Total de integrantes: {len(integrantes)}")
    print("="*50 + "\n")


if __name__ == "__main__":
    mostrar_integrantes()