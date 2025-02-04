import fire

from talk_codebase.config import CONFIGURE_STEPS, save_config, get_config, config_path, remove_api_key, \
    remove_model_type
from talk_codebase.consts import DEFAULT_CONFIG
from talk_codebase.llm import factory_llm


def configure(reset=True):
    if reset:
        remove_api_key()
        remove_model_type()
    config = get_config()
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    for step in CONFIGURE_STEPS:
        step(config)
    save_config(config)


def chat(root_dir=None):
    configure(False)
    config = get_config()
    llm = factory_llm(root_dir, config)
    while True:
        query = input("👉 ").lower().strip()
        if not query:
            print("🤖 Please enter a query")
            continue
        if query in ('exit', 'quit'):
            break
        llm.send_query(query)


def main():
    print(f"🤖 Config path: {config_path}:")
    try:
        fire.Fire({
            "chat": chat,
            "configure": lambda: configure(True)
        })
    except KeyboardInterrupt:
        print("\n🤖 Bye!")
    except Exception as e:
        if str(e) == "<empty message>":
            print("🤖 Please configure your API key. Use talk-codebase configure")
        else:
            raise e


if __name__ == "__main__":
    main()
