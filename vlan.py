
def validar_vlan(numero_vlan):
    """
    Función que valida si una VLAN está en rango normal o extendido
    
    Rangos:
    - Normal: 1 - 1005
    - Extendido: 1006 - 4094
    """
    if 1 <= numero_vlan <= 1005:
        return "NORMAL"
    elif 1006 <= numero_vlan <= 4094:
        return "EXTENDIDO"
    else:
        return "INVÁLIDO"

def main():
    """
    Función principal del script
    """
    print("\n" + "="*50)
    print("     VALIDADOR DE RANGO DE VLAN")
    print("="*50)
    print("\nRangos válidos:")
    print("  • VLAN Normal:    1 - 1005")
    print("  • VLAN Extendido: 1006 - 4094")
    print("\n" + "-"*50)
    
    try:
      
        entrada = input("\nIngrese el número de VLAN: ")
        
       
        numero_vlan = int(entrada)
        
     
        rango = validar_vlan(numero_vlan)
        
      
        print("\n" + "="*50)
        print(f"  VLAN {numero_vlan}:")
        
        if rango == "INVÁLIDO":
            print(f"  ❌ Número fuera de rango (1-4094)")
        else:
            print(f"  ✅ Rango: {rango}")
            if rango == "NORMAL":
                print("  📌 VLAN estándar (1-1005)")
            else:
                print("  📌 VLAN extendida (1006-4094)")
        print("="*50 + "\n")
        
    except ValueError:
       
        print("\n❌ Error: Debe ingresar un número entero válido.\n")


if __name__ == "__main__":
    main()