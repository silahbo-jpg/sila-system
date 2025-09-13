def test_deprecated_import():
    try:
        import deprecated
        print(f"✅ Módulo 'deprecated' importado com sucesso. Versão: {deprecated.__version__}")
    except ImportError as e:
        print(f"❌ Erro ao importar 'deprecated': {e}")

if __name__ == "__main__":
    test_deprecated_import()
