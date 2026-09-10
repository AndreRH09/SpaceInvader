from game import Game


def main():
    """Función principal que inicia el juego."""
    print("=" * 50)
    print("SPACE INVADERS - Versión Modular Mejorada")
    print("=" * 50)
    print("\nControles:")
    print("  ← / → : Mover nave")
    print("  SPACE : Disparar")
    print("  M     : Silenciar/Activar audio")
    print("  ESC   : Salir del juego")
    print("\nIniciando juego...\n")

    game = Game()
    game.run()

    print("\nGracias por jugar Space Invaders")
    print("=" * 50)


if __name__ == "__main__":
    main()
